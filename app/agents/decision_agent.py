from app.agents.base_agent import BaseAgent
from app.committee.committee_engine import CommitteeEngine


class DecisionAgent(BaseAgent):

    def __init__(self):
        self.committee = CommitteeEngine()

    @property
    def name(self):
        return "Decision Agent"

    def analyze(self, artifact):

        votes = self.committee.vote(artifact)

        buy_count = len([v for v in votes if v["vote"] == "BUY"])
        hold_count = len([v for v in votes if v["vote"] == "HOLD"])
        sell_count = len([v for v in votes if v["vote"] == "SELL"])

        technical = artifact.scores["technical"]
        news = artifact.scores["news"]
        risk = artifact.scores["risk"]
        fundamental = artifact.scores["fundamental"]

        regime = artifact.metadata.get("market_regime", "Sideways")
        volatility = artifact.metadata.get("market_volatility", "Normal")
        risk_level = artifact.metadata.get("risk_level", "MEDIUM")

        overall = (
            technical * 0.30
            + news * 0.15
            + risk * 0.20
            + fundamental * 0.35
        )

        overall = round(overall)

        reasons = []

        if buy_count >= 3:
            overall += 5
            reasons.append("Majority committee vote is bullish")

        if sell_count >= 2:
            overall -= 10
            reasons.append("Multiple agents are warning against trade")

        if regime == "Bull Market":
            overall += 5
            reasons.append("Bull market supports buying")

        elif regime == "Bear Market":
            overall -= 10
            reasons.append("Bear market reduces confidence")

        if volatility == "High":
            overall -= 5
            reasons.append("High volatility reduces confidence")

        if risk_level == "HIGH":
            overall -= 10
            reasons.append("High risk reduces confidence")

        if technical >= 80:
            reasons.append("Strong technical structure")

        if news >= 60:
            reasons.append("Positive market sentiment")

        if risk >= 70:
            reasons.append("Low investment risk")

        if fundamental >= 70:
            reasons.append("Strong company fundamentals")

        overall = max(0, min(100, overall))

        if overall >= 80:
            recommendation = "STRONG BUY"
        elif overall >= 65:
            recommendation = "BUY"
        elif overall >= 50:
            recommendation = "HOLD"
        else:
            recommendation = "AVOID"

        if regime == "Bear Market" and risk_level == "HIGH":
            if recommendation in ["STRONG BUY", "BUY"]:
                recommendation = "HOLD"
                reasons.append(
                    "Downgraded because bear market and high risk are both present"
                )

        artifact.metadata["committee"] = votes

        artifact.metadata["decision"] = {
            "recommendation": recommendation,
            "confidence": overall,
            "reasoning": reasons,
            "votes": {
                "buy": buy_count,
                "hold": hold_count,
                "sell": sell_count,
            },
        }

        return artifact