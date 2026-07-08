from datetime import datetime

from app.database.database import SessionLocal
from app.database.models import DecisionJournal
from app.repositories.trade_feedback_repository import TradeFeedbackRepository


class TradeFeedbackService:

    def __init__(self):
        self.db = SessionLocal()
        self.repo = TradeFeedbackRepository()

    def _latest_decision(self, symbol: str):
        return (
            self.db.query(DecisionJournal)
            .filter(DecisionJournal.symbol == symbol)
            .order_by(DecisionJournal.id.desc())
            .first()
        )

    def record_trade(self, trade, exit_reason: str):
        decision = self._latest_decision(trade.symbol)

        entry_date = trade.entry_date
        exit_date = trade.exit_date

        holding_days = 0

        try:
            holding_days = (
                datetime.fromisoformat(exit_date)
                - datetime.fromisoformat(entry_date)
            ).days
        except Exception:
            holding_days = 0

        pnl = trade.pnl or 0

        data = {
            "symbol": trade.symbol,
            "strategy": trade.strategy,

            "recommendation": decision.recommendation if decision else "UNKNOWN",
            "confidence": decision.confidence if decision else 0,

            "technical_score": decision.technical_score if decision else 0,
            "news_score": decision.news_score if decision else 0,
            "risk_score": decision.risk_score if decision else 0,
            "fundamental_score": decision.fundamental_score if decision else 0,

            "entry_price": trade.entry_price,
            "exit_price": trade.exit_price,
            "shares": trade.shares,

            "pnl": pnl,
            "outcome": "WIN" if pnl > 0 else "LOSS",
            "exit_reason": exit_reason,

            "entry_date": entry_date,
            "exit_date": exit_date,
            "holding_days": holding_days,

            "created_at": datetime.now().isoformat(),
        }

        return self.repo.save(data)

    def summary(self):
        rows = self.repo.all()

        if not rows:
            return {
                "total_feedback_records": 0,
                "wins": 0,
                "losses": 0,
                "average_confidence": 0,
                "average_pnl": 0,
            }

        wins = sum(1 for r in rows if r.outcome == "WIN")
        losses = sum(1 for r in rows if r.outcome == "LOSS")

        return {
            "total_feedback_records": len(rows),
            "wins": wins,
            "losses": losses,
            "average_confidence": round(
                sum(r.confidence or 0 for r in rows) / len(rows),
                2,
            ),
            "average_pnl": round(
                sum(r.pnl or 0 for r in rows) / len(rows),
                2,
            ),
        }
    def strategy_breakdown(self):
        rows = self.repo.all()

        if not rows:
            return []

        result = {}

        for trade in rows:
            strategy = trade.strategy

            if strategy not in result:
                result[strategy] = {
                    "strategy": strategy,
                    "total": 0,
                    "wins": 0,
                    "losses": 0,
                    "total_pnl": 0,
                }

            result[strategy]["total"] += 1
            result[strategy]["total_pnl"] += trade.pnl or 0

            if trade.outcome == "WIN":
                result[strategy]["wins"] += 1
            else:
                result[strategy]["losses"] += 1

        output = []

        for s in result.values():
            s["win_rate"] = round(
                (s["wins"] / s["total"]) * 100,
                2,
            )

            s["average_pnl"] = round(
                s["total_pnl"] / s["total"],
                2,
            )

            output.append(s)

        output.sort(
            key=lambda x: x["win_rate"],
            reverse=True,
        )

        return output

    def symbol_breakdown(self):
        rows = self.repo.all()

        if not rows:
            return []

        result = {}

        for trade in rows:
            symbol = trade.symbol

            if symbol not in result:
                result[symbol] = {
                    "symbol": symbol,
                    "total": 0,
                    "wins": 0,
                    "losses": 0,
                    "total_pnl": 0,
                }

            result[symbol]["total"] += 1
            result[symbol]["total_pnl"] += trade.pnl or 0

            if trade.outcome == "WIN":
                result[symbol]["wins"] += 1
            else:
                result[symbol]["losses"] += 1

        output = []

        for s in result.values():
            s["win_rate"] = round((s["wins"] / s["total"]) * 100, 2)
            s["average_pnl"] = round(s["total_pnl"] / s["total"], 2)
            output.append(s)

        output.sort(key=lambda x: x["win_rate"], reverse=True)

        return output

    def confidence_breakdown(self):
        rows = self.repo.all()

        buckets = {
            "0-49": [],
            "50-69": [],
            "70-84": [],
            "85-100": [],
        }

        for trade in rows:
            confidence = trade.confidence or 0

            if confidence < 50:
                buckets["0-49"].append(trade)
            elif confidence < 70:
                buckets["50-69"].append(trade)
            elif confidence < 85:
                buckets["70-84"].append(trade)
            else:
                buckets["85-100"].append(trade)

        result = []

        for bucket, trades in buckets.items():
            if not trades:
                result.append({
                    "confidence_range": bucket,
                    "total": 0,
                    "wins": 0,
                    "losses": 0,
                    "win_rate": 0,
                    "average_pnl": 0,
                })
                continue

            wins = sum(1 for t in trades if t.outcome == "WIN")
            losses = sum(1 for t in trades if t.outcome == "LOSS")
            total_pnl = sum(t.pnl or 0 for t in trades)

            result.append({
                "confidence_range": bucket,
                "total": len(trades),
                "wins": wins,
                "losses": losses,
                "win_rate": round((wins / len(trades)) * 100, 2),
                "average_pnl": round(total_pnl / len(trades), 2),
            })

        return result
    def exit_reason_breakdown(self):
        rows = self.repo.all()

        result = {}

        for trade in rows:
            reason = trade.exit_reason or "UNKNOWN"

            if reason not in result:
                result[reason] = {
                    "exit_reason": reason,
                    "total": 0,
                    "wins": 0,
                    "losses": 0,
                    "total_pnl": 0,
                }

            result[reason]["total"] += 1
            result[reason]["total_pnl"] += trade.pnl or 0

            if trade.outcome == "WIN":
                result[reason]["wins"] += 1
            else:
                result[reason]["losses"] += 1

        output = []

        for r in result.values():
            r["win_rate"] = round((r["wins"] / r["total"]) * 100, 2)
            r["average_pnl"] = round(r["total_pnl"] / r["total"], 2)
            output.append(r)

        output.sort(key=lambda x: x["total"], reverse=True)

        return output