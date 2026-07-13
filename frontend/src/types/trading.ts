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