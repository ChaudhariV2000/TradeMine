import yfinance as yf

from app.agents.base_agent import BaseAgent
from app.core.artifact import ResearchArtifact


class FundamentalAgent(BaseAgent):

    @property
    def name(self):
        return "Fundamental Agent"

    def analyze(self, artifact: ResearchArtifact):

        try:

            ticker = yf.Ticker(f"{artifact.symbol}.NS")

            info = ticker.info

            pe = info.get("trailingPE")
            roe = info.get("returnOnEquity")
            debt = info.get("debtToEquity")
            market_cap = info.get("marketCap")

            score = 50

            if pe and pe < 30:
                score += 15

            if roe and roe > 0.15:
                score += 20

            if debt and debt < 100:
                score += 15

            score = max(0, min(score, 100))

            artifact.scores["fundamental"] = score

            artifact.metadata["fundamental"] = {
                "pe": pe,
                "roe": roe,
                "debt_to_equity": debt,
                "market_cap": market_cap,
            }
            artifact.fundamentals.score = score
            artifact.fundamentals.pe = pe
            artifact.fundamentals.roe = roe
            artifact.fundamentals.debt_to_equity = debt
            artifact.fundamentals.market_cap = market_cap
        except Exception:

            artifact.scores["fundamental"] = 50

            artifact.metadata["fundamental"] = {}

        return artifact