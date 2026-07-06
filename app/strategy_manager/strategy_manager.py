from app.strategies.ema_macd_strategy import EMAMACDStrategy
from app.strategies.rsi_reversal_strategy import RSIReversalStrategy

class StrategyManager:
    """
    Manages all trading strategies.
    """

    def __init__(self):

        self.strategies = {
            "EMA_MACD": EMAMACDStrategy(),
            "RSI_REVERSAL": RSIReversalStrategy(),
        }

    def get(self, name: str):

        if name not in self.strategies:
            raise ValueError(f"Unknown strategy: {name}")

        return self.strategies[name]

    def list(self):

        return list(self.strategies.keys())