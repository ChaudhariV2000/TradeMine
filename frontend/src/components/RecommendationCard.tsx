import type {
  MarketOpportunity,
} from "../types/trading";

type RecommendationCardProps = {
  opportunity: MarketOpportunity | null;
};

export function RecommendationCard({
  opportunity,
}: RecommendationCardProps) {
  return (
    <article className="best-opportunity">
      <span>Best Opportunity</span>

      {opportunity ? (
        <>
          <strong>
            {opportunity.symbol}
          </strong>

          <div>
            {opportunity.recommendation}
          </div>

          <small>
            Confidence{" "}
            {opportunity.confidence}% · ₹
            {opportunity.price}
          </small>
        </>
      ) : (
        <strong>
          No candidate available
        </strong>
      )}
    </article>
  );
}