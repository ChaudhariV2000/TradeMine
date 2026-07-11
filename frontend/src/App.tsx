import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API = "http://127.0.0.1:8000";

type PortfolioSummary = {
  monthly_budget: number;
  current_month_used: number;
  cash: number;
  invested: number;
  current_value: number;
  unrealized_pnl: number;
  return_percent: number;
  positions: number;
};

type Holding = {
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
};

type DailyBriefing = {
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
    best_opportunity: {
      symbol: string;
      recommendation: string;
      confidence: number;
      price: number;
    } | null;
  };
  portfolio: {
    summary: PortfolioSummary;
    holdings: Holding[];
  };
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

type AutomationStatus = {
  enabled: boolean;
  scheduler_running: boolean;
  is_executing: boolean;
  last_run_status: string;
  last_run_started_at: string | null;
  last_run_completed_at: string | null;
};

function App() {
  const [briefing, setBriefing] = useState<DailyBriefing | null>(null);
  const [automation, setAutomation] = useState<AutomationStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [error, setError] = useState("");

  const loadDashboard = async () => {
    setLoading(true);
    setError("");

    try {
      const [briefingResponse, automationResponse] = await Promise.all([
        axios.get<DailyBriefing>(`${API}/daily-briefing`),
        axios.get<AutomationStatus>(`${API}/automation/status`),
      ]);

      setBriefing(briefingResponse.data);
      setAutomation(automationResponse.data);
    } catch (err) {
      setError(
        axios.isAxiosError(err)
          ? err.message
          : "Could not load TradeMine dashboard."
      );
    } finally {
      setLoading(false);
    }
  };

  const runAutomation = async () => {
    setActionLoading(true);
    setError("");

    try {
      await axios.post(`${API}/automation/run-now`);
      await loadDashboard();
    } catch (err) {
      setError(
        axios.isAxiosError(err)
          ? err.message
          : "Automatic paper-trading run failed."
      );
    } finally {
      setActionLoading(false);
    }
  };

  const runScheduler = async () => {
    setActionLoading(true);
    setError("");

    try {
      await axios.post(`${API}/scheduler/run-daily`);
      await loadDashboard();
    } catch (err) {
      setError(
        axios.isAxiosError(err)
          ? err.message
          : "Daily scheduler run failed."
      );
    } finally {
      setActionLoading(false);
    }
  };

  useEffect(() => {
    void loadDashboard();
  }, []);

  if (loading) {
    return <div className="state-screen">Loading TradeMine...</div>;
  }

  if (!briefing) {
    return (
      <div className="state-screen">
        <p>{error || "Dashboard data is unavailable."}</p>
        <button onClick={() => void loadDashboard()}>Retry</button>
      </div>
    );
  }

  const { summary, holdings } = briefing.portfolio;
  const best = briefing.market_status.best_opportunity;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <div className="brand">TradeMine</div>
          <div className="brand-subtitle">AI Portfolio Manager</div>
        </div>

        <nav>
          <a className="active" href="#overview">Overview</a>
          <a href="#portfolio">Portfolio</a>
          <a href="#market">Market</a>
          <a href="#automation">Automation</a>
        </nav>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h1>Dashboard</h1>
            <p>{briefing.recommendation}</p>
          </div>

          <div className="actions">
            <button
              className="secondary"
              disabled={actionLoading}
              onClick={() => void runScheduler()}
            >
              Run Daily Cycle
            </button>

            <button
              disabled={actionLoading}
              onClick={() => void runAutomation()}
            >
              {actionLoading ? "Running..." : "Run Auto Trader"}
            </button>
          </div>
        </header>

        {error && <div className="error-banner">{error}</div>}

        <section id="overview" className="metrics-grid">
          <MetricCard
            label="Portfolio Value"
            value={`₹${summary.current_value.toLocaleString("en-IN")}`}
          />
          <MetricCard
            label="Available Cash"
            value={`₹${summary.cash.toLocaleString("en-IN")}`}
          />
          <MetricCard
            label="Unrealized P/L"
            value={`₹${summary.unrealized_pnl.toLocaleString("en-IN")}`}
            detail={`${summary.return_percent}%`}
          />
          <MetricCard
            label="Open Positions"
            value={String(summary.positions)}
          />
        </section>

        <section className="two-column-grid">
          <div id="market" className="panel">
            <div className="panel-header">
              <h2>Market Overview</h2>
            </div>

            <div className="market-stats">
              <Stat label="Scanned" value={briefing.market_status.stocks_scanned} />
              <Stat label="Buy" value={briefing.market_status.buy_candidates} />
              <Stat label="Hold" value={briefing.market_status.hold_candidates} />
              <Stat label="Avoid" value={briefing.market_status.avoid_candidates} />
            </div>

            <div className="best-opportunity">
              <span>Best Opportunity</span>
              {best ? (
                <>
                  <strong>{best.symbol}</strong>
                  <div>{best.recommendation}</div>
                  <small>
                    Confidence {best.confidence}% · ₹{best.price}
                  </small>
                </>
              ) : (
                <strong>No candidate</strong>
              )}
            </div>
          </div>

          <div id="automation" className="panel">
            <div className="panel-header">
              <h2>Automation</h2>
            </div>

            <div className="automation-list">
              <Row
                label="Enabled"
                value={automation?.enabled ? "Yes" : "No"}
              />
              <Row
                label="Scheduler"
                value={automation?.scheduler_running ? "Running" : "Stopped"}
              />
              <Row
                label="Execution"
                value={automation?.is_executing ? "Running" : "Idle"}
              />
              <Row
                label="Last Run"
                value={automation?.last_run_status || "Unknown"}
              />
            </div>
          </div>
        </section>

        <section id="portfolio" className="panel">
          <div className="panel-header">
            <h2>Open Holdings</h2>
            <span>{holdings.length} positions</span>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Symbol</th>
                  <th>Strategy</th>
                  <th>Qty</th>
                  <th>Entry</th>
                  <th>Current</th>
                  <th>Investment</th>
                  <th>P/L</th>
                  <th>Target</th>
                  <th>Stop</th>
                </tr>
              </thead>
              <tbody>
                {holdings.length === 0 ? (
                  <tr>
                    <td colSpan={9} className="empty-cell">
                      No open holdings.
                    </td>
                  </tr>
                ) : (
                  holdings.map((holding) => (
                    <tr key={holding.id}>
                      <td className="symbol-cell">{holding.symbol}</td>
                      <td>{holding.strategy}</td>
                      <td>{holding.quantity}</td>
                      <td>₹{holding.entry_price}</td>
                      <td>₹{holding.current_price}</td>
                      <td>₹{holding.investment}</td>
                      <td className={holding.pnl >= 0 ? "positive" : "negative"}>
                        ₹{holding.pnl} ({holding.pnl_percent}%)
                      </td>
                      <td>₹{holding.target}</td>
                      <td>₹{holding.stop_loss}</td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}

function MetricCard({
  label,
  value,
  detail,
}: {
  label: string;
  value: string;
  detail?: string;
}) {
  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      {detail && <small>{detail}</small>}
    </article>
  );
}

function Stat({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="stat">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Row({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

export default App;