import pandas as pd

from app.config.logging import logger
from app.config.settings import settings
from app.providers.yahoo_provider import YahooProvider
from app.indicators.engine import IndicatorEngine
from app.features.feature_engine import FeatureEngine


class MarketCollector:

    def __init__(self):
        self.provider = YahooProvider()
        self.engine = IndicatorEngine()
        self.feature_engine = FeatureEngine()

    def collect(
        self,
        symbol: str,
        refresh: bool = False,
    ) -> pd.DataFrame:

        symbol = symbol.upper()
        file = settings.DATA_DIR / f"{symbol}.csv"

        if file.exists() and not refresh:
            logger.info(f"Loading cached data for {symbol}")

            df = pd.read_csv(file)

            df = self.engine.calculate(df)
            df = self.feature_engine.generate(df)
            df = self._clean_market_data(df)

            self.save(symbol, df)

            return df

        logger.info(f"Downloading {symbol}")

        df = self.provider.get_history(
            symbol=symbol,
            period=settings.DEFAULT_PERIOD,
            interval=settings.DEFAULT_INTERVAL,
        )

        logger.info(f"Downloaded {len(df)} rows")

        df = self.engine.calculate(df)
        df = self.feature_engine.generate(df)
        df = self._clean_market_data(df)

        self.save(symbol, df)

        return df

    def save(
        self,
        symbol: str,
        df: pd.DataFrame,
    ):

        symbol = symbol.upper()
        file = settings.DATA_DIR / f"{symbol}.csv"

        df.to_csv(file, index=False)

        logger.info(f"Saved {file}")

        return file

    def load(
        self,
        symbol: str,
    ) -> pd.DataFrame:

        symbol = symbol.upper()
        file = settings.DATA_DIR / f"{symbol}.csv"

        if not file.exists():
            raise FileNotFoundError(
                f"{symbol}.csv not found."
            )

        df = pd.read_csv(file)

        return self._clean_market_data(df)

    def latest_price(
        self,
        symbol: str,
    ) -> float:
        """
        Returns the latest valid cached closing price.
        """

        df = self.load(symbol)

        if "close" not in df.columns:
            raise ValueError(
                f"'close' column missing for {symbol}"
            )

        closes = pd.to_numeric(
            df["close"],
            errors="coerce",
        ).dropna()

        if closes.empty:
            raise ValueError(
                f"No valid close price found for {symbol}"
            )

        return round(
            float(closes.iloc[-1]),
            2,
        )

    def _clean_market_data(
        self,
        df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Cleans market data so downstream APIs never receive invalid prices.
        """

        df = df.copy()

        if "close" not in df.columns:
            return df

        df["close"] = pd.to_numeric(
            df["close"],
            errors="coerce",
        )

        df = df.dropna(
            subset=["close"],
        )

        df = df.reset_index(
            drop=True,
        )

        return df