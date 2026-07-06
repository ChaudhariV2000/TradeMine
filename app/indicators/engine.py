import pandas as pd

from app.indicators.momentum import MomentumIndicator
from app.indicators.trend import TrendIndicator
from app.indicators.volatility import VolatilityIndicator
from app.indicators.volume import VolumeIndicator


class IndicatorEngine:

    def __init__(self):

        self.indicators = [
            TrendIndicator(),
            MomentumIndicator(),
            VolatilityIndicator(),
            VolumeIndicator(),
        ]

    def calculate(self, df: pd.DataFrame):

        for indicator in self.indicators:
            df = indicator.calculate(df)

        return df