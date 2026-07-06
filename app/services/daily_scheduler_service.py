from app.collectors.market_collector import MarketCollector
from app.services.watchlist_service import WatchlistService
from app.services.trade_exit_service import TradeExitService
from app.services.trading_service import TradingService
from app.services.portfolio_service import PortfolioService
from app.services.trade_cleanup_service import TradeCleanupService


class DailySchedulerService:
    """
    Runs the complete daily TradeMine workflow.
    """

    def __init__(self):
        self.collector = MarketCollector()
        self.watchlist = WatchlistService()
        self.trade_exit_service = TradeExitService()
        self.trading_service = TradingService()
        self.portfolio_service = PortfolioService()
        self.trade_cleanup_service = TradeCleanupService()

    def run(self, scan_function):
        cleanup = self.trade_cleanup_service.close_invalid_trades()

        refreshed = []
        refresh_errors = []

        for symbol in self.watchlist.get_symbols():
            try:
                df = self.collector.collect(
                    symbol.upper(),
                    refresh=True,
                )

                refreshed.append({
                    "symbol": symbol.upper(),
                    "rows": len(df),
                })

            except Exception as e:
                refresh_errors.append({
                    "symbol": symbol.upper(),
                    "error": str(e),
                })

        exits = self.trade_exit_service.check_exits()

        scan_results = scan_function()

        entries = self.trading_service.execute_best_trades(
            scan_results
        )

        portfolio = self.portfolio_service.current_portfolio()

        return {
            "cleanup": cleanup,
            "market_refresh": {
                "symbols_updated": len(refreshed),
                "symbols_failed": len(refresh_errors),
                "updated": refreshed,
                "errors": refresh_errors,
            },
            "trade_exits": exits,
            "trade_entries": entries,
            "portfolio": portfolio,
        }