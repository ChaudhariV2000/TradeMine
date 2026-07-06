from abc import ABC, abstractmethod
import pandas as pd


class BaseIndicator(ABC):
    """
    Base class for all technical indicators.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique indicator name."""
        ...

    @abstractmethod
    def calculate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate indicator values and return updated DataFrame."""
        ...