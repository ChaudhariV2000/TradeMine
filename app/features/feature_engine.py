import pandas as pd


class FeatureEngine:
    """
    Generates engineered features from market data.
    """

    def generate(self, df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()

        # Daily return
        df["daily_return"] = df["close"].pct_change()

        # 5-day return
        df["return_5d"] = df["close"].pct_change(5)

        # 20-day return
        df["return_20d"] = df["close"].pct_change(20)

        # Price vs EMA
        df["price_above_ema20"] = df["close"] > df["ema20"]
        df["price_above_ema50"] = df["close"] > df["ema50"]
        df["price_above_ema200"] = df["close"] > df["ema200"]

        # RSI States
        df["rsi_overbought"] = df["rsi"] > 70
        df["rsi_oversold"] = df["rsi"] < 30

        # MACD State
        df["macd_bullish"] = df["macd"] > df["macd_signal"]
        df["strong_trend"] = df["adx"] > 25

        df["high_volume"] = (
            df["volume"] > df["volume_ma20"]
        )

        df["near_upper_band"] = (
            df["close"] >= df["bb_upper"]
        )

        df["near_lower_band"] = (
            df["close"] <= df["bb_lower"]
        )

        return df