from app.agents.base_agent import BaseAgent
from app.strategy_manager.strategy_comparator import StrategyComparator


class StrategyAgent(BaseAgent):

    @property
    def name(self):
        return "Strategy Agent"

    def __init__(self):
        self.comparator = StrategyComparator()

    def analyze(self, artifact):

        results = self.comparator.compare(
            artifact.market_data
        )
        regime = artifact.metadata["market_regime"]

        for strategy in results:

            score = strategy["return_percent"]

            if regime == "Bull Market":
                if strategy["strategy"] == "EMA_MACD":
                    score += 10

            elif regime == "Sideways":
                if strategy["strategy"] == "RSI_REVERSAL":
                    score += 10

            elif regime == "Bear Market":
                if strategy["strategy"] == "RSI_REVERSAL":
                    score += 5

            strategy["strategy_score"] = score

        results.sort(
            key=lambda x: x["strategy_score"],
            reverse=True,
        )

        best = results[0]

        artifact.metadata["preferred_strategy"] = best["strategy"]

        artifact.metadata["strategy_results"] = results

        return artifact