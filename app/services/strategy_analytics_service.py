from collections import defaultdict

from app.database.database import SessionLocal
from app.database.models import PaperTrade


class StrategyAnalyticsService:
    """
    Analytics grouped by strategy.
    """

    def __init__(self):
        self.db = SessionLocal()

    def summary(self):

        trades = (
            self.db.query(PaperTrade)
            .filter(PaperTrade.status == "CLOSED")
            .all()
        )

        analytics = defaultdict(
            lambda: {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "total_pnl": 0.0,
                "best_trade": None,
                "worst_trade": None,
            }
        )

        for trade in trades:

            row = analytics[trade.strategy]

            pnl = trade.pnl or 0

            row["trades"] += 1
            row["total_pnl"] += pnl

            if pnl > 0:
                row["wins"] += 1

            elif pnl < 0:
                row["losses"] += 1

            if (
                row["best_trade"] is None
                or pnl > row["best_trade"]
            ):
                row["best_trade"] = pnl

            if (
                row["worst_trade"] is None
                or pnl < row["worst_trade"]
            ):
                row["worst_trade"] = pnl

        result = {}

        for strategy, row in analytics.items():

            trades = row["trades"]

            win_rate = (
                round(
                    row["wins"] / trades * 100,
                    2,
                )
                if trades
                else 0
            )

            avg_pnl = (
                round(
                    row["total_pnl"] / trades,
                    2,
                )
                if trades
                else 0
            )

            result[strategy] = {
                "trades": trades,
                "wins": row["wins"],
                "losses": row["losses"],
                "win_rate": win_rate,
                "total_pnl": round(
                    row["total_pnl"],
                    2,
                ),
                "average_pnl": avg_pnl,
                "best_trade": row["best_trade"],
                "worst_trade": row["worst_trade"],
            }

        return result