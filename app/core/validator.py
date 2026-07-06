import pandas as pd

from app.core.exceptions import ValidationError


class DataValidator:

    REQUIRED_COLUMNS = [
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]

    @classmethod
    def validate_ohlcv(cls, df: pd.DataFrame):

        missing = [
            col
            for col in cls.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing:
            raise ValidationError(
                f"Missing required columns: {missing}"
            )

        if df.empty:
            raise ValidationError(
                "Received an empty DataFrame."
            )

        return True