import pandas as pd


class DatasetBuilder:

    def build(self, df: pd.DataFrame) -> pd.DataFrame:

        dataset = df.copy()
        dataset["technical_score"] = 0
        dataset["news_score"] = 0
        dataset["risk_score"] = 0   
        dataset["fundamental_score"] = 0

        # Future 5-day return
        dataset["future_return"] = (
            dataset["close"].shift(-5) - dataset["close"]
        ) / dataset["close"]

        # Target:
        # 1 = Buy
        # 0 = Hold/Sell
        dataset["target"] = (
            dataset["future_return"] > 0.03
        ).astype(int)

        dataset = dataset.dropna()

        return dataset
    def enrich(
    self,
    artifact,
    dataset,
    ):
        dataset["technical_score"] = artifact.scores["technical"]
        dataset["news_score"] = artifact.scores["news"]
        dataset["risk_score"] = artifact.scores["risk"]
        dataset["fundamental_score"] = artifact.scores["fundamental"]