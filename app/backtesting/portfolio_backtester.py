from app.backtesting.backtester import Backtester
from app.collectors.market_collector import MarketCollector
from app.services.watchlist_service import WatchlistService


class PortfolioBacktester:

    def __init__(self):
        self.collector = MarketCollector()
        self.backtester = Backtester()
        self.watchlist = WatchlistService()

    def run(self):

        results = []

        for symbol in self.watchlist.get_symbols():

            try:

                df = self.collector.collect(symbol)

                result = self.backtester.run(df)

                result["symbol"] = symbol

                results.append(result)

            except Exception as e:

                results.append({
                    "symbol": symbol,
                    "error": str(e)
                })

        results.sort(
            key=lambda x: x.get("return_percent", -999),
            reverse=True
        )

        return results