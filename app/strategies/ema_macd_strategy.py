import pandas as pd

from app.strategies.base_strategy import BaseStrategy


class EMAMACDStrategy(BaseStrategy):

    @property
    def name(self) -> str:
        return "EMA + MACD Strategy"

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        df["signal"] = "HOLD"

        buy = (
            (df["ema20"] > df["ema50"]) &
            (df["macd"] > df["macd_signal"])
        )

        sell = (
            df["ema20"] < df["ema50"]
        )

        df.loc[buy, "signal"] = "BUY"
        df.loc[sell, "signal"] = "SELL"

        return df