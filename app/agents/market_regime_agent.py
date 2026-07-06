from app.agents.base_agent import BaseAgent
from app.core.artifact import ResearchArtifact


class MarketRegimeAgent(BaseAgent):

    @property
    def name(self):
        return "Market Regime Agent"

    def analyze(self, artifact: ResearchArtifact):

        latest = artifact.market_data.iloc[-1]

        # Trend
        if latest["ema20"] > latest["ema50"] > latest["ema200"]:
            regime = "Bull Market"

        elif latest["ema20"] < latest["ema50"] < latest["ema200"]:
            regime = "Bear Market"

        else:
            regime = "Sideways"

        # Volatility
        atr_percent = (
            latest["atr"] / latest["close"]
        ) * 100

        if atr_percent > 3:
            volatility = "High"

        elif atr_percent < 1:
            volatility = "Low"

        else:
            volatility = "Normal"

        artifact.metadata["market_regime"] = regime
        artifact.metadata["market_volatility"] = volatility

        return artifact