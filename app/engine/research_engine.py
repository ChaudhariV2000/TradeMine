from app.collectors.market_collector import MarketCollector
from app.core.artifact import ResearchArtifact
from app.managers.agent_manager import AgentManager
from app.config.settings import settings
from app.repositories.decision_journal_repository import (
    DecisionJournalRepository,
)
from app.services.ml_prediction_service import MLPredictionService


class ResearchEngine:

    def __init__(self):
        self.collector = MarketCollector()
        self.agent_manager = AgentManager()
        self.decision_repo = DecisionJournalRepository()
        self.ml_prediction = MLPredictionService()

    def analyze(self, symbol: str, refresh: bool = False):

        df = self.collector.collect(
            symbol,
            refresh=refresh,
        )

        artifact = ResearchArtifact(
            symbol=symbol,
            timeframe=settings.DEFAULT_PERIOD,
            market_data=df,
        )

        artifact = self.agent_manager.run(artifact)

        decision = artifact.metadata["decision"]

        ml_prediction = self.ml_prediction.predict(
            confidence=decision["confidence"],
            technical_score=artifact.scores["technical"],
            news_score=artifact.scores["news"],
            risk_score=artifact.scores["risk"],
            fundamental_score=artifact.scores["fundamental"],
            holding_days=5,
        )

        artifact.metadata["ml_prediction"] = ml_prediction

        rule_confidence = decision["confidence"]

        if ml_prediction.get("status") == "READY":
            hybrid_score = round(
                (rule_confidence * 0.6)
                + (ml_prediction["success_probability"] * 0.4),
                2,
            )
        else:
            hybrid_score = rule_confidence

        artifact.metadata["hybrid_score"] = hybrid_score

        if hybrid_score >= 90:
            hybrid_recommendation = "STRONG BUY"
        elif hybrid_score >= 75:
            hybrid_recommendation = "BUY"
        elif hybrid_score >= 60:
            hybrid_recommendation = "WATCH"
        elif hybrid_score >= 45:
            hybrid_recommendation = "HOLD"
        else:
            hybrid_recommendation = "SELL"

        artifact.metadata["hybrid_decision"] = {
            "recommendation": hybrid_recommendation,
            "confidence": hybrid_score,
        }

        try:
            self.decision_repo.save(artifact)
        except Exception as e:
            print(f"Decision Journal Error: {e}")

        return artifact