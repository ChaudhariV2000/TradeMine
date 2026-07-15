import {
  useEffect,
  useState,
} from "react";

import type {
  PaperTrade,
} from "../types/trading";

type ClosePaperTradeModalProps = {
  trade: PaperTrade | null;
  loading: boolean;

  onClose: () => void;

  onConfirm: (
    trade: PaperTrade,
    exitPrice?: number,
  ) => Promise<boolean>;
};

export function ClosePaperTradeModal({
  trade,
  loading,
  onClose,
  onConfirm,
}: ClosePaperTradeModalProps) {
  const [exitPrice, setExitPrice] =
    useState("");

  const [validationError, setValidationError] =
    useState("");

  useEffect(() => {
    setExitPrice("");
    setValidationError("");
  }, [trade]);

  if (!trade) {
    return null;
  }

  const submit = async () => {
    const parsedPrice =
      exitPrice.trim() === ""
        ? undefined
        : Number(exitPrice);

    if (
      parsedPrice !== undefined &&
      (
        !Number.isFinite(parsedPrice) ||
        parsedPrice <= 0
      )
    ) {
      setValidationError(
        "Exit price must be greater than zero.",
      );

      return;
    }

    setValidationError("");

    const successful =
      await onConfirm(
        trade,
        parsedPrice,
      );

    if (successful) {
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
        role="dialog"
        aria-modal="true"
        aria-labelledby="paper-close-title"
        onMouseDown={(event) =>
          event.stopPropagation()
        }
      >
        <h2 id="paper-close-title">
          Close {trade.symbol}
        </h2>

        <p>
          Leave the price blank to use the
          latest cached market price.
        </p>

        <div className="trade-close-summary">
          <div>
            <span>Entry Price</span>
            <strong>
              ₹{trade.entry_price}
            </strong>
          </div>

          <div>
            <span>Quantity</span>
            <strong>
              {trade.shares}
            </strong>
          </div>

          <div>
            <span>Strategy</span>
            <strong>
              {trade.strategy}
            </strong>
          </div>
        </div>

        <label>
          Exit price

          <div className="currency-input">
            <span>₹</span>

            <input
              type="number"
              min="0.01"
              step="0.01"
              placeholder="Latest cached price"
              value={exitPrice}
              onChange={(event) =>
                setExitPrice(
                  event.target.value,
                )
              }
            />
          </div>
        </label>

        {validationError ? (
          <div className="field-error">
            {validationError}
          </div>
        ) : null}

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
            className="danger"
            disabled={loading}
            onClick={() =>
              void submit()
            }
          >
            {loading
              ? "Closing..."
              : "Confirm Close"}
          </button>
        </div>
      </div>
    </div>
  );
}