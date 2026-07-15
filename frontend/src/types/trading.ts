export type PortfolioSummary = {
  monthly_budget: number;
  current_month_used: number;
  cash: number;
  invested: number;
  current_value: number;
  unrealized_pnl: number;
  return_percent: number;
  positions: number;
};

export type Holding = {
  id: number;
  symbol: string;
  strategy: string;
  quantity: number;
  entry_price: number;
  current_price: number;
  investment: number;
  current_value: number;
  pnl: number;
  pnl_percent: number;
  stop_loss: number;
  target: number;
  status: string;
  entry_date?: string;
};

export type Portfolio = {
  summary: PortfolioSummary;
  holdings: Holding[];
};

export type MarketOpportunity = {
  symbol: string;
  recommendation: string;
  confidence: number;
  price: number;
};

export type DailyBriefing = {
  recommendation: string;

  alerts: Array<{
    symbol: string;
    type: string;
    message: string;
  }>;

  market_status: {
    stocks_scanned: number;
    buy_candidates: number;
    hold_candidates: number;
    avoid_candidates: number;
    best_opportunity: MarketOpportunity | null;
  };

  portfolio: Portfolio;

  paper_trading: {
    total_trades: number;
    open_trades: number;
    closed_trades: number;
    winning_trades: number;
    losing_trades: number;
    win_rate: number;
    total_pnl: number;
  };
};

export type AutomationStatus = {
  enabled: boolean;
  scheduler_running: boolean;
  is_executing: boolean;
  last_run_status: string;
  last_run_started_at: string | null;
  last_run_completed_at: string | null;

  jobs?: Array<{
    id: string;
    next_run_time: string | null;
  }>;
};

export type ManualCloseResponse = {
  status: string;
  reason: string;

  trade: {
    id: number;
    symbol: string;
    status: string;
    exit_price: number;
    pnl: number;
  };

  portfolio: Portfolio;
};

export type ScanResult = {
  symbol: string;
  price?: number;

  recommendation?: string;
  confidence?: number;

  technical_score?: number;
  news_score?: number;
  risk_score?: number;
  fundamental_score?: number;

  signal?: string;
  trend?: string;

  preferred_strategy?: string;
  market_regime?: string;
  market_volatility?: string;

  risk_level?: string;
  news_sentiment?: string;

  overall_score?: number;
  error?: string;
};

export type OpenTradeResponse = {
  symbol?: string;
  status: string;
  reason?: string;
  decision?: string;
  confidence?: number;
  investment?: number;

  trade?: {
    id: number;
    symbol: string;
    strategy: string;
    entry_price: number;
    stop_loss: number;
    target: number;
    shares: number;
    status: string;
  };
};
export type CommitteeVote = {
  agent: string;
  vote: string;
};

export type StrategyResult = {
  strategy?: string;
  name?: string;
  return_percent?: number;
  final_capital?: number;
  total_trades?: number;
  win_rate?: number;
  [key: string]: unknown;
};

export type ResearchResult = {
  symbol: string;
  timeframe: string;
  price: number;

  technical_score: number;
  fundamental_score: number;

  signal: string;
  trend: string;
  confidence: number;

  reasons: string[];

  indicators: {
    ema20: number;
    ema50: number;
    ema200: number;
    rsi: number;
    macd: number;
    macd_signal: number;
    adx: number;
    atr: number;
  };

  features: {
    price_above_ema20: boolean;
    price_above_ema50: boolean;
    price_above_ema200: boolean;
    rsi_overbought: boolean;
    rsi_oversold: boolean;
    macd_bullish: boolean;
    strong_trend: boolean;
    high_volume: boolean;
  };

  news: {
    score: number;
    sentiment: string;
    confidence: number;
    headlines: string[];
  };

  risk: {
    score: number;
    level: string;
    volatility: number;
  };

  fundamentals: Record<string, unknown>;

  trade_plan: {
    entry: number;
    stop_loss: number;
    take_profit: number;
    risk_reward: number;
  };

  position: {
    capital: number;
    risk_percent: number;
    shares: number;
    investment: number;
  };

  preferred_strategy: string;
  strategy_comparison: StrategyResult[];

  decision: {
    recommendation: string;
    confidence: number;
    [key: string]: unknown;
  };

  market: {
    regime: string;
    volatility: string;
  };

  committee: CommitteeVote[];

  ml_prediction?: unknown;
  hybrid_score?: number;
  hybrid_decision?:
  | string
  | {
      recommendation?: string;
      confidence?: number;
    };
  };
export type PaperTrade = {
  id: number;
  symbol: string;
  strategy: string;

  entry_price: number;
  stop_loss: number;
  target: number;

  shares: number;
  status: string;

  entry_date: string | null;
  exit_price: number | null;
  exit_date: string | null;

  pnl: number;
};

export type PaperTradeSummary = {
  total_trades: number;
  open_trades: number;
  closed_trades: number;
  winning_trades: number;
  losing_trades: number;
  win_rate: number;
  total_pnl: number;
};

export type ExitCheckResult = {
  checked: number;
  closed_count: number;
  still_open_count: number;

  closed: Array<{
    id: number;
    symbol: string;
    reason: string;
    entry_price: number;
    exit_price: number;
    shares: number;
    pnl: number;
  }>;

  still_open: Array<{
    id: number;
    symbol: string;
    current_price: number;
    stop_loss: number;
    target: number;
    unrealized_pnl: number;
  }>;

  errors: Array<{
    id: number;
    symbol: string;
    error: string;
  }>;
};

export type CleanupResult = {
  invalid_trades_closed: number;

  closed: Array<{
    id: number;
    symbol: string;
    reason: string;
  }>;
};