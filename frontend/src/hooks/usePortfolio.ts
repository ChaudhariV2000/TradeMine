import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  closePaperTrade,
  depositCash,
  getPortfolio,
} from "../api/portfolio";

import { getApiError } from "../api/api";

import type {
  Holding,
  Portfolio,
} from "../types/trading";

export function usePortfolio() {
  const [portfolio, setPortfolio] =
    useState<Portfolio | null>(null);

  const [loading, setLoading] =
    useState(true);

  const [actionLoading, setActionLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState("");

  const loadPortfolio =
    useCallback(async () => {
      setError("");

      try {
        const result =
          await getPortfolio();

        setPortfolio(result);
      } catch (requestError) {
        setError(
          getApiError(
            requestError,
            "Could not load portfolio.",
          ),
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    void loadPortfolio();
  }, [loadPortfolio]);

  const addCash = async (
    amount: number,
  ) => {
    setActionLoading(true);
    setError("");
    setSuccess("");

    try {
      const result =
        await depositCash(amount);

      setPortfolio(result);

      setSuccess(
        `₹${amount.toLocaleString(
          "en-IN",
        )} added successfully.`,
      );

      return true;
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          "Deposit failed.",
        ),
      );

      return false;
    } finally {
      setActionLoading(false);
    }
  };

  const closeTrade = async (
    holding: Holding,
    exitPrice?: number,
  ) => {
    setActionLoading(true);
    setError("");
    setSuccess("");

    try {
      const result =
        await closePaperTrade(
          holding.id,
          exitPrice,
        );

      setPortfolio(result.portfolio);

      setSuccess(
        `${holding.symbol} closed at ₹${result.trade.exit_price}. P/L ₹${result.trade.pnl}.`,
      );

      return true;
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          "Trade could not be closed.",
        ),
      );

      return false;
    } finally {
      setActionLoading(false);
    }
  };

  return {
    portfolio,
    loading,
    actionLoading,
    error,
    success,
    loadPortfolio,
    addCash,
    closeTrade,
    setError,
    setSuccess,
  };
}