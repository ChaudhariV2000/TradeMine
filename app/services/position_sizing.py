import math


class PositionSizing:

    @staticmethod
    def calculate(
        capital: float,
        risk_percent: float,
        entry: float,
        stop_loss: float,
    ):

        values = [capital, risk_percent, entry, stop_loss]

        for value in values:
            if value is None:
                return {
                    "shares": 0,
                    "investment": 0,
                }

            if isinstance(value, float) and math.isnan(value):
                return {
                    "shares": 0,
                    "investment": 0,
                }

        if capital <= 0 or entry <= 0:
            return {
                "shares": 0,
                "investment": 0,
            }

        risk_amount = capital * (risk_percent / 100)
        risk_per_share = abs(entry - stop_loss)

        shares = 0

        if risk_amount > 0 and risk_per_share > 0:
            shares = int(risk_amount / risk_per_share)

        # Hybrid fallback for small accounts:
        # if risk-based sizing gives 0 shares, buy 1 share if affordable.
        if shares <= 0 and capital >= entry:
            shares = 1

        investment = round(shares * entry, 2)

        if investment > capital:
            return {
                "shares": 0,
                "investment": 0,
            }

        return {
            "shares": shares,
            "investment": investment,
        }