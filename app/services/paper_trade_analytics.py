from app.database.database import SessionLocal
from app.database.models import PaperTrade


class PaperTradeAnalytics:
    """
    Calculates paper trading performance.
    """

    def __init__(self):
        self.db = SessionLocal()

    def summary(self):
        trades = self.db.query(PaperTrade).all()

        open_trades = [
            t for t in trades
            if t.status == "OPEN"
        ]

        closed_trades = [
            t for t in trades
            if t.status != "OPEN"
        ]

        winning_trades = [
            t for t in closed_trades
            if t.pnl and t.pnl > 0
        ]

        losing_trades = [
            t for t in closed_trades
            if t.pnl and t.pnl < 0
        ]

        total_pnl = round(
            sum(t.pnl or 0 for t in closed_trades),
            2,
        )

        win_rate = round(
            (len(winning_trades) / len(closed_trades)) * 100,
            2,
        ) if closed_trades else 0

        return {
            "total_trades": len(trades),
            "open_trades": len(open_trades),
            "closed_trades": len(closed_trades),
            "winning_trades": len(winning_trades),
            "losing_trades": len(losing_trades),
            "win_rate": win_rate,
            "total_pnl": total_pnl,
        }