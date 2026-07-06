class RankingService:
    """
    Combines technical analysis, historical performance,
    win rate, and news sentiment into one score.
    """

    @staticmethod
    def calculate_overall_score(
    technical_score,
    return_percent,
    win_rate,
    news_score,
    risk_score,
    )-> int:

        return_score = max(0, min(return_percent, 100))
        win_rate_score = max(0, min(win_rate, 100))
        news_score = max(0, min(news_score, 100))
        risk_score = max(0, min(risk_score, 100))

        overall = (
            technical_score * 0.35
            + return_score * 0.20
            + win_rate_score * 0.15
            + news_score * 0.15
            + risk_score * 0.15
        )

        return round(overall)

        

    @staticmethod
    def recommendation(overall_score: int) -> str:
        if overall_score >= 75:
            return "STRONG_BUY"
        if overall_score >= 60:
            return "WATCH"
        if overall_score >= 40:
            return "HOLD"
        return "AVOID"