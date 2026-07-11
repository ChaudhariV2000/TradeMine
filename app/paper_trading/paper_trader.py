import math
from datetime import datetime

import yfinance as yf

from app.collectors.market_collector import MarketCollector
from app.database.crud import PaperTradeCRUD
from app.database.database import SessionLocal
from app.database.models import PaperTrade
from app.services.trade_feedback_service import TradeFeedbackService


class PaperTrader:

    def __init__(self):
        self.db = SessionLocal()
        self.collector = MarketCollector()
        self.feedback_service = TradeFeedbackService()

    def open_trade(self, trade):
        trade["status"] = "OPEN"
        trade["entry_date"] = datetime.now().isoformat()
        trade["exit_price"] = None
        trade["exit_date"] = None
        trade["pnl"] = 0.0

        row = PaperTradeCRUD.create(
            self.db,
            trade,
        )

        return self._serialize_trade(row)

    def list_trades(self):
        rows = PaperTradeCRUD.all(self.db)

        return [
            self._serialize_trade(row)
            for row in rows
        ]

    def close_trade(
        self,
        trade_id: int,
        exit_price: float | None = None,
    ):
        trade = (
            self.db.query(PaperTrade)
            .filter(PaperTrade.id == trade_id)
            .first()
        )

        if not trade:
            return {
                "status": "NOT_FOUND",
                "reason": f"Trade {trade_id} was not found.",
            }

        if trade.status != "OPEN":
            return {
                "status": "ALREADY_CLOSED",
                "reason": (
                    f"Trade {trade_id} is already "
                    f"{trade.status}."
                ),
                "trade": self._serialize_trade(trade),
            }

        price = (
            float(exit_price)
            if exit_price is not None
            else self.collector.latest_price(trade.symbol)
        )

        if (
            not math.isfinite(price)
            or price <= 0
        ):
            return {
                "status": "FAILED",
                "reason": "A valid exit price is required.",
            }

        pnl = round(
            (price - trade.entry_price) * trade.shares,
            2,
        )

        updated = PaperTradeCRUD.update(
            self.db,
            trade.id,
            {
                "status": "MANUALLY_CLOSED",
                "exit_price": round(price, 2),
                "exit_date": datetime.now().isoformat(),
                "pnl": pnl,
            },
        )

        feedback_saved = True
        feedback_error = None

        try:
            self.feedback_service.record_trade(
                updated,
                "MANUAL",
            )
        except Exception as exc:
            feedback_saved = False
            feedback_error = str(exc)

        return {
            "status": "CLOSED",
            "reason": "MANUAL",
            "feedback_saved": feedback_saved,
            "feedback_error": feedback_error,
            "trade": self._serialize_trade(updated),
        }

    def update_open_trades(self):
        open_trades = PaperTradeCRUD.open_trades(
            self.db
        )

        results = []

        for trade in open_trades:
            ticker = yf.Ticker(
                f"{trade.symbol}.NS"
            )

            data = ticker.history(
                period="1d",
                interval="1d",
            )

            if data.empty:
                results.append({
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "status": "NO_PRICE_DATA",
                })
                continue

            current_price = float(
                data.iloc[-1]["Close"]
            )

            unrealized_pnl = (
                current_price - trade.entry_price
            ) * trade.shares

            update_data = {}
            exit_reason = None

            if current_price >= trade.target:
                exit_reason = "TARGET"

                update_data = {
                    "status": "TARGET_HIT",
                    "exit_price": current_price,
                    "exit_date": datetime.now().isoformat(),
                    "pnl": unrealized_pnl,
                }

            elif current_price <= trade.stop_loss:
                exit_reason = "STOP_LOSS"

                update_data = {
                    "status": "STOP_LOSS_HIT",
                    "exit_price": current_price,
                    "exit_date": datetime.now().isoformat(),
                    "pnl": unrealized_pnl,
                }

            if update_data:
                updated = PaperTradeCRUD.update(
                    self.db,
                    trade.id,
                    update_data,
                )

                feedback_saved = True
                feedback_error = None

                try:
                    self.feedback_service.record_trade(
                        updated,
                        exit_reason,
                    )
                except Exception as exc:
                    feedback_saved = False
                    feedback_error = str(exc)

                results.append({
                    "id": updated.id,
                    "symbol": updated.symbol,
                    "status": updated.status,
                    "exit_price": updated.exit_price,
                    "pnl": round(updated.pnl, 2),
                    "feedback_saved": feedback_saved,
                    "feedback_error": feedback_error,
                })

            else:
                results.append({
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "status": trade.status,
                    "current_price": round(
                        current_price,
                        2,
                    ),
                    "unrealized_pnl": round(
                        unrealized_pnl,
                        2,
                    ),
                })

        return results

    @staticmethod
    def _serialize_trade(trade):
        return {
            "id": trade.id,
            "symbol": trade.symbol,
            "strategy": trade.strategy,
            "entry_price": trade.entry_price,
            "stop_loss": trade.stop_loss,
            "target": trade.target,
            "shares": trade.shares,
            "status": trade.status,
            "entry_date": trade.entry_date,
            "exit_price": trade.exit_price,
            "exit_date": trade.exit_date,
            "pnl": trade.pnl,
        }