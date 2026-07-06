from app.agents.base_agent import BaseAgent
from app.core.artifact import ResearchArtifact
from app.utils.scoring import ScoreEngine


class TechnicalAgent(BaseAgent):
    """
    Technical Analysis Agent.
    """

    @property
    def name(self) -> str:
        return "Technical Agent"

    def analyze(self, artifact: ResearchArtifact) -> ResearchArtifact:
        df = artifact.market_data
        latest = df.iloc[-1]

        score = 50
        reasons = []

        if latest["ema20"] > latest["ema50"]:
            score += 15
            reasons.append("EMA20 above EMA50")

        if latest["ema50"] > latest["ema200"]:
            score += 20
            reasons.append("EMA50 above EMA200")

        if 45 <= latest["rsi"] <= 65:
            score += 10
            reasons.append("Healthy RSI")
        elif latest["rsi"] < 30:
            score += 5
            reasons.append("Oversold RSI")
        elif latest["rsi"] > 70:
            score -= 10
            reasons.append("Overbought RSI")

        if latest["macd"] > latest["macd_signal"]:
            score += 15
            reasons.append("MACD Bullish")
        else:
            score -= 10
            reasons.append("MACD Bearish")

        if latest["strong_trend"]:
            score += 10
            reasons.append("Strong ADX Trend")

        if latest["high_volume"]:
            score += 10
            reasons.append("High Trading Volume")

        if latest["near_lower_band"]:
            score += 5
            reasons.append("Near Lower Bollinger Band")

        if latest["near_upper_band"]:
            score -= 5
            reasons.append("Near Upper Bollinger Band")

        score = ScoreEngine.clamp(score)

        if latest["ema20"] > latest["ema50"] > latest["ema200"]:
            trend = "Bullish"
        elif latest["ema20"] < latest["ema50"] < latest["ema200"]:
            trend = "Bearish"
        else:
            trend = "Sideways"

        if score >= 80:
            signal = "BUY"
        elif score >= 60:
            signal = "HOLD"
        else:
            signal = "SELL"

        artifact.scores["technical"] = score
        artifact.metadata["signal"] = signal
        artifact.metadata["trend"] = trend
        artifact.metadata["confidence"] = score
        artifact.metadata["technical_reasons"] = reasons
        artifact.technical.score = score
        artifact.technical.signal = signal
        artifact.technical.trend = trend
        artifact.technical.confidence = score
        artifact.technical.reasons = reasons

        artifact.technical.indicators = {
            "ema20": latest["ema20"],
            "ema50": latest["ema50"],
            "ema200": latest["ema200"],
            "rsi": latest["rsi"],
            "macd": latest["macd"],
            "macd_signal": latest["macd_signal"],
            "adx": latest.get("adx"),
            "atr": latest.get("atr"),
        }

        artifact.technical.features = {
            "price_above_ema20": latest.get("price_above_ema20"),
            "price_above_ema50": latest.get("price_above_ema50"),
            "price_above_ema200": latest.get("price_above_ema200"),
            "rsi_overbought": latest.get("rsi_overbought"),
            "rsi_oversold": latest.get("rsi_oversold"),
            "macd_bullish": latest.get("macd_bullish"),
            "strong_trend": latest.get("strong_trend"),
            "high_volume": latest.get("high_volume"),
        }

        return artifact