from app.database.database import SessionLocal
from app.database.models import TradeFeedback


class TradeFeedbackRepository:

    def __init__(self):
        self.db = SessionLocal()

    def save(self, data: dict):
        row = TradeFeedback(**data)

        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)

        return row

    def all(self):
        return self.db.query(TradeFeedback).all()