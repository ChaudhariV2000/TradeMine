from datetime import datetime

from app.database.database import SessionLocal
from app.database.models import PaperTrade


class TradeCleanupService:
    """
    Cleans invalid paper trades.
    """

    def __init__(self):
        self.db = SessionLocal()

    def close_invalid_trades(self):
        invalid_trades = (
            self.db.query(PaperTrade)
            .filter(PaperTrade.status == "OPEN")
            .filter(PaperTrade.shares <= 0)
            .all()
        )

        closed = []

        for trade in invalid_trades:
            trade.status = "INVALID"
            trade.exit_price = trade.entry_price
            trade.exit_date = datetime.now().isoformat()
            trade.pnl = 0.0

            closed.append({
                "id": trade.id,
                "symbol": trade.symbol,
                "reason": "Invalid zero-share trade closed",
            })

        self.db.commit()

        return {
            "invalid_trades_closed": len(closed),
            "closed": closed,
        }