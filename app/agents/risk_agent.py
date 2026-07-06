import pandas as pd

from app.agents.base_agent import BaseAgent
from app.core.artifact import ResearchArtifact


class RiskAgent(BaseAgent):

    @property
    def name(self) -> str:
        return "Risk Agent"

    def analyze(self, artifact: ResearchArtifact) -> ResearchArtifact:

        df = artifact.market_data.copy()

        returns = df["close"].pct_change().dropna()

        volatility = returns.std() * 100

        latest = df.iloc[-1]
        price = latest["close"]
        atr = latest["atr"]

        stop_loss = round(price - (2 * atr), 2)
        take_profit = round(price + (3 * atr), 2)

        risk = price - stop_loss
        reward = take_profit - price

        risk_reward = round(reward / risk, 2) if risk else 0

        trend_score = 0

        if latest["close"] > latest["ema20"]:
            trend_score += 15

        if latest["close"] > latest["ema50"]:
            trend_score += 20

        if latest["close"] > latest["ema200"]:
            trend_score += 25

        volatility_score = max(0, 40 - volatility * 4)

        risk_score = round(trend_score + volatility_score)

        risk_score = max(0, min(risk_score, 100))

        if risk_score >= 70:
            level = "LOW"

        elif risk_score >= 40:
            level = "MEDIUM"

        else:
            level = "HIGH"

        artifact.scores["risk"] = risk_score

        artifact.metadata["risk_level"] = level

        artifact.metadata["volatility"] = round(volatility, 2)
        artifact.metadata["entry_price"] = round(price, 2)
        artifact.metadata["stop_loss"] = stop_loss
        artifact.metadata["take_profit"] = take_profit
        artifact.metadata["risk_reward"] = risk_reward
        artifact.risk.score = risk_score
        artifact.risk.level = level
        artifact.risk.volatility = volatility

        return artifact