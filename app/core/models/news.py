from dataclasses import dataclass, field


@dataclass
class NewsResult:
    score: int = 50

    sentiment: str = "Neutral"

    confidence: int = 0

    headlines: list[str] = field(default_factory=list)