from app.trading.trading_engine import TradingEngine

from app.repositories.decision_journal_repository import (
    DecisionJournalRepository,
)
class TradingService:

    def __init__(self):
        self.engine = TradingEngine()
        self.decision_repo = DecisionJournalRepository()

    def execute_trade(self, symbol: str):
        result=self.engine.execute_paper_trade(symbol)
        if result.get("status") == "OPENED":
            self.decision_repo.mark_executed(symbol)
        return result

    def execute_best_trades(self, scan_results):
        return self.engine.open_best_paper_trades(
            scan_results
        )