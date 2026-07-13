import {
  useEffect,
  useState,
} from "react";

import type {
  Holding,
} from "../types/trading";

type CloseTradeModalProps = {
  holding: Holding | null;
  loading: boolean;
  onClose: () => void;

  onConfirm: (
    holding: Holding,
    exitPrice?: number,
  ) => Promise<boolean>;
};

export function CloseTradeModal({
  holding,
  loading,
  onClose,
  onConfirm,
}: CloseTradeModalProps) {
  const [exitPrice, setExitPrice] =
    useState("");

  useEffect(() => {
    setExitPrice("");
  }, [holding]);

  if (!holding) {
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
      return;
    }

    const success =
      await onConfirm(
        holding,
        parsedPrice,
      );

    if (success) {
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
        <h2>
          Close {holding.symbol}
        </h2>

        <p>
          Leave the price blank to use
          the latest cached price of ₹
          {holding.current_price}.
        </p>

        <label>
          Exit price

          <div className="currency-input">
            <span>₹</span>

            <input
              type="number"
              min="0.01"
              step="0.01"
              placeholder={String(
                holding.current_price,
              )}
              value={exitPrice}
              onChange={(event) =>
                setExitPrice(
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