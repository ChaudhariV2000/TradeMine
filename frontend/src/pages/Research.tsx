import {
  useState,
} from "react";

import {
  CommitteePanel,
} from "../components/CommitteePanel";

import {
  Header,
} from "../components/Header";

import {
  IndicatorGrid,
} from "../components/IndicatorGrid";

import {
  ResearchSummary,
} from "../components/ResearchSummary";

import {
  useResearch,
} from "../hooks/useResearch";

export function Research() {
  const {
    research,
    loading,
    error,
    success,
    analyze,
  } = useResearch();

  const [symbol, setSymbol] =
    useState("SBIN");

  const [capital, setCapital] =
    useState("100000");

  const [
    riskPercent,
    setRiskPercent,
  ] = useState("1");

  const [refreshData, setRefreshData] =
    useState(false);

  const submit = async (
    event: React.FormEvent,
  ) => {
    event.preventDefault();

    const parsedCapital =
      Number(capital);

    const parsedRisk =
      Number(riskPercent);

    if (
      !Number.isFinite(
        parsedCapital,
      ) ||
      parsedCapital <= 0
    ) {
      return;
    }

    if (
      !Number.isFinite(parsedRisk) ||
      parsedRisk <= 0
    ) {
      return;
    }

    await analyze(symbol, {
      refresh: refreshData,
      capital: parsedCapital,
      riskPercent: parsedRisk,
    });
  };
    const reasons = Array.isArray(research?.reasons)
    ? research.reasons
    : [];

    const committee = Array.isArray(research?.committee)
    ? research.committee
    : [];

    const headlines = Array.isArray(research?.news?.headlines)
    ? research.news.headlines
    : [];

    const features =
    research?.features &&
    typeof research.features === "object"
        ? research.features
        : {};

    const fundamentals =
    research?.fundamentals &&
    typeof research.fundamentals === "object"
        ? research.fundamentals
        : {};

  return (
    <>
      <Header
        eyebrow="Deep Analysis"
        title="Stock Research"
        description="Review technicals, fundamentals, news, risk, committee votes, ML output and the complete trade plan."
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

      <section className="panel research-search-panel">
        <form
          className="research-form"
          onSubmit={(event) =>
            void submit(event)
          }
        >
          <div className="filter-group">
            <label htmlFor="research-symbol">
              Symbol
            </label>

            <input
              id="research-symbol"
              type="text"
              placeholder="SBIN"
              value={symbol}
              onChange={(event) =>
                setSymbol(
                  event.target.value
                    .toUpperCase(),
                )
              }
            />
          </div>

          <div className="filter-group">
            <label htmlFor="research-capital">
              Capital
            </label>

            <input
              id="research-capital"
              type="number"
              min="1"
              value={capital}
              onChange={(event) =>
                setCapital(
                  event.target.value,
                )
              }
            />
          </div>

          <div className="filter-group">
            <label htmlFor="research-risk">
              Risk %
            </label>

            <input
              id="research-risk"
              type="number"
              min="0.1"
              step="0.1"
              value={riskPercent}
              onChange={(event) =>
                setRiskPercent(
                  event.target.value,
                )
              }
            />
          </div>

          <label className="checkbox-control">
            <input
              type="checkbox"
              checked={refreshData}
              onChange={(event) =>
                setRefreshData(
                  event.target.checked,
                )
              }
            />

            Refresh market data
          </label>

          <button
            type="submit"
            disabled={loading}
          >
            {loading
              ? "Analyzing..."
              : "Run Research"}
          </button>
        </form>
      </section>

      {!research && !loading ? (
        <section className="panel research-empty">
          <h2>
            Research any watchlist stock
          </h2>

          <p>
            Enter a symbol and run the
            TradeMine research pipeline.
          </p>
        </section>
      ) : null}

      {research ? (
        <>
          <ResearchSummary
            research={research}
          />

          <section className="research-layout">
            <article className="panel">
              <div className="panel-header">
                <h2>
                  Technical Indicators
                </h2>

                <span>
                  Score{" "}
                  {
                    research.technical_score
                  }
                </span>
              </div>

              <IndicatorGrid
                indicators={
                  research.indicators
                }
              />
            </article>

            <article className="panel">
              <div className="panel-header">
                <h2>Trade Plan</h2>
              </div>

              <div className="detail-list">
                <ResearchRow
                  label="Entry"
                  value={`₹${research.trade_plan.entry}`}
                />

                <ResearchRow
                  label="Stop Loss"
                  value={`₹${research.trade_plan.stop_loss}`}
                />

                <ResearchRow
                  label="Take Profit"
                  value={`₹${research.trade_plan.take_profit}`}
                />

                <ResearchRow
                  label="Risk / Reward"
                  value={String(
                    research.trade_plan
                      .risk_reward,
                  )}
                />

                <ResearchRow
                  label="Shares"
                  value={String(
                    research.position.shares,
                  )}
                />

                <ResearchRow
                  label="Investment"
                  value={`₹${research.position.investment.toLocaleString(
                    "en-IN",
                  )}`}
                />
              </div>
            </article>
          </section>

          <section className="research-layout">
            <article className="panel">
              <div className="panel-header">
                <h2>
                  AI Committee
                </h2>
              </div>

              <CommitteePanel
                votes={
                  committee
                }
              />
            </article>

            <article className="panel">
              <div className="panel-header">
                <h2>
                  Market & Risk
                </h2>
              </div>

              <div className="detail-list">
                <ResearchRow
                  label="Market Regime"
                  value={
                    research.market.regime
                  }
                />

                <ResearchRow
                  label="Market Volatility"
                  value={
                    research.market
                      .volatility
                  }
                />

                <ResearchRow
                  label="Risk Level"
                  value={
                    research.risk.level
                  }
                />

                <ResearchRow
                  label="Risk Score"
                  value={String(
                    research.risk.score,
                  )}
                />

                <ResearchRow
                  label="Volatility"
                  value={String(
                    research.risk
                      .volatility,
                  )}
                />

                <ResearchRow
                  label="Fundamental Score"
                  value={String(
                    research
                      .fundamental_score,
                  )}
                />
              </div>
            </article>
          </section>

          <section className="research-layout">
            <article className="panel">
              <div className="panel-header">
                <h2>
                  Technical Reasons
                </h2>
              </div>

              <ul className="research-list">
                {reasons.length === 0 ? (
                    <li>No technical reasons returned.</li>
                ) : (
                    reasons.map((reason, index) => (
                    <li key={`${reason}-${index}`}>
                        {reason}
                    </li>
                    ))
                )}
                </ul>
            </article>

            <article className="panel">
              <div className="panel-header">
                <h2>News</h2>

                <span>
                  {
                    research.news
                      .sentiment
                  }
                </span>
              </div>

              <div className="detail-list research-news-summary">
                <ResearchRow
                  label="News Score"
                  value={String(
                    research.news.score,
                  )}
                />

                <ResearchRow
                  label="Confidence"
                  value={`${research.news.confidence}%`}
                />
              </div>

             <ul className="research-list">
                {headlines.length === 0 ? (
                    <li>No headlines returned.</li>
                ) : (
                    headlines.map((headline, index) => (
                    <li key={`${headline}-${index}`}>
                        {headline}
                    </li>
                    ))
                )}
                </ul>
            </article>
          </section>

          <section className="research-layout">
            <article className="panel">
              <div className="panel-header">
                <h2>
                  Feature Signals
                </h2>
              </div>

              <div className="feature-grid">
  {Object.entries(features).length === 0 ? (
    <p className="empty-message">
      No feature signals available.
    </p>
  ) : (
    Object.entries(features).map(([key, value]) => (
      <div className="feature-item" key={key}>
        <span>{formatLabel(key)}</span>

        <strong
          className={
            Boolean(value)
              ? "positive-text"
              : ""
          }
        >
          {Boolean(value) ? "YES" : "NO"}
        </strong>
      </div>
    ))
  )}
</div>
            </article>

            <article className="panel">
              <div className="panel-header">
                <h2>
                  Fundamentals
                </h2>
              </div>

              <div className="detail-list">
                {Object.keys(
                  research.fundamentals,
                ).length === 0 ? (
                  <p className="empty-message">
                    No fundamental details.
                  </p>
                ) : (
                  Object.entries(
                    research.fundamentals,
                  ).map(
                    ([key, value]) => (
                      <ResearchRow
                        key={key}
                        label={formatLabel(
                          key,
                        )}
                        value={formatValue(
                          value,
                        )}
                      />
                    ),
                  )
                )}
              </div>
            </article>
          </section>

          <section className="panel">
            <div className="panel-header">
              <h2>
                ML & Hybrid Decision
              </h2>
            </div>

            <div className="detail-list">
              <ResearchRow
  label="Hybrid Decision"
  value={formatValue(
    research.hybrid_decision,
  )}
/>

<ResearchRow
  label="Hybrid Score"
  value={formatValue(
    research.hybrid_score,
  )}
/>

<ResearchRow
  label="ML Prediction"
  value={formatValue(
    research.ml_prediction,
  )}
/>
            </div>
          </section>
        </>
      ) : null}
    </>
  );
}

function ResearchRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="detail-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function formatLabel(
  value: string,
) {
  return value
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase(),
    );
}

function formatValue(
  value: unknown,
): string {
  if (
    value === null ||
    value === undefined
  ) {
    return "Not available";
  }

  if (
    typeof value === "string" ||
    typeof value === "number" ||
    typeof value === "boolean"
  ) {
    return String(value);
  }

  if (
    typeof value === "object"
  ) {
    const row = value as Record<
      string,
      unknown
    >;

    if (
      "recommendation" in row ||
      "confidence" in row
    ) {
      const recommendation =
        row.recommendation
          ? String(row.recommendation)
          : "Unknown";

      const confidence =
        row.confidence !== undefined
          ? ` (${String(
              row.confidence,
            )}% confidence)`
          : "";

      return `${recommendation}${confidence}`;
    }

    return JSON.stringify(value);
  }

  return String(value);
}