class EquityCurve:

    def __init__(self):
        self.values = []

    def add(self, capital):
        self.values.append(round(capital, 2))

    def get(self):
        return self.values