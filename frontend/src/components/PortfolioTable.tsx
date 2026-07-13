import type {
  Holding,
} from "../types/trading";

type PortfolioTableProps = {
  holdings: Holding[];
  loading: boolean;
  onCloseTrade: (
    holding: Holding,
  ) => void;
};

export function PortfolioTable({
  holdings,
  loading,
  onCloseTrade,
}: PortfolioTableProps) {
  return (
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
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {holdings.length === 0 ? (
            <tr>
              <td
                colSpan={10}
                className="empty-cell"
              >
                No open positions.
              </td>
            </tr>
          ) : (
            holdings.map((holding) => (
              <tr key={holding.id}>
                <td className="symbol-cell">
                  {holding.symbol}
                </td>

                <td>{holding.strategy}</td>
                <td>{holding.quantity}</td>
                <td>₹{holding.entry_price}</td>
                <td>₹{holding.current_price}</td>
                <td>₹{holding.investment}</td>

                <td
                  className={
                    holding.pnl >= 0
                      ? "positive-text"
                      : "negative-text"
                  }
                >
                  ₹{holding.pnl} (
                  {holding.pnl_percent}%)
                </td>

                <td>₹{holding.target}</td>
                <td>₹{holding.stop_loss}</td>

                <td>
                  <button
                    type="button"
                    className="danger-small"
                    disabled={loading}
                    onClick={() =>
                      onCloseTrade(
                        holding,
                      )
                    }
                  >
                    Close
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
}