from collections import defaultdict

from app.database.database import SessionLocal
from app.database.models import PaperTrade


class SymbolAnalyticsService:
    """
    Analytics grouped by stock symbol.
    """

    def __init__(self):
        self.db = SessionLocal()

    def summary(self):
        trades = (
            self.db.query(PaperTrade)
            .filter(PaperTrade.status != "OPEN")
            .all()
        )

        analytics = defaultdict(
            lambda: {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "total_pnl": 0.0,
            }
        )

        for trade in trades:
            row = analytics[trade.symbol]
            pnl = trade.pnl or 0

            row["trades"] += 1
            row["total_pnl"] += pnl

            if pnl > 0:
                row["wins"] += 1
            elif pnl < 0:
                row["losses"] += 1

        result = {}

        for symbol, row in analytics.items():
            trades = row["trades"]

            result[symbol] = {
                "trades": trades,
                "wins": row["wins"],
                "losses": row["losses"],
                "win_rate": round(
                    (row["wins"] / trades) * 100,
                    2,
                ) if trades else 0,
                "total_pnl": round(row["total_pnl"], 2),
                "average_pnl": round(
                    row["total_pnl"] / trades,
                    2,
                ) if trades else 0,
            }

        return result