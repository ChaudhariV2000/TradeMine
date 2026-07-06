import pandas as pd
import ta

from app.indicators.base_indicator import BaseIndicator


class TrendIndicator(BaseIndicator):
    @property
    def name(self) -> str:
        return "Trend"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        close = df["close"]

        df["ema20"] = ta.trend.EMAIndicator(close, window=20).ema_indicator()

        df["ema50"] = ta.trend.EMAIndicator(close, window=50).ema_indicator()

        df["ema200"] = ta.trend.EMAIndicator(close, window=200).ema_indicator()

        macd = ta.trend.MACD(close)

        df["macd"] = macd.macd()
        df["macd_signal"] = macd.macd_signal()
        # ADX
        adx = ta.trend.ADXIndicator(
            high=df["high"],
            low=df["low"],
            close=close,
        )

        df["adx"] = adx.adx()

        # ATR
        atr = ta.volatility.AverageTrueRange(
            high=df["high"],
            low=df["low"],
            close=close,
        )

        df["atr"] = atr.average_true_range()

        # Bollinger Bands
        bb = ta.volatility.BollingerBands(close)

        df["bb_upper"] = bb.bollinger_hband()
        df["bb_lower"] = bb.bollinger_lband()
        df["bb_middle"] = bb.bollinger_mavg()

        # Volume Average
        df["volume_ma20"] = (
            df["volume"]
            .rolling(20)
            .mean()
        )
        return df