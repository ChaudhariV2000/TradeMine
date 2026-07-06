from app.engine.research_engine import ResearchEngine
from app.paper_trading.paper_trader import PaperTrader
from app.repositories.settings_repository import SettingsRepository
from app.services.position_sizing import PositionSizing
from app.services.portfolio_service import PortfolioService


class TradingEngine:
    """
    Central execution layer for paper trading decisions.
    """

    def __init__(self):
        self.research_engine = ResearchEngine()
        self.paper_trader = PaperTrader()
        self.settings_repo = SettingsRepository()
        self.position_sizing = PositionSizing()
        self.portfolio_service = PortfolioService()

    def execute_paper_trade(self, symbol: str):
        symbol = symbol.upper()

        settings = self.settings_repo.get_settings()

        artifact = self.research_engine.analyze(symbol)

        decision = artifact.metadata["decision"]
        recommendation = decision["recommendation"]
        confidence = decision["confidence"]

        if recommendation not in ["STRONG BUY", "BUY"]:
            return {
                "symbol": symbol,
                "status": "SKIPPED",
                "reason": f"Decision is {recommendation}",
                "confidence": confidence,
            }

        portfolio = self.portfolio_service.current_portfolio()
        holdings = portfolio["holdings"]
        summary = portfolio["summary"]

        available_cash = summary["cash"]

        position = self.position_sizing.calculate(
            capital=available_cash,
            risk_percent=1,
            entry=artifact.metadata["entry_price"],
            stop_loss=artifact.metadata["stop_loss"],
        )

        if position["shares"] <= 0:
            return {
                "symbol": symbol,
                "status": "SKIPPED",
                "reason": "Available cash too small for this trade setup",
                "available_cash": available_cash,
            }

        portfolio_check = self.portfolio_service.engine.can_buy(
            symbol=symbol,
            holdings=holdings,
            available_cash=available_cash,
            investment_required=position["investment"],
            capital=settings.monthly_budget,
            max_positions=settings.max_positions,
        )

        if not portfolio_check["allowed"]:
            return {
                "symbol": symbol,
                "status": "SKIPPED",
                "reason": portfolio_check["reason"],
                "confidence": confidence,
            }

        trade = self.paper_trader.open_trade({
            "symbol": symbol,
            "strategy": artifact.metadata["preferred_strategy"],
            "entry_price": artifact.metadata["entry_price"],
            "stop_loss": artifact.metadata["stop_loss"],
            "target": artifact.metadata["take_profit"],
            "shares": position["shares"],
        })

        return {
            "status": "OPENED",
            "decision": recommendation,
            "confidence": confidence,
            "investment": position["investment"],
            "trade": trade,
        }

    def open_best_paper_trades(self, scan_results: list[dict]):
        settings = self.settings_repo.get_settings()

        candidates = [
            s for s in scan_results
            if s.get("recommendation") in ["STRONG BUY", "BUY"]
        ]

        candidates.sort(
            key=lambda x: x.get("confidence", 0),
            reverse=True,
        )

        opened = []
        skipped = []

        for stock in candidates:
            result = self.execute_paper_trade(stock["symbol"])

            if result.get("status") == "OPENED":
                opened.append({
                    **result["trade"],
                    "investment": result["investment"],
                    "confidence": result["confidence"],
                })
            else:
                skipped.append({
                    "symbol": stock["symbol"],
                    "reason": result.get("reason"),
                })

        portfolio = self.portfolio_service.current_portfolio()

        return {
            "monthly_budget": settings.monthly_budget,
            "current_month_used": portfolio["summary"]["current_month_used"],
            "cash_available": portfolio["summary"]["cash"],
            "opened": opened,
            "skipped": skipped,
            "total_opened": len(opened),
        }