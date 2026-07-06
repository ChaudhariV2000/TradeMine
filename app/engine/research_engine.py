from app.collectors.market_collector import MarketCollector
from app.core.artifact import ResearchArtifact
from app.managers.agent_manager import AgentManager
from app.config.settings import settings
from app.repositories.decision_journal_repository import (
    DecisionJournalRepository,
)


class ResearchEngine:

    def __init__(self):
        self.collector = MarketCollector()
        self.agent_manager = AgentManager()
        self.decision_repo = DecisionJournalRepository()

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
        try:
            self.decision_repo.save(artifact)
        except Exception as e:
            print(f"Decision Journal Error: {e}")

        return artifact