import { AutomationCard } from "../components/AutomationCard";
import { Header } from "../components/Header";
import { MetricCard } from "../components/MetricCard";
import { RecommendationCard } from "../components/RecommendationCard";

import { useAutomation } from "../hooks/useAutomation";

export function Dashboard() {
  const {
    briefing,
    automation,
    loading,
    actionLoading,
    error,
    success,
    refresh,
    runDaily,
    runAutomation,
    toggleAutomation,
  } = useAutomation();

  if (loading) {
    return (
      <div className="state-screen">
        Loading TradeMine...
      </div>
    );
  }

  if (!briefing) {
    return (
      <div className="state-screen">
        <p>
          {error ||
            "Dashboard unavailable."}
        </p>

        <button
          type="button"
          onClick={() =>
            void refresh()
          }
        >
          Retry
        </button>
      </div>
    );
  }

  const { summary } =
    briefing.portfolio;

  return (
    <>
      <Header
        eyebrow="Overview"
        title="Trading Dashboard"
        description={
          briefing.recommendation
        }
        actions={
          <>
            <button
              type="button"
              className="secondary"
              disabled={actionLoading}
              onClick={() =>
                void runDaily()
              }
            >
              Run Daily Cycle
            </button>

            <button
              type="button"
              disabled={actionLoading}
              onClick={() =>
                void runAutomation()
              }
            >
              {actionLoading
                ? "Working..."
                : "Run Auto Trader"}
            </button>
          </>
        }
      />

      {error ? (
        <div className="status-message error">
          {error}
        </div>
      ) : null}

      {success ? (
        <div className="status-message success">
          {success}
        </div>
      ) : null}

      <section className="metrics-grid">
        <MetricCard
          label="Portfolio Value"
          value={`₹${summary.current_value.toLocaleString(
            "en-IN",
          )}`}
        />

        <MetricCard
          label="Available Cash"
          value={`₹${summary.cash.toLocaleString(
            "en-IN",
          )}`}
        />

        <MetricCard
          label="Unrealized P/L"
          value={`₹${summary.unrealized_pnl.toLocaleString(
            "en-IN",
          )}`}
          detail={`${summary.return_percent}%`}
          tone={
            summary.unrealized_pnl >= 0
              ? "positive"
              : "negative"
          }
        />

        <MetricCard
          label="Open Positions"
          value={String(
            summary.positions,
          )}
        />
      </section>

      <section className="content-grid">
        <article className="panel">
          <div className="panel-header">
            <h2>Market Overview</h2>
          </div>

          <div className="market-stats">
            <MarketStat
              label="Scanned"
              value={
                briefing.market_status
                  .stocks_scanned
              }
            />

            <MarketStat
              label="Buy"
              value={
                briefing.market_status
                  .buy_candidates
              }
            />

            <MarketStat
              label="Hold"
              value={
                briefing.market_status
                  .hold_candidates
              }
            />

            <MarketStat
              label="Avoid"
              value={
                briefing.market_status
                  .avoid_candidates
              }
            />
          </div>

          <RecommendationCard
            opportunity={
              briefing.market_status
                .best_opportunity
            }
          />
        </article>

        <AutomationCard
          automation={automation}
          actionLoading={
            actionLoading
          }
          onToggle={() =>
            void toggleAutomation()
          }
        />
      </section>
    </>
  );
}

function MarketStat({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="market-stat">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}