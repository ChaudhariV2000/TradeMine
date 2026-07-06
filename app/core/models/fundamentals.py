from dataclasses import dataclass, field


@dataclass
class FundamentalResult:
    score: int = 0

    pe: float | None = None
    roe: float | None = None
    debt_to_equity: float | None = None
    market_cap: float | None = None