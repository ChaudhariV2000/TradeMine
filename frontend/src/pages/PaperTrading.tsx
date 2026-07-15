import {
  useState,
} from "react";

import {
  ClosePaperTradeModal,
} from "../components/ClosePaperTradeModal";

import {
  Header,
} from "../components/Header";

import {
  MetricCard,
} from "../components/MetricCard";

import {
  PaperTradeTable,
} from "../components/PaperTradeTable";

import {
  type TradeStatusFilter,
  usePaperTrading,
} from "../hooks/usePaperTrading";

import type {
  PaperTrade,
} from "../types/trading";

const statusOptions:
TradeStatusFilter[] = [
  "ALL",
  "OPEN",
  "CLOSED",
  "WINNERS",
  "LOSERS",
];

export function PaperTrading() {
  const {
    trades,
    filteredTrades,
    summary,

    search,
    setSearch,

    statusFilter,
    setStatusFilter,

    loading,
    actionLoading,

    error,
    success,

    refresh,
    runExitCheck,
    runCleanup,
    closeTrade,
  } = usePaperTrading();

  const [
    selectedTrade,
    setSelectedTrade,
  ] =
    useState<PaperTrade | null>(
      null,
    );

  if (loading) {
    return (
      <div className="state-screen">
        Loading paper trades...
      </div>
    );
  }

  return (
    <>
      <Header
        eyebrow="Strategy Testing"
        title="Paper Trading"
        description="Monitor automated strategy trades, manually close positions and review realized performance."
        actions={
          <>
            <button
              type="button"
              className="secondary"
              disabled={actionLoading}
              onClick={() =>
                void runCleanup()
              }
            >
              Clean Invalid Trades
            </button>

            <button
              type="button"
              disabled={actionLoading}
              onClick={() =>
                void runExitCheck()
              }
            >
              {actionLoading
                ? "Checking..."
                : "Check Exits"}
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
          label="Total Trades"
          value={String(
            summary?.total_trades ?? 0,
          )}
        />

        <MetricCard
          label="Open Trades"
          value={String(
            summary?.open_trades ?? 0,
          )}
        />

        <MetricCard
          label="Win Rate"
          value={`${summary?.win_rate ?? 0}%`}
          detail={`${summary?.winning_trades ?? 0} wins / ${summary?.losing_trades ?? 0} losses`}
          tone={
            (summary?.win_rate ?? 0) >= 50
              ? "positive"
              : "normal"
          }
        />

        <MetricCard
          label="Realized P/L"
          value={`₹${(
            summary?.total_pnl ?? 0
          ).toLocaleString(
            "en-IN",
          )}`}
          tone={
            (summary?.total_pnl ?? 0) >= 0
              ? "positive"
              : "negative"
          }
        />
      </section>

      <section className="panel paper-trade-filters">
        <div className="filter-group">
          <label htmlFor="trade-search">
            Search symbol
          </label>

          <input
            id="trade-search"
            type="search"
            placeholder="SBIN, INFY..."
            value={search}
            onChange={(event) =>
              setSearch(
                event.target.value,
              )
            }
          />
        </div>

        <div className="filter-group">
          <label htmlFor="trade-status">
            Trade status
          </label>

          <select
            id="trade-status"
            value={statusFilter}
            onChange={(event) =>
              setStatusFilter(
                event.target
                  .value as TradeStatusFilter,
              )
            }
          >
            {statusOptions.map(
              (option) => (
                <option
                  key={option}
                  value={option}
                >
                  {option}
                </option>
              ),
            )}
          </select>
        </div>

        <div className="filter-summary">
          Showing{" "}
          <strong>
            {filteredTrades.length}
          </strong>{" "}
          of{" "}
          <strong>
            {trades.length}
          </strong>
        </div>

        <button
          type="button"
          className="secondary"
          disabled={actionLoading}
          onClick={() =>
            void refresh()
          }
        >
          Refresh
        </button>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Trade History</h2>

            <p>
              Open trades can be closed
              manually. Closed trades are used
              for strategy analytics and ML
              training.
            </p>
          </div>
        </div>

        <PaperTradeTable
          trades={filteredTrades}
          loading={actionLoading}
          onCloseTrade={
            setSelectedTrade
          }
        />
      </section>

      <ClosePaperTradeModal
        trade={selectedTrade}
        loading={actionLoading}
        onClose={() =>
          setSelectedTrade(null)
        }
        onConfirm={closeTrade}
      />
    </>
  );
}