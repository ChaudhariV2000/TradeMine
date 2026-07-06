from dataclasses import dataclass
@dataclass
class Trade:
    entry_price: float
    exit_price: float
    entry_date: str
    exit_date: str
    quantity: float
    pnl: float
    return_percent: float
    holding_days: int