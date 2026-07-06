class PortfolioScorer:
    """
    Scores how well a stock fits into the portfolio.
    """

    def score(
        self,
        duplicate_position: bool,
        enough_cash: bool,
        allocation_ok: bool,
        positions_ok: bool,
    ):

        score = 100
        reasons = []

        if duplicate_position:
            score -= 100
            reasons.append("Already in portfolio")

        if not enough_cash:
            score -= 40
            reasons.append("Insufficient cash")

        if not allocation_ok:
            score -= 30
            reasons.append("Allocation too large")

        if not positions_ok: 
            score -= 20
            reasons.append("Maximum positions reached")

        score = max(score, 0)

        return {
            "score": score,
            "reasons": reasons,
        }