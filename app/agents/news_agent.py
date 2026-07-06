import feedparser
import yfinance as yf
from urllib.parse import quote_plus

from app.agents.base_agent import BaseAgent
from app.core.artifact import ResearchArtifact


class NewsAgent(BaseAgent):
    """
    Collects recent stock news and calculates simple sentiment.
    """

    @property
    def name(self) -> str:
        return "News Agent"

    def analyze(self, artifact: ResearchArtifact) -> ResearchArtifact:
        headlines = self._get_yahoo_news(artifact.symbol)

        if not headlines:
            headlines = self._get_google_news(artifact.symbol)

        score, sentiment = self._score_sentiment(headlines)

        artifact.scores["news"] = score
        artifact.metadata["news_sentiment"] = sentiment
        artifact.metadata["news_confidence"] = 60 if headlines else 30
        artifact.metadata["news_headlines"] = headlines
        artifact.news.score = score
        artifact.news.sentiment = sentiment
        artifact.news.confidence = artifact.metadata["news_confidence"]
        artifact.news.headlines = headlines

        return artifact

    def _get_yahoo_news(self, symbol: str) -> list[str]:
        try:
            ticker = yf.Ticker(f"{symbol}.NS")
            news_items = ticker.news or []

            headlines = []
            for item in news_items[:5]:
                title = item.get("title")
                if title:
                    headlines.append(title)

            return headlines

        except Exception:
            return []

    def _get_google_news(self, symbol: str) -> list[str]:
        try:
            query = quote_plus(f"{symbol} stock India")
            url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

            feed = feedparser.parse(url)

            headlines = []
            for entry in feed.entries[:5]:
                headlines.append(entry.title)

            return headlines

        except Exception:
            return []

    def _score_sentiment(self, headlines: list[str]) -> tuple[int, str]:
        if not headlines:
            return 50, "Neutral"

        positive_words = [
            "profit", "growth", "beats", "gain", "strong",
            "rises", "surge", "upgrade", "record", "rally"
        ]

        negative_words = [
            "loss", "fall", "drops", "weak", "decline",
            "downgrade", "probe", "fraud", "concern", "slump",
            "crash", "plunge", "plunges", "worst", "shock",
            "disruption", "low", "lows"
        ]

        text = " ".join(headlines).lower()

        positive_count = sum(word in text for word in positive_words)
        negative_count = sum(word in text for word in negative_words)

        if positive_count > negative_count:
            return 70, "Positive"

        if negative_count > positive_count:
            return 30, "Negative"

        return 50, "Neutral"