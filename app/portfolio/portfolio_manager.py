from app.repositories.settings_repository import SettingsRepository
from app.database.database import SessionLocal
from app.database.models import Holding


class PortfolioManager:

    def __init__(self):
        self.db = SessionLocal()
        self.settings = SettingsRepository()

    def get_holdings(self):
        return self.db.query(Holding).all()

    def has_position(self, symbol: str):

        return (
            self.db.query(Holding)
            .filter(Holding.symbol == symbol)
            .count()
            > 0
        )

    def total_invested(self):

        holdings = self.get_holdings()

        return sum(h.invested for h in holdings)

    def available_cash(self):

        settings = self.settings.get_settings()

        return (
            settings.monthly_budget
            - self.total_invested()
        )