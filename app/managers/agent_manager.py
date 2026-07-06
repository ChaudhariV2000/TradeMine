from app.agents.market_regime_agent import MarketRegimeAgent
from app.agents.decision_agent import DecisionAgent
from app.agents.technical_agent import TechnicalAgent
from app.agents.news_agent import NewsAgent
from app.agents.risk_agent import RiskAgent
from app.core.artifact import ResearchArtifact
from app.agents.fundamental_agent import FundamentalAgent
from app.agents.strategy_agent import StrategyAgent

class AgentManager:
    """
    Executes all research agents in sequence.
    """

    def __init__(self):

        self.agents = [
            TechnicalAgent(),
            NewsAgent(),
            RiskAgent(),
            FundamentalAgent(),
            MarketRegimeAgent(),
            StrategyAgent(),
            DecisionAgent(),
        ]

    def run(self, artifact: ResearchArtifact) -> ResearchArtifact:

        for agent in self.agents:
            artifact = agent.analyze(artifact)

        return artifact

    def list_agents(self):

        return [agent.name for agent in self.agents]