from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class BacktestChart:

    @staticmethod
    def equity_curve(curve, symbol):

        reports = Path("reports")
        reports.mkdir(exist_ok=True)

        plt.figure(figsize=(10,5))

        plt.plot(curve)

        plt.title(f"{symbol} Equity Curve")

        plt.xlabel("Trades")

        plt.ylabel("Capital")

        plt.grid(True)

        file = reports / f"{symbol}_equity_curve.png"

        plt.savefig(file)

        plt.close()

        return str(file)