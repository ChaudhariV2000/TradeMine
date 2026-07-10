import pandas as pd
from xgboost import XGBClassifier

from app.config.settings import settings


class MLPredictionService:

    def __init__(self):
        self.model_file = settings.DATA_DIR / "trademine_ml_model.json"

    def _load_model(self):
        if not self.model_file.exists():
            return None

        model = XGBClassifier()
        model.load_model(str(self.model_file))

        return model

    def predict(
        self,
        confidence,
        technical_score,
        news_score,
        risk_score,
        fundamental_score,
        holding_days,
    ):
        model = self._load_model()

        if model is None:
            return {
                "status": "NOT_READY",
                "message": "ML model not trained yet. Run POST /learning/train after enough feedback records exist.",
            }

        df = pd.DataFrame([{
            "confidence": confidence,
            "technical_score": technical_score,
            "news_score": news_score,
            "risk_score": risk_score,
            "fundamental_score": fundamental_score,
            "holding_days": holding_days,
        }])

        probability = model.predict_proba(df)[0][1]

        return {
            "status": "READY",
            "success_probability": round(float(probability) * 100, 2),
        }