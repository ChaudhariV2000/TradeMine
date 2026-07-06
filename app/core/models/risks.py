from dataclasses import dataclass


@dataclass
class RiskResult:
    score: int = 50
    level: str = "MEDIUM"
    volatility: float = 0.0