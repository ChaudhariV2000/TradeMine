import type {
  PaperTrade,
} from "../types/trading";

type PaperTradeTableProps = {
  trades: PaperTrade[];
  loading: boolean;

  onCloseTrade: (
    trade: PaperTrade,
  ) => void;
};

export function PaperTradeTable({
  trades,
  loading,
  onCloseTrade,
}: PaperTradeTableProps) {
  return (
    <div className="table-wrap">
      <table className="paper-trade-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Symbol</th>
            <th>Strategy</th>
            <th>Qty</th>
            <th>Entry</th>
            <th>Target</th>
            <th>Stop</th>
            <th>Status</th>
            <th>Entry Date</th>
            <th>Exit Price</th>
            <th>Exit Date</th>
            <th>P/L</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {trades.length === 0 ? (
            <tr>
              <td
                colSpan={13}
                className="empty-cell"
              >
                No trades match the selected
                filters.
              </td>
            </tr>
          ) : (
            trades.map((trade) => {
              const isOpen =
                trade.status === "OPEN";

              return (
                <tr key={trade.id}>
                  <td>{trade.id}</td>

                  <td className="symbol-cell">
                    {trade.symbol}
                  </td>

                  <td>{trade.strategy}</td>
                  <td>{trade.shares}</td>

                  <td>
                    {formatCurrency(
                      trade.entry_price,
                    )}
                  </td>

                  <td>
                    {formatCurrency(
                      trade.target,
                    )}
                  </td>

                  <td>
                    {formatCurrency(
                      trade.stop_loss,
                    )}
                  </td>

                  <td>
                    <TradeStatusBadge
                      status={trade.status}
                    />
                  </td>

                  <td>
                    {formatDate(
                      trade.entry_date,
                    )}
                  </td>

                  <td>
                    {trade.exit_price === null
                      ? "—"
                      : formatCurrency(
                          trade.exit_price,
                        )}
                  </td>

                  <td>
                    {formatDate(
                      trade.exit_date,
                    )}
                  </td>

                  <td
                    className={
                      isOpen
                        ? ""
                        : trade.pnl >= 0
                          ? "positive-text"
                          : "negative-text"
                    }
                  >
                    {isOpen
                      ? "Unrealized"
                      : formatCurrency(
                          trade.pnl,
                        )}
                  </td>

                  <td>
                    {isOpen ? (
                      <button
                        type="button"
                        className="danger-small"
                        disabled={loading}
                        onClick={() =>
                          onCloseTrade(
                            trade,
                          )
                        }
                      >
                        Close
                      </button>
                    ) : (
                      <span className="closed-label">
                        Closed
                      </span>
                    )}
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

function TradeStatusBadge({
  status,
}: {
  status: string;
}) {
  const normalized =
    status
      .toLowerCase()
      .replaceAll("_", "-");

  return (
    <span
      className={`trade-status ${normalized}`}
    >
      {status.replaceAll("_", " ")}
    </span>
  );
}

function formatCurrency(
  value: number,
) {
  return `₹${Number(value).toLocaleString(
    "en-IN",
    {
      maximumFractionDigits: 2,
    },
  )}`;
}

function formatDate(
  value: string | null,
) {
  if (!value) {
    return "—";
  }

  const parsed = new Date(value);

  if (
    Number.isNaN(
      parsed.getTime(),
    )
  ) {
    return value;
  }

  return parsed.toLocaleString(
    "en-IN",
  );
}