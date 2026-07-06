class ScoreEngine:
    """
    Utility class for calculating normalized scores.
    """

    MIN_SCORE = 0
    MAX_SCORE = 100

    @classmethod
    def clamp(cls, score: int) -> int:
        return max(cls.MIN_SCORE, min(score, cls.MAX_SCORE))