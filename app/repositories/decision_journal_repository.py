from datetime import datetime

from app.database.database import SessionLocal
from app.database.models import DecisionJournal


class DecisionJournalRepository:

    def __init__(self):
        self.db = SessionLocal()

    def save(self, artifact):

        row = DecisionJournal(
            symbol=artifact.symbol,
            recommendation=artifact.metadata["decision"]["recommendation"],
            confidence=artifact.metadata["decision"]["confidence"],

            technical_score=artifact.scores["technical"],
            news_score=artifact.scores["news"],
            risk_score=artifact.scores["risk"],
            fundamental_score=artifact.scores["fundamental"],

            market_regime=artifact.metadata["market_regime"],
            preferred_strategy=artifact.metadata["preferred_strategy"],

            executed="NO",

            created_at=datetime.now().isoformat(),
        )

        self.db.add(row)
        self.db.commit()

        return row

    def all(self):
        return self.db.query(DecisionJournal).all()
    
    def mark_executed(self, symbol: str):

        row = (
            self.db.query(DecisionJournal)
            .filter(DecisionJournal.symbol == symbol)
            .order_by(DecisionJournal.id.desc())
            .first()
        )

        if row:
            row.executed = "YES"
            self.db.commit()

        return row