import type {
  ResearchResult,
} from "../types/trading";

type IndicatorGridProps = {
  indicators:
    ResearchResult["indicators"];
};

export function IndicatorGrid({
  indicators,
}: IndicatorGridProps) {
  const rows = [
    ["EMA 20", indicators.ema20],
    ["EMA 50", indicators.ema50],
    ["EMA 200", indicators.ema200],
    ["RSI", indicators.rsi],
    ["MACD", indicators.macd],
    [
      "MACD Signal",
      indicators.macd_signal,
    ],
    ["ADX", indicators.adx],
    ["ATR", indicators.atr],
  ] as const;

  return (
    <div className="indicator-grid">
      {rows.map(([label, value]) => (
        <div
          className="indicator-card"
          key={label}
        >
          <span>{label}</span>
          <strong>
            {formatNumber(value)}
          </strong>
        </div>
      ))}
    </div>
  );
}

function formatNumber(
  value: number,
) {
  if (!Number.isFinite(value)) {
    return "—";
  }

  return value.toLocaleString(
    "en-IN",
    {
      maximumFractionDigits: 2,
    },
  );
}