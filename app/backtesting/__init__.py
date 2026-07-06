class Backtester:

    def __init__(self):
        self.strategy = EMAMACDStrategy()

    def run(self, df: pd.DataFrame):
        ...