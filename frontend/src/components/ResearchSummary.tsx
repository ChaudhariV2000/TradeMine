import { MetricCard } from "./MetricCard";

import type {
  ResearchResult,
} from "../types/trading";

type ResearchSummaryProps = {
  research: ResearchResult;
};

export function ResearchSummary({
  research,
}: ResearchSummaryProps) {
  const hybridDecision =
  research.hybrid_decision;

const finalDecision =
  typeof hybridDecision === "string"
    ? hybridDecision
    : hybridDecision &&
        typeof hybridDecision === "object" &&
        "recommendation" in hybridDecision
      ? String(hybridDecision.recommendation)
      : research.decision.recommendation;

const finalConfidence =
  typeof research.hybrid_score === "number"
    ? research.hybrid_score
    : hybridDecision &&
        typeof hybridDecision === "object" &&
        "confidence" in hybridDecision
      ? Number(hybridDecision.confidence)
      : research.decision.confidence;
  return (
    <section className="metrics-grid">
      <MetricCard
        label="Current Price"
        value={`₹${research.price.toLocaleString(
          "en-IN",
        )}`}
      />

      <MetricCard
        label="Final Decision"
        value={finalDecision}
        detail={`Confidence ${finalConfidence}%`}
        tone={
          ["BUY", "STRONG BUY"].includes(
            finalDecision,
          )
            ? "positive"
            : ["SELL", "AVOID"].includes(
                  finalDecision,
                )
              ? "negative"
              : "normal"
        }
      />

      <MetricCard
        label="Trend"
        value={research.trend}
        detail={`Signal ${research.signal}`}
      />

      <MetricCard
        label="Preferred Strategy"
        value={
          research.preferred_strategy
        }
        detail={
          research.market.regime
        }
      />
    </section>
  );
}