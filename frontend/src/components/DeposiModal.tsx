import {
  useState,
} from "react";

type DepositModalProps = {
  open: boolean;
  loading: boolean;
  onClose: () => void;
  onDeposit: (
    amount: number,
  ) => Promise<boolean>;
};

export function DepositModal({
  open,
  loading,
  onClose,
  onDeposit,
}: DepositModalProps) {
  const [amount, setAmount] =
    useState("");

  if (!open) {
    return null;
  }

  const submit = async () => {
    const parsedAmount =
      Number(amount);

    if (
      !Number.isFinite(parsedAmount) ||
      parsedAmount <= 0
    ) {
      return;
    }

    const success =
      await onDeposit(parsedAmount);

    if (success) {
      setAmount("");
      onClose();
    }
  };

  return (
    <div
      className="modal-backdrop"
      onMouseDown={() => {
        if (!loading) {
          onClose();
        }
      }}
    >
      <div
        className="modal"
        onMouseDown={(event) =>
          event.stopPropagation()
        }
      >
        <h2>Add Cash</h2>

        <p>
          Add more capital to the current
          paper-trading monthly budget.
        </p>

        <label>
          Deposit amount

          <div className="currency-input">
            <span>₹</span>

            <input
              type="number"
              min="1"
              step="0.01"
              placeholder="Enter amount"
              value={amount}
              onChange={(event) =>
                setAmount(
                  event.target.value,
                )
              }
            />
          </div>
        </label>

        <div className="modal-actions">
          <button
            type="button"
            className="secondary"
            disabled={loading}
            onClick={onClose}
          >
            Cancel
          </button>

          <button
            type="button"
            disabled={loading}
            onClick={() =>
              void submit()
            }
          >
            {loading
              ? "Adding..."
              : "Add Cash"}
          </button>
        </div>
      </div>
    </div>
  );
}