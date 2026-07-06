from sqlalchemy.orm import Session

from app.database.models import PaperTrade


class PaperTradeCRUD:

    @staticmethod
    def create(db: Session, trade: dict):

        row = PaperTrade(**trade)

        db.add(row)
        db.commit()
        db.refresh(row)

        return row

    @staticmethod
    def all(db: Session):

        return db.query(PaperTrade).all()

    @staticmethod
    def open_trades(db: Session):

        return (
            db.query(PaperTrade)
            .filter(PaperTrade.status == "OPEN")
            .all()
        )
    @staticmethod
    def update(db: Session, trade_id: int, data: dict):

        row = (
            db.query(PaperTrade)
            .filter(PaperTrade.id == trade_id)
            .first()
        )

        if not row:
            return None

        for key, value in data.items():
            setattr(row, key, value)

        db.commit()
        db.refresh(row)

        return row