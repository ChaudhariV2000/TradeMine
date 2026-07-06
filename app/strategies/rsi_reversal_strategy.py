import pandas as pd

from app.strategies.base_strategy import BaseStrategy


class RSIReversalStrategy(BaseStrategy):

    @property
    def name(self) -> str:
        return "RSI_REVERSAL"

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df["signal"] = "HOLD"

        buy = df["rsi"] < 30
        sell = df["rsi"] > 60

        df.loc[buy, "signal"] = "BUY"
        df.loc[sell, "signal"] = "SELL"

        return df