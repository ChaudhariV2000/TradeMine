import type {
  AutomationStatus,
} from "../types/trading";

type AutomationCardProps = {
  automation: AutomationStatus | null;
  actionLoading: boolean;
  onToggle: () => void;
};

export function AutomationCard({
  automation,
  actionLoading,
  onToggle,
}: AutomationCardProps) {
  return (
    <article className="panel">
      <div className="panel-header">
        <h2>Automation</h2>

        <button
          type="button"
          className={
            automation?.enabled
              ? "danger-small"
              : "success-small"
          }
          disabled={actionLoading}
          onClick={onToggle}
        >
          {automation?.enabled
            ? "Disable"
            : "Enable"}
        </button>
      </div>

      <div className="detail-list">
        <DetailRow
          label="Enabled"
          value={
            automation?.enabled
              ? "Yes"
              : "No"
          }
        />

        <DetailRow
          label="Scheduler"
          value={
            automation?.scheduler_running
              ? "Running"
              : "Stopped"
          }
        />

        <DetailRow
          label="Execution"
          value={
            automation?.is_executing
              ? "Running"
              : "Idle"
          }
        />

        <DetailRow
          label="Last Run"
          value={
            automation?.last_run_status ??
            "Unknown"
          }
        />
      </div>
    </article>
  );
}

function DetailRow({
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