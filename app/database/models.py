from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base


class PaperTrade(Base):

    __tablename__ = "paper_trades"

    id = Column(Integer, primary_key=True)

    symbol = Column(String)

    strategy = Column(String)

    entry_price = Column(Float)

    stop_loss = Column(Float)

    target = Column(Float)

    shares = Column(Integer)

    status = Column(String)

    entry_date = Column(String)

    exit_price = Column(Float, nullable=True)

    exit_date = Column(String, nullable=True)

    pnl = Column(Float)

class Portfolio(Base):
    __tablename__ = "portfolio"

    id = Column(Integer, primary_key=True)

    total_value = Column(Float)
    cash = Column(Float)
    invested = Column(Float)

    monthly_budget = Column(Float)

    created_at = Column(String)

class Holding(Base):
    __tablename__ = "holdings"

    id = Column(Integer, primary_key=True)

    symbol = Column(String)

    quantity = Column(Integer)

    average_price = Column(Float)

    current_price = Column(Float)

    invested = Column(Float)

    current_value = Column(Float)

    pnl = Column(Float)
class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)

    symbol = Column(String)

    recommendation = Column(String)

    confidence = Column(Float)

    strategy = Column(String)

    created_at = Column(String)
class Setting(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True)

    monthly_budget = Column(Float)

    risk_profile = Column(String)

    max_positions = Column(Integer)

    paper_trading = Column(String)

class DecisionJournal(Base):
    __tablename__ = "decision_journal"

    id = Column(Integer, primary_key=True)

    symbol = Column(String)
    recommendation = Column(String)
    confidence = Column(Float)

    technical_score = Column(Float)
    news_score = Column(Float)
    risk_score = Column(Float)
    fundamental_score = Column(Float)

    market_regime = Column(String)
    preferred_strategy = Column(String)

    executed = Column(String)  # YES / NO
    created_at = Column(String)

class TradeFeedback(Base):
    __tablename__ = "trade_feedback"

    id = Column(Integer, primary_key=True)

    symbol = Column(String)
    strategy = Column(String)

    recommendation = Column(String)
    confidence = Column(Float)

    technical_score = Column(Float)
    news_score = Column(Float)
    risk_score = Column(Float)
    fundamental_score = Column(Float)

    entry_price = Column(Float)
    exit_price = Column(Float)
    shares = Column(Integer)

    pnl = Column(Float)
    outcome = Column(String)
    exit_reason = Column(String)

    entry_date = Column(String)
    exit_date = Column(String)
    holding_days = Column(Integer)

    created_at = Column(String)