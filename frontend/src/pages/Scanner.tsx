import { Header } from "../components/Header";
import { MetricCard } from "../components/MetricCard";
import { ScannerTable } from "../components/ScannerTable";

import {
  type RecommendationFilter,
  useScanner,
} from "../hooks/useScanner";

const recommendationOptions:
RecommendationFilter[] = [
  "ALL",
  "STRONG BUY",
  "BUY",
  "HOLD",
  "WATCH",
  "AVOID",
  "SELL",
];

export function Scanner() {
  const {
    results,
    filteredResults,

    search,
    setSearch,

    recommendationFilter,
    setRecommendationFilter,

    minimumConfidence,
    setMinimumConfidence,

    loading,
    actionSymbol,
    error,
    success,

    validCount,
    errorCount,
    buyCount,

    refresh,
    openTrade,
  } = useScanner();

  return (
    <>
      <Header
        eyebrow="Market Intelligence"
        title="Stock Scanner"
        description="Compare TradeMine recommendations, confidence, agent scores and preferred strategies."
        actions={
          <button
            type="button"
            disabled={loading}
            onClick={() =>
              void refresh()
            }
          >
            {loading
              ? "Scanning..."
              : "Refresh Scanner"}
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
          label="Stocks Scanned"
          value={String(
            results.length,
          )}
        />

        <MetricCard
          label="Valid Results"
          value={String(validCount)}
        />

        <MetricCard
          label="Buy Candidates"
          value={String(buyCount)}
          tone={
            buyCount > 0
              ? "positive"
              : "normal"
          }
        />

        <MetricCard
          label="Scanner Errors"
          value={String(errorCount)}
          tone={
            errorCount > 0
              ? "negative"
              : "normal"
          }
        />
      </section>

      <section className="panel scanner-filters">
        <div className="filter-group">
          <label htmlFor="scanner-search">
            Search symbol
          </label>

          <input
            id="scanner-search"
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
          <label htmlFor="decision-filter">
            Recommendation
          </label>

          <select
            id="decision-filter"
            value={
              recommendationFilter
            }
            onChange={(event) =>
              setRecommendationFilter(
                event.target
                  .value as RecommendationFilter,
              )
            }
          >
            {recommendationOptions.map(
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

        <div className="filter-group">
          <label htmlFor="confidence-filter">
            Minimum confidence:{" "}
            {minimumConfidence}
          </label>

          <input
            id="confidence-filter"
            type="range"
            min="0"
            max="100"
            step="5"
            value={
              minimumConfidence
            }
            onChange={(event) =>
              setMinimumConfidence(
                Number(
                  event.target.value,
                ),
              )
            }
          />
        </div>

        <div className="filter-summary">
          Showing{" "}
          <strong>
            {filteredResults.length}
          </strong>{" "}
          of{" "}
          <strong>
            {results.length}
          </strong>
        </div>
      </section>

      <section className="panel">
        <div className="panel-header">
          <div>
            <h2>
              Scanner Results
            </h2>

            <p>
              Only BUY and STRONG BUY
              recommendations can be opened
              from this page.
            </p>
          </div>
        </div>

        {loading ? (
          <div className="panel-loading">
            Running stock research and
            committee analysis...
          </div>
        ) : (
          <ScannerTable
            results={
              filteredResults
            }
            actionSymbol={
              actionSymbol
            }
            onOpenTrade={(
              symbol,
            ) =>
              void openTrade(
                symbol,
              )
            }
          />
        )}
      </section>
    </>
  );
}