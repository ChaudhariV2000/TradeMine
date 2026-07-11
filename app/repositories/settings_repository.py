from datetime import datetime

from app.database.database import SessionLocal
from app.database.models import Setting


class SettingsRepository:
    def __init__(self):
        self.db = SessionLocal()

    def get_settings(self):
        settings = self.db.query(Setting).first()

        if settings:
            return settings

        settings = Setting(
            monthly_budget=5000,
            risk_profile="MODERATE",
            max_positions=5,
            paper_trading="ON",
        )

        self.db.add(settings)
        self.db.commit()
        self.db.refresh(settings)

        return settings

    def update_settings(self, data: dict):
        settings = self.get_settings()

        for key, value in data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)

        self.db.commit()
        self.db.refresh(settings)

        return settings
    def add_cash(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        settings = self.get_settings()

        settings.monthly_budget = round(
            (settings.monthly_budget or 0) + amount,
            2,
        )

        self.db.commit()
        self.db.refresh(settings)

        return settings