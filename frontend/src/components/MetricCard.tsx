type MetricCardProps = {
  label: string;
  value: string;
  detail?: string;
  tone?: "normal" | "positive" | "negative";
};

export function MetricCard({
  label,
  value,
  detail,
  tone = "normal",
}: MetricCardProps) {
  return (
    <article
      className={`metric-card ${tone}`}
    >
      <span>{label}</span>
      <strong>{value}</strong>

      {detail ? (
        <small>{detail}</small>
      ) : null}
    </article>
  );
}