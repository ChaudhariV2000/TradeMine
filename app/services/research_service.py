from app.engine.research_engine import ResearchEngine


class ResearchService:

    def __init__(self):
        self.engine = ResearchEngine()

    def analyze(self, symbol: str, refresh=False):
        return self.engine.analyze(
            symbol,
            refresh=refresh,
        )