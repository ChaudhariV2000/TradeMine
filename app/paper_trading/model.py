from dataclasses import dataclass


@dataclass
class PaperTrade:
    symbol: str
    strategy: str
    entry_price: float
    stop_loss: float
    target: float
    shares: int
    status: str
    entry_date: str
    exit_price: float | None = None
    exit_date: str | None = None
    pnl: float = 0.0