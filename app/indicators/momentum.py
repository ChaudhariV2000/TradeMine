import pandas as pd
import ta

from app.indicators.base_indicator import BaseIndicator


class MomentumIndicator(BaseIndicator):
    @property
    def name(self) -> str:
        return "Momentum"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        close = df["close"]

        df["rsi"] = ta.momentum.RSIIndicator(close).rsi()

        df["stoch"] = ta.momentum.StochasticOscillator(
            df["high"],
            df["low"],
            close,
        ).stoch()

        return df