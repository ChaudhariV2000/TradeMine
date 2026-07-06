class CommitteeEngine:

    def vote(self, artifact):

        votes = []

        # Technical
        technical = artifact.metadata["signal"]

        votes.append({
            "agent": "Technical",
            "vote": technical
        })

        # News
        news = artifact.metadata["news_sentiment"]

        if news == "Positive":
            news_vote = "BUY"

        elif news == "Negative":
            news_vote = "SELL"

        else:
            news_vote = "HOLD"

        votes.append({
            "agent": "News",
            "vote": news_vote
        })

        # Fundamentals

        if artifact.scores["fundamental"] >= 70:
            fundamental_vote = "BUY"
        else:
            fundamental_vote = "HOLD"

        votes.append({
            "agent": "Fundamental",
            "vote": fundamental_vote
        })

        # Risk

        if artifact.metadata["risk_level"] == "LOW":
            risk_vote = "BUY"

        elif artifact.metadata["risk_level"] == "HIGH":
            risk_vote = "SELL"

        else:
            risk_vote = "HOLD"

        votes.append({
            "agent": "Risk",
            "vote": risk_vote
        })

        return votes