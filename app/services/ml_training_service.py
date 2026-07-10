import pandas as pd
from xgboost import XGBClassifier

from app.repositories.trade_feedback_repository import TradeFeedbackRepository
from app.config.settings import settings


class MLTrainingService:
    """
    Trains first ML model using closed trade feedback.
    """

    def __init__(self):
        self.repo = TradeFeedbackRepository()

    def train(self):
        rows = self.repo.all()

        if len(rows) < 30:
            return {
                "status": "NOT_READY",
                "records": len(rows),
                "message": "Need at least 30 closed trade feedback records.",
            }

        data = []

        for r in rows:
            data.append({
                "confidence": r.confidence or 0,
                "technical_score": r.technical_score or 0,
                "news_score": r.news_score or 0,
                "risk_score": r.risk_score or 0,
                "fundamental_score": r.fundamental_score or 0,
                "holding_days": r.holding_days or 0,
                "outcome": 1 if r.outcome == "WIN" else 0,
            })

        df = pd.DataFrame(data)

        X = df[
            [
                "confidence",
                "technical_score",
                "news_score",
                "risk_score",
                "fundamental_score",
                "holding_days",
            ]
        ]

        y = df["outcome"]

        model = XGBClassifier(
            n_estimators=50,
            max_depth=3,
            learning_rate=0.1,
            eval_metric="logloss",
        )

        model.fit(X, y)

        model_file = settings.DATA_DIR / "trademine_ml_model.json"

        model.save_model(str(model_file))

        return {
            "status": "TRAINED",
            "records": len(rows),
            "model_path": str(model_file),
        }