from datetime import datetime
import math
from app.collectors.market_collector import MarketCollector
from app.database.database import SessionLocal
from app.database.models import PaperTrade
from app.portfolio.portfolio_engine import PortfolioEngine
from app.repositories.settings_repository import SettingsRepository


class PortfolioService:
    """
    Builds actual portfolio view from open paper trades.
    """

    def __init__(self):
        self.db = SessionLocal()
        self.settings_repo = SettingsRepository()
        self.engine = PortfolioEngine()
        self.collector = MarketCollector()

    def _is_current_month(self, date_text: str) -> bool:
        if not date_text:
            return False

        try:
            trade_date = datetime.fromisoformat(date_text)
            now = datetime.now()

            return (
                trade_date.year == now.year
                and trade_date.month == now.month
            )
        except Exception:
            return False

    def current_portfolio(self):
        settings = self.settings_repo.get_settings()
        monthly_budget = settings.monthly_budget

        open_trades = (
            self.db.query(PaperTrade)
            .filter(PaperTrade.status == "OPEN")
            .all()
        )

        holdings = []

        total_investment = 0
        total_current_value = 0
        current_month_used = 0

        for trade in open_trades:
            current_price = self.collector.latest_price(trade.symbol)
            if current_price is None or math.isnan(float(current_price)):
                continue

            investment = round(
                trade.entry_price * trade.shares,
                2,
            )

            current_value = round(
                current_price * trade.shares,
                2,
            )

            pnl = round(
                current_value - investment,
                2,
            )

            pnl_percent = round(
                (pnl / investment) * 100,
                2,
            ) if investment else 0

            total_investment += investment
            total_current_value += current_value

            if self._is_current_month(trade.entry_date):
                current_month_used += investment

            holdings.append({
                "id": trade.id,
                "symbol": trade.symbol,
                "strategy": trade.strategy,
                "quantity": trade.shares,

                "entry_price": trade.entry_price,
                "current_price": current_price,

                "investment": investment,
                "current_value": current_value,

                "pnl": pnl,
                "pnl_percent": pnl_percent,

                "stop_loss": trade.stop_loss,
                "target": trade.target,

                "status": trade.status,
                "entry_date": trade.entry_date,
            })

        total_investment = round(total_investment, 2)
        total_current_value = round(total_current_value, 2)
        current_month_used = round(current_month_used, 2)

        unrealized_pnl = round(
            total_current_value - total_investment,
            2,
        )

        return_percent = round(
            (unrealized_pnl / total_investment) * 100,
            2,
        ) if total_investment else 0

        cash_available = round(
            max(monthly_budget - current_month_used, 0),
            2,
        )

        return {
            "summary": {
                "monthly_budget": monthly_budget,
                "current_month_used": current_month_used,
                "cash": cash_available,

                "invested": total_investment,
                "current_value": total_current_value,
                "unrealized_pnl": unrealized_pnl,
                "return_percent": return_percent,

                "positions": len(holdings),
            },
            "holdings": holdings,
        }

    def build(self, scan_results, capital=100000):
        candidates = [
            s for s in scan_results
            if s.get("recommendation") in ["STRONG BUY", "BUY", "WATCH", "HOLD"]
            and s.get("confidence", 0) >= 55
            and "price" in s
        ]

        candidates.sort(
            key=lambda x: x.get("confidence", 0),
            reverse=True,
        )

        candidates = candidates[:5]

        if not candidates:
            return {
                "capital": capital,
                "investment": 0,
                "cash_remaining": capital,
                "stocks": [],
                "message": "No suitable portfolio candidates found today.",
            }

        total_confidence = sum(
            s.get("confidence", 0)
            for s in candidates
        )

        portfolio = []
        invested = 0

        for stock in candidates:
            weight = stock["confidence"] / total_confidence
            allocation = round(capital * weight, 2)

            shares = int(allocation / stock["price"])

            if shares <= 0:
                continue

            investment = round(shares * stock["price"], 2)
            invested += investment

            portfolio.append({
                "symbol": stock["symbol"],
                "recommendation": stock["recommendation"],
                "confidence": stock["confidence"],
                "allocation": allocation,
                "investment": investment,
                "shares": shares,
                "price": stock["price"],
                "weight": round(weight * 100, 2),
            })

        return {
            "capital": capital,
            "investment": round(invested, 2),
            "cash_remaining": round(capital - invested, 2),
            "stocks": portfolio,
        }