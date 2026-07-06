from datetime import datetime

from app.collectors.market_collector import MarketCollector
from app.database.database import SessionLocal
from app.database.models import PaperTrade


class TradeExitService:
    """
    Checks open paper trades and closes them if target or stop-loss is hit.
    """

    def __init__(self):
        self.db = SessionLocal()
        self.collector = MarketCollector()

    def check_exits(self):
        open_trades = (
            self.db.query(PaperTrade)
            .filter(PaperTrade.status == "OPEN")
            .all()
        )

        closed = []
        still_open = []
        errors = []

        for trade in open_trades:
            try:
                if trade.shares <= 0:
                    errors.append({
                        "id": trade.id,
                        "symbol": trade.symbol,
                        "error": "Invalid share quantity",
                    })
                    continue

                current_price = self.collector.latest_price(trade.symbol)

                if current_price <= trade.stop_loss:
                    pnl = round(
                        (current_price - trade.entry_price) * trade.shares,
                        2,
                    )

                    trade.status = "STOP_LOSS_HIT"
                    trade.exit_price = current_price
                    trade.exit_date = datetime.now().isoformat()
                    trade.pnl = pnl

                    self.db.commit()

                    closed.append({
                        "id": trade.id,
                        "symbol": trade.symbol,
                        "reason": "STOP_LOSS",
                        "entry_price": trade.entry_price,
                        "exit_price": current_price,
                        "shares": trade.shares,
                        "pnl": pnl,
                    })

                elif current_price >= trade.target:
                    pnl = round(
                        (current_price - trade.entry_price) * trade.shares,
                        2,
                    )

                    trade.status = "TARGET_HIT"
                    trade.exit_price = current_price
                    trade.exit_date = datetime.now().isoformat()
                    trade.pnl = pnl

                    self.db.commit()

                    closed.append({
                        "id": trade.id,
                        "symbol": trade.symbol,
                        "reason": "TARGET",
                        "entry_price": trade.entry_price,
                        "exit_price": current_price,
                        "shares": trade.shares,
                        "pnl": pnl,
                    })

                else:
                    still_open.append({
                        "id": trade.id,
                        "symbol": trade.symbol,
                        "current_price": current_price,
                        "stop_loss": trade.stop_loss,
                        "target": trade.target,
                        "unrealized_pnl": round(
                            (current_price - trade.entry_price) * trade.shares,
                            2,
                        ),
                    })

            except Exception as e:
                errors.append({
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "error": str(e),
                })

        return {
            "checked": len(open_trades),
            "closed_count": len(closed),
            "still_open_count": len(still_open),
            "closed": closed,
            "still_open": still_open,
            "errors": errors,
        }