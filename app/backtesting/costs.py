class TradingCosts:
    """
    Simple trading cost model.
    """

    def __init__(
        self,
        brokerage_percent: float = 0.03,
        slippage_percent: float = 0.05,
    ):
        self.brokerage_percent = brokerage_percent
        self.slippage_percent = slippage_percent

    def apply_buy_cost(self, price: float) -> float:
        return price * (1 + self.slippage_percent / 100)

    def apply_sell_cost(self, price: float) -> float:
        return price * (1 - self.slippage_percent / 100)

    def brokerage(self, amount: float) -> float:
        return amount * (self.brokerage_percent / 100)