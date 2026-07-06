from datetime import datetime

from app.database.database import SessionLocal
from app.database.crud import PaperTradeCRUD
from datetime import datetime
import yfinance as yf


class PaperTrader:

    def __init__(self):
        self.db = SessionLocal()

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

        return {
            "id": row.id,
            "symbol": row.symbol,
            "strategy": row.strategy,
            "entry_price": row.entry_price,
            "stop_loss": row.stop_loss,
            "target": row.target,
            "shares": row.shares,
            "status": row.status,
        }

    def list_trades(self):

        rows = PaperTradeCRUD.all(self.db)

        return [
            {
                "id": r.id,
                "symbol": r.symbol,
                "strategy": r.strategy,
                "entry_price": r.entry_price,
                "stop_loss": r.stop_loss,
                "target": r.target,
                "shares": r.shares,
                "status": r.status,
                "entry_date": r.entry_date,
                "exit_price": r.exit_price,
                "exit_date": r.exit_date,
                "pnl": r.pnl,
            }
            for r in rows
        ]
    def update_open_trades(self):

        open_trades = PaperTradeCRUD.open_trades(self.db)

        results = []

        for trade in open_trades:

            ticker = yf.Ticker(f"{trade.symbol}.NS")
            data = ticker.history(period="1d", interval="1d")

            if data.empty:
                results.append({
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "status": "NO_PRICE_DATA",
                })
                continue

            current_price = float(data.iloc[-1]["Close"])

            unrealized_pnl = (
                current_price - trade.entry_price
            ) * trade.shares

            update_data = {}

            if current_price >= trade.target:
                update_data = {
                    "status": "TARGET_HIT",
                    "exit_price": current_price,
                    "exit_date": datetime.now().isoformat(),
                    "pnl": unrealized_pnl,
                }

            elif current_price <= trade.stop_loss:
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

                results.append({
                    "id": updated.id,
                    "symbol": updated.symbol,
                    "status": updated.status,
                    "exit_price": updated.exit_price,
                    "pnl": round(updated.pnl, 2),
                })

            else:
                results.append({
                    "id": trade.id,
                    "symbol": trade.symbol,
                    "status": trade.status,
                    "current_price": round(current_price, 2),
                    "unrealized_pnl": round(unrealized_pnl, 2),
                })

        return results