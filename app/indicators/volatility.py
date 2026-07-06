import pandas as pd
import ta

from app.indicators.base_indicator import BaseIndicator


class VolatilityIndicator(BaseIndicator):
    @property
    def name(self) -> str:
        return "Volatility"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        indicator = ta.volatility.BollingerBands(df["close"])

        df["bb_upper"] = indicator.bollinger_hband()

        df["bb_middle"] = indicator.bollinger_mavg()

        df["bb_lower"] = indicator.bollinger_lband()

        df["atr"] = ta.volatility.AverageTrueRange(
            df["high"],
            df["low"],
            df["close"],
        ).average_true_range()

        return df