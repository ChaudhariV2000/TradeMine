import type {
  ScanResult,
} from "../types/trading";

type ScannerTableProps = {
  results: ScanResult[];
  actionSymbol: string | null;

  onOpenTrade: (
    symbol: string,
  ) => void;
};

export function ScannerTable({
  results,
  actionSymbol,
  onOpenTrade,
}: ScannerTableProps) {
  return (
    <div className="table-wrap">
      <table className="scanner-table">
        <thead>
          <tr>
            <th>Symbol</th>
            <th>Price</th>
            <th>Decision</th>
            <th>Confidence</th>
            <th>Technical</th>
            <th>News</th>
            <th>Risk</th>
            <th>Fundamental</th>
            <th>Trend</th>
            <th>Strategy</th>
            <th>Regime</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {results.length === 0 ? (
            <tr>
              <td
                colSpan={12}
                className="empty-cell"
              >
                No stocks match the selected
                filters.
              </td>
            </tr>
          ) : (
            results.map((row) => {
              if (row.error) {
                return (
                  <tr
                    key={row.symbol}
                    className="error-row"
                  >
                    <td className="symbol-cell">
                      {row.symbol}
                    </td>

                    <td colSpan={10}>
                      {row.error}
                    </td>

                    <td>Unavailable</td>
                  </tr>
                );
              }

              const canOpen =
                row.recommendation ===
                  "STRONG BUY" ||
                row.recommendation ===
                  "BUY";

              return (
                <tr key={row.symbol}>
                  <td className="symbol-cell">
                    {row.symbol}
                  </td>

                  <td>
                    {formatCurrency(
                      row.price,
                    )}
                  </td>

                  <td>
                    <DecisionBadge
                      recommendation={
                        row.recommendation
                      }
                    />
                  </td>

                  <td>
                    <ScoreValue
                      value={
                        row.confidence
                      }
                    />
                  </td>

                  <td>
                    <ScoreValue
                      value={
                        row.technical_score
                      }
                    />
                  </td>

                  <td>
                    <ScoreValue
                      value={
                        row.news_score
                      }
                    />
                  </td>

                  <td>
                    <ScoreValue
                      value={
                        row.risk_score
                      }
                    />
                  </td>

                  <td>
                    <ScoreValue
                      value={
                        row.fundamental_score
                      }
                    />
                  </td>

                  <td>
                    {row.trend ?? "—"}
                  </td>

                  <td>
                    {row.preferred_strategy ??
                      "—"}
                  </td>

                  <td>
                    {row.market_regime ??
                      "—"}
                  </td>

                  <td>
                    <button
                      type="button"
                      className={
                        canOpen
                          ? "success-small"
                          : "secondary-small"
                      }
                      disabled={
                        !canOpen ||
                        actionSymbol !== null
                      }
                      onClick={() =>
                        onOpenTrade(
                          row.symbol,
                        )
                      }
                    >
                      {actionSymbol ===
                      row.symbol
                        ? "Opening..."
                        : canOpen
                          ? "Open Trade"
                          : "Not Eligible"}
                    </button>
                  </td>
                </tr>
              );
            })
          )}
        </tbody>
      </table>
    </div>
  );
}

function ScoreValue({
  value,
}: {
  value?: number;
}) {
  if (
    value === undefined ||
    value === null
  ) {
    return <span>—</span>;
  }

  return (
    <span
      className={
        value >= 80
          ? "score-high"
          : value >= 60
            ? "score-medium"
            : "score-low"
      }
    >
      {value}
    </span>
  );
}

function DecisionBadge({
  recommendation,
}: {
  recommendation?: string;
}) {
  const decision =
    recommendation ?? "UNKNOWN";

  const className = decision
    .toLowerCase()
    .replaceAll(" ", "-");

  return (
    <span
      className={`decision-badge ${className}`}
    >
      {decision}
    </span>
  );
}

function formatCurrency(
  value?: number,
) {
  if (
    value === undefined ||
    value === null
  ) {
    return "—";
  }

  return `₹${value.toLocaleString(
    "en-IN",
  )}`;
}