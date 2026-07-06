import pandas as pd
import ta

from app.indicators.base_indicator import BaseIndicator


class VolumeIndicator(BaseIndicator):
    @property
    def name(self) -> str:
        return "Volume"

    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:

        df["obv"] = ta.volume.OnBalanceVolumeIndicator(
            df["close"],
            df["volume"],
        ).on_balance_volume()

        return df