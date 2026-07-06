class DrawdownCalculator:

    @staticmethod
    def calculate(equity_curve):

        if not equity_curve:
            return 0

        peak = equity_curve[0]
        max_drawdown = 0

        for value in equity_curve:

            if value > peak:
                peak = value

            drawdown = ((peak - value) / peak) * 100

            if drawdown > max_drawdown:
                max_drawdown = drawdown

        return round(max_drawdown, 2)