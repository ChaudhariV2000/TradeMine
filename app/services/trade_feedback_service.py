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