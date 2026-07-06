from dataclasses import dataclass, field
from typing import Any

import pandas as pd
from app.core.models.fundamentals import FundamentalResult
from app.core.models.techincal import TechnicalResult
from app.core.models.risks import RiskResult
from app.core.models.news import NewsResult
@dataclass
class ResearchArtifact:

    symbol: str

    timeframe: str

    market_data: pd.DataFrame

    indicators: dict[str, Any] = field(default_factory=dict)

    news: list = field(default_factory=list)

    fundamentals: dict[str, Any] = field(default_factory=dict)

    scores: dict[str, float] = field(default_factory=dict)

    recommendations: list = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    technical: TechnicalResult = field(
        default_factory=TechnicalResult
    )

    news: NewsResult = field(
            default_factory=NewsResult
        )
    risk: RiskResult = field(
        default_factory=RiskResult
    )
    fundamentals: FundamentalResult = field(
        default_factory=FundamentalResult
    )