import {
  useState,
} from "react";

import { CloseTradeModal } from "../components/CloseTradeModal";
import { DepositModal } from "../components/DeposiModal";
import { Header } from "../components/Header";
import { MetricCard } from "../components/MetricCard";
import { PortfolioTable } from "../components/PortfolioTable";

import { usePortfolio } from "../hooks/usePortfolio";

import type {
  Holding,
} from "../types/trading";

export function Portfolio() {
  const {
    portfolio,
    loading,
    actionLoading,
    error,
    success,
    loadPortfolio,
    addCash,
    closeTrade,
  } = usePortfolio();

  const [
    depositModalOpen,
    setDepositModalOpen,
  ] = useState(false);

  const [
    selectedHolding,
    setSelectedHolding,
  ] = useState<Holding | null>(
    null,
  );

  if (loading) {
    return (
      <div className="state-screen">
        Loading portfolio...
      </div>
    );
  }

  if (!portfolio) {
    return (
      <div className="state-screen">
        <p>
          {error ||
            "Portfolio unavailable."}
        </p>

        <button
          type="button"
          onClick={() =>
            void loadPortfolio()
          }
        >
          Retry
        </button>
      </div>
    );
  }

  const {
    summary,
    holdings,
  } = portfolio;

  return (
    <>
      <Header
        eyebrow="Capital Management"
        title="Portfolio"
        description="Manage paper-trading capital and open positions."
        actions={
          <button
            type="button"
            onClick={() =>
              setDepositModalOpen(true)
            }
          >
            Add Cash
          </button>
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
          label="Monthly Capital"
          value={`₹${summary.monthly_budget.toLocaleString(
            "en-IN",
          )}`}
        />

        <MetricCard
          label="Used This Month"
          value={`₹${summary.current_month_used.toLocaleString(
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
          label="Portfolio P/L"
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
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>Open Positions</h2>

            <p>
              Close positions manually using
              the current or custom price.
            </p>
          </div>

          <span>
            {holdings.length} positions
          </span>
        </div>

        <PortfolioTable
          holdings={holdings}
          loading={actionLoading}
          onCloseTrade={
            setSelectedHolding
          }
        />
      </section>

      <DepositModal
        open={depositModalOpen}
        loading={actionLoading}
        onClose={() =>
          setDepositModalOpen(false)
        }
        onDeposit={addCash}
      />

      <CloseTradeModal
        holding={selectedHolding}
        loading={actionLoading}
        onClose={() =>
          setSelectedHolding(null)
        }
        onConfirm={closeTrade}
      />
    </>
  );
}