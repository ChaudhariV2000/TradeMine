import type {
  CommitteeVote,
} from "../types/trading";

type CommitteePanelProps = {
  votes: CommitteeVote[];
};

export function CommitteePanel({
  votes,
}: CommitteePanelProps) {
  return (
    <div className="committee-grid">
      {votes.length === 0 ? (
        <p className="empty-message">
          No committee data available.
        </p>
      ) : (
        votes.map((vote) => (
          <div
            className="committee-vote"
            key={`${vote.agent}-${vote.vote}`}
          >
            <span>{vote.agent}</span>

            <strong
              className={getVoteClass(
                vote.vote,
              )}
            >
              {vote.vote}
            </strong>
          </div>
        ))
      )}
    </div>
  );
}

function getVoteClass(
  vote: string,
) {
  const normalized =
    vote.toUpperCase();

  if (
    normalized.includes("BUY")
  ) {
    return "positive-text";
  }

  if (
    normalized.includes("SELL") ||
    normalized.includes("AVOID")
  ) {
    return "negative-text";
  }

  return "";
}