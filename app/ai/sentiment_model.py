from transformers import pipeline


class SentimentModel:

    def __init__(self):
        self.model = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
        )

    def analyze(self, text: str):

        if not text:
            return {
                "score": 50,
                "sentiment": "Neutral",
                "confidence": 0,
            }

        result = self.model(text[:512])[0]

        label = result["label"]
        confidence = round(result["score"] * 100)

        if label == "POSITIVE":
            sentiment = "Positive"
            score = 70
        else:
            sentiment = "Negative"
            score = 30

        return {
            "score": score,
            "sentiment": sentiment,
            "confidence": confidence,
        }