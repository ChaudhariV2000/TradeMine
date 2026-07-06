from app.backtesting.backtester import Backtester
from app.strategy_manager.strategy_manager import StrategyManager


class StrategyComparator:

    def __init__(self):
        self.manager = StrategyManager()
        self.backtester = Backtester()

    def compare(self, df):

        results = []

        for strategy_name in self.manager.list():

            result = self.backtester.run(
                df.copy(),
                strategy_name=strategy_name,
            )

            result["strategy"] = strategy_name

            results.append(result)

        results.sort(
            key=lambda x: x["return_percent"],
            reverse=True,
        )

        if results:
            results[0]["recommendation"] = "BEST"

            for r in results[1:]:
                r["recommendation"] = "GOOD"

        return results