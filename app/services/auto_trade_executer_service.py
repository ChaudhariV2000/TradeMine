import json
import threading
from datetime import datetime
from pathlib import Path
from typing import Callable
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config.logging import logger
from app.config.settings import settings
from app.services.daily_scheduler_service import DailySchedulerService
from app.services.trade_exit_service import TradeExitService


class AutoPaperTradeExecutor:
    """
    Automatically runs TradeMine's paper-trading workflow.

    Jobs:
    - Full daily cycle at 09:20 IST, Monday-Friday.
    - Exit monitoring every 15 minutes during market hours.
    """

    TIMEZONE = ZoneInfo("Asia/Kolkata")

    def __init__(self):
        self.scheduler = BackgroundScheduler(
            timezone=self.TIMEZONE,
        )

        self.daily_service = DailySchedulerService()
        self.exit_service = TradeExitService()

        self.scan_function: Callable | None = None

        self.enabled = True
        self.is_running = False
        self.last_run_started_at = None
        self.last_run_completed_at = None
        self.last_run_status = "NEVER_RUN"
        self.last_error = None
        self.last_result = None

        self._lock = threading.Lock()

        self.history_file = (
            settings.DATA_DIR / "auto_executor_history.json"
        )

        settings.DATA_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def configure(self, scan_function: Callable):
        self.scan_function = scan_function

    def start(self):
        if self.scheduler.running:
            return

        self.scheduler.add_job(
            self._scheduled_daily_run,
            CronTrigger(
                day_of_week="mon-fri",
                hour=9,
                minute=20,
                timezone=self.TIMEZONE,
            ),
            id="trademine_daily_cycle",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=900,
        )

        self.scheduler.add_job(
            self._scheduled_exit_check,
            CronTrigger(
                day_of_week="mon-fri",
                hour="9-15",
                minute="0,15,30,45",
                timezone=self.TIMEZONE,
            ),
            id="trademine_exit_monitor",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=300,
        )

        self.scheduler.start()

        logger.info(
            "Auto paper trade executor started"
        )

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown(
                wait=False,
            )

        logger.info(
            "Auto paper trade executor stopped"
        )

    def enable(self):
        self.enabled = True

        return self.status()

    def disable(self):
        self.enabled = False

        return self.status()

    def run_now(self):
        return self._run_daily_cycle(
            trigger="MANUAL",
            force=True,
        )

    def history(self, limit: int = 20):
        rows = self._load_history()

        return rows[-limit:][::-1]

    def status(self):
        jobs = []

        if self.scheduler.running:
            for job in self.scheduler.get_jobs():
                jobs.append({
                    "id": job.id,
                    "next_run_time": (
                        job.next_run_time.isoformat()
                        if job.next_run_time
                        else None
                    ),
                })

        return {
            "enabled": self.enabled,
            "scheduler_running": self.scheduler.running,
            "is_executing": self.is_running,
            "last_run_status": self.last_run_status,
            "last_run_started_at": self.last_run_started_at,
            "last_run_completed_at": self.last_run_completed_at,
            "last_error": self.last_error,
            "jobs": jobs,
        }

    def _scheduled_daily_run(self):
        self._run_daily_cycle(
            trigger="SCHEDULED",
            force=False,
        )

    def _scheduled_exit_check(self):
        if not self.enabled:
            return

        if not self._is_market_monitoring_time():
            return

        try:
            result = self.exit_service.check_exits()

            self._append_history({
                "type": "EXIT_CHECK",
                "trigger": "SCHEDULED",
                "started_at": self._now_iso(),
                "completed_at": self._now_iso(),
                "status": "SUCCESS",
                "result": result,
            })

        except Exception as exc:
            logger.exception(
                "Scheduled exit check failed"
            )

            self._append_history({
                "type": "EXIT_CHECK",
                "trigger": "SCHEDULED",
                "started_at": self._now_iso(),
                "completed_at": self._now_iso(),
                "status": "FAILED",
                "error": str(exc),
            })

    def _run_daily_cycle(
        self,
        trigger: str,
        force: bool,
    ):
        if not self.enabled and not force:
            return {
                "status": "SKIPPED",
                "reason": "Auto executor is disabled",
            }

        if self.scan_function is None:
            return {
                "status": "FAILED",
                "reason": "Scan function is not configured",
            }

        if not force and self._already_ran_today():
            return {
                "status": "SKIPPED",
                "reason": "Daily cycle already completed today",
            }

        if not self._lock.acquire(blocking=False):
            return {
                "status": "SKIPPED",
                "reason": "Another execution is already running",
            }

        started_at = self._now_iso()

        self.is_running = True
        self.last_run_started_at = started_at
        self.last_run_status = "RUNNING"
        self.last_error = None

        try:
            result = self.daily_service.run(
                self.scan_function
            )

            completed_at = self._now_iso()

            self.last_result = result
            self.last_run_completed_at = completed_at
            self.last_run_status = "SUCCESS"

            history_row = {
                "type": "DAILY_CYCLE",
                "trigger": trigger,
                "started_at": started_at,
                "completed_at": completed_at,
                "status": "SUCCESS",
                "result": result,
            }

            self._append_history(history_row)

            return {
                "status": "SUCCESS",
                "trigger": trigger,
                "started_at": started_at,
                "completed_at": completed_at,
                "result": result,
            }

        except Exception as exc:
            completed_at = self._now_iso()

            self.last_run_completed_at = completed_at
            self.last_run_status = "FAILED"
            self.last_error = str(exc)

            logger.exception(
                "Auto paper trading cycle failed"
            )

            history_row = {
                "type": "DAILY_CYCLE",
                "trigger": trigger,
                "started_at": started_at,
                "completed_at": completed_at,
                "status": "FAILED",
                "error": str(exc),
            }

            self._append_history(history_row)

            return {
                "status": "FAILED",
                "trigger": trigger,
                "started_at": started_at,
                "completed_at": completed_at,
                "error": str(exc),
            }

        finally:
            self.is_running = False
            self._lock.release()

    def _already_ran_today(self):
        today = datetime.now(
            self.TIMEZONE
        ).date().isoformat()

        for row in reversed(
            self._load_history()
        ):
            if (
                row.get("type") == "DAILY_CYCLE"
                and row.get("status") == "SUCCESS"
                and str(
                    row.get("completed_at", "")
                ).startswith(today)
            ):
                return True

        return False

    def _is_market_monitoring_time(self):
        now = datetime.now(
            self.TIMEZONE
        )

        if now.weekday() >= 5:
            return False

        minutes = (
            now.hour * 60
            + now.minute
        )

        market_open = 9 * 60 + 15
        market_close = 15 * 60 + 30

        return (
            market_open
            <= minutes
            <= market_close
        )

    def _load_history(self):
        if not self.history_file.exists():
            return []

        try:
            content = self.history_file.read_text(
                encoding="utf-8"
            )

            if not content.strip():
                return []

            data = json.loads(content)

            return (
                data
                if isinstance(data, list)
                else []
            )

        except Exception:
            logger.exception(
                "Could not read auto executor history"
            )
            return []

    def _append_history(self, row: dict):
        rows = self._load_history()
        rows.append(row)

        rows = rows[-500:]

        temp_file = Path(
            str(self.history_file) + ".tmp"
        )

        temp_file.write_text(
            json.dumps(
                rows,
                indent=2,
                default=str,
            ),
            encoding="utf-8",
        )

        temp_file.replace(
            self.history_file
        )

    def _now_iso(self):
        return datetime.now(
            self.TIMEZONE
        ).isoformat()