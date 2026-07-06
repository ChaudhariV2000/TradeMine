from dataclasses import dataclass, field


@dataclass
class TechnicalResult:
    score: int = 0

    signal: str = ""

    trend: str = ""

    confidence: int = 0

    reasons: list[str] = field(default_factory=list)

    indicators: dict = field(default_factory=dict)

    features: dict = field(default_factory=dict)