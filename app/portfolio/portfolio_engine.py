class PortfolioEngine:
    """
    Portfolio intelligence and calculations.
    """

    def has_position(self, holdings, symbol):
        return any(h["symbol"] == symbol for h in holdings)

    def available_cash(self, capital, invested):
        return round(capital - invested, 2)

    def portfolio_summary(self, holdings, capital):
        invested = sum(h["investment"] for h in holdings)

        return {
            "capital": capital,
            "invested": round(invested, 2),
            "cash": self.available_cash(capital, invested),
            "positions": len(holdings),
        }

    def can_buy(
        self,
        symbol: str,
        holdings: list,
        available_cash: float,
        investment_required: float,
        capital: float,
        max_positions: int = 5,
        max_allocation_percent: float = 30,
    ):
        if self.has_position(holdings, symbol):
            return {
                "allowed": False,
                "reason": "Already in portfolio",
            }

        if len(holdings) >= max_positions:
            return {
                "allowed": False,
                "reason": "Maximum portfolio positions reached",
            }

        if investment_required > available_cash:
            return {
                "allowed": False,
                "reason": "Insufficient cash",
            }

        allocation_percent = (investment_required / capital) * 100

        if allocation_percent > max_allocation_percent:
            return {
                "allowed": False,
                "reason": f"Allocation exceeds {max_allocation_percent}% limit",
            }

        return {
            "allowed": True,
            "reason": "Portfolio check passed",
        }