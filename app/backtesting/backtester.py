import pandas as pd

from app.backtesting.costs import TradingCosts
from app.backtesting.equity_curve import EquityCurve
from app.backtesting.metrics import MetricsCalculator
from app.backtesting.models import Trade
from app.strategy_manager.strategy_manager import StrategyManager
from app.backtesting.charts import BacktestChart
from app.backtesting.drawdown import DrawdownCalculator
class Backtester:
    """
    Long-only backtesting engine with costs and equity curve.
    """

    def __init__(self):
        self.strategy_manager = StrategyManager()
        self.costs = TradingCosts()

    def run(self, df: pd.DataFrame, strategy_name: str = "EMA_MACD"):
        strategy = self.strategy_manager.get(strategy_name)
        df = strategy.generate_signals(df)

        initial_capital = 100000.0
        cash = initial_capital
        shares = 0.0

        curve = EquityCurve()
        curve.add(cash)

        completed_trades = []

        entry_price = None
        entry_date = None

        for _, row in df.iterrows():

            if shares == 0 and row["signal"] == "BUY":
                entry_price = self.costs.apply_buy_cost(float(row["close"]))
                entry_date = str(row["date"])

                brokerage = self.costs.brokerage(cash)
                usable_cash = cash - brokerage

                shares = usable_cash / entry_price
                cash = 0.0

            elif shares > 0 and row["signal"] == "SELL":
                exit_price = self.costs.apply_sell_cost(float(row["close"]))
                exit_date = str(row["date"])

                gross_cash = shares * exit_price
                brokerage = self.costs.brokerage(gross_cash)
                cash = gross_cash - brokerage

                pnl = cash - (shares * entry_price)

                return_percent = (
                    (exit_price - entry_price) / entry_price
                ) * 100

                holding_days = (
                    pd.to_datetime(exit_date)
                    - pd.to_datetime(entry_date)
                ).days

                completed_trades.append(
                    Trade(
                        entry_date=entry_date,
                        exit_date=exit_date,
                        entry_price=entry_price,
                        exit_price=exit_price,
                        quantity=shares,
                        pnl=pnl,
                        return_percent=return_percent,
                        holding_days=holding_days,
                    )
                )

                shares = 0.0
                entry_price = None
                entry_date = None

                curve.add(cash)

        if shares > 0:
            exit_price = self.costs.apply_sell_cost(float(df.iloc[-1]["close"]))
            exit_date = str(df.iloc[-1]["date"])

            gross_cash = shares * exit_price
            brokerage = self.costs.brokerage(gross_cash)
            cash = gross_cash - brokerage

            pnl = cash - (shares * entry_price)

            return_percent = (
                (exit_price - entry_price) / entry_price
            ) * 100

            holding_days = (
                pd.to_datetime(exit_date)
                - pd.to_datetime(entry_date)
            ).days

            completed_trades.append(
                Trade(
                    entry_date=entry_date,
                    exit_date=exit_date,
                    entry_price=entry_price,
                    exit_price=exit_price,
                    quantity=shares,
                    pnl=pnl,
                    return_percent=return_percent,
                    holding_days=holding_days,
                )
            )

            curve.add(cash)

        total_return = ((cash - initial_capital) / initial_capital) * 100
        metrics = MetricsCalculator.calculate(completed_trades)
        max_drawdown = DrawdownCalculator.calculate(
            curve.get()
        )
        chart = BacktestChart.equity_curve(
            curve.get(),
            strategy_name,
        )

        return {
            "initial_capital": initial_capital,
            "final_capital": round(cash, 2),
            "return_percent": round(total_return, 2),
            **metrics,
            "equity_curve": curve.get(),
            "max_drawdown": max_drawdown,
            "equity_curve_chart": chart,
        }