import pandas as pd
import yfinance as yf

from app.providers.base_provider import BaseMarketProvider


class YahooProvider(BaseMarketProvider):

    def get_history(
        self,
        symbol: str,
        period: str = "5y",
        interval: str = "1d",
    ) -> pd.DataFrame:

        ticker = yf.Ticker(f"{symbol}.NS")

        df = ticker.history(
            period=period,
            interval=interval,
            auto_adjust=False,
        )

        if df.empty:
            raise Exception(f"No data found for {symbol}")

        df = df.reset_index()

        df.columns = [c.lower().replace(" ", "_") for c in df.columns]

        return df