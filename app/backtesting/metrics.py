from app.backtesting.models import Trade


class MetricsCalculator:

    @staticmethod
    def calculate(trades: list[Trade]):

        if not trades:
            return {
                "total_trades": 0,
                "winning_trades": 0,
                "losing_trades": 0,
                "win_rate": 0,
                "average_profit": 0,
                "average_loss": 0,
                "best_trade": 0,
                "worst_trade": 0,
            }

        winners = [t for t in trades if t.pnl > 0]
        losers = [t for t in trades if t.pnl <= 0]

        avg_profit = (
            sum(t.pnl for t in winners) / len(winners)
            if winners else 0
        )

        avg_loss = (
            sum(t.pnl for t in losers) / len(losers)
            if losers else 0
        )
        average_holding_days = round(
            sum(t.holding_days for t in trades) / len(trades),
            2,
        )

        return {
            "total_trades": len(trades),
            "winning_trades": len(winners),
            "losing_trades": len(losers),
            "win_rate": round(len(winners) / len(trades) * 100, 2),
            "average_profit": round(avg_profit, 2),
            "average_loss": round(avg_loss, 2),
            "best_trade": round(max((t.pnl for t in trades), default=0), 2),
            "worst_trade": round(min((t.pnl for t in trades), default=0), 2),
            "average_holding_days": average_holding_days,
        }