from abc import ABC, abstractmethod
import pandas as pd


class BaseMarketProvider(ABC):

    @abstractmethod
    def get_history(
        self,
        symbol: str,
        period: str = "5y",
        interval: str = "1d"
    ) -> pd.DataFrame:
        pass