import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  checkPaperTradeExits,
  cleanupPaperTrades,
  getPaperTrades,
  getPaperTradeSummary,
} from "../api/paperTrading";

import {
  closePaperTrade,
} from "../api/portfolio";

import {
  getApiError,
} from "../api/api";

import type {
  PaperTrade,
  PaperTradeSummary,
} from "../types/trading";

export type TradeStatusFilter =
  | "ALL"
  | "OPEN"
  | "CLOSED"
  | "WINNERS"
  | "LOSERS";

export function usePaperTrading() {
  const [trades, setTrades] =
    useState<PaperTrade[]>([]);

  const [summary, setSummary] =
    useState<PaperTradeSummary | null>(
      null,
    );

  const [statusFilter, setStatusFilter] =
    useState<TradeStatusFilter>("ALL");

  const [search, setSearch] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [actionLoading, setActionLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState("");

  const refresh =
    useCallback(async () => {
      setError("");

      try {
        const [
          tradeRows,
          tradeSummary,
        ] = await Promise.all([
          getPaperTrades(),
          getPaperTradeSummary(),
        ]);

        setTrades(tradeRows);
        setSummary(tradeSummary);
      } catch (requestError) {
        setError(
          getApiError(
            requestError,
            "Could not load paper trades.",
          ),
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const runExitCheck = async () => {
    setActionLoading(true);
    setError("");
    setSuccess("");

    try {
      const result =
        await checkPaperTradeExits();

      setSuccess(
        result.closed_count > 0
          ? `${result.closed_count} trade(s) closed automatically.`
          : `${result.checked} trade(s) checked. No exits triggered.`,
      );

      await refresh();
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          "Exit check failed.",
        ),
      );
    } finally {
      setActionLoading(false);
    }
  };

  const runCleanup = async () => {
    setActionLoading(true);
    setError("");
    setSuccess("");

    try {
      const result =
        await cleanupPaperTrades();

      setSuccess(
        result.invalid_trades_closed > 0
          ? `${result.invalid_trades_closed} invalid trade(s) cleaned.`
          : "No invalid trades were found.",
      );

      await refresh();
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          "Trade cleanup failed.",
        ),
      );
    } finally {
      setActionLoading(false);
    }
  };

  const closeTrade = async (
    trade: PaperTrade,
    exitPrice?: number,
  ) => {
    setActionLoading(true);
    setError("");
    setSuccess("");

    try {
      const result =
        await closePaperTrade(
          trade.id,
          exitPrice,
        );

      setSuccess(
        `${trade.symbol} closed at ₹${result.trade.exit_price}. P/L: ₹${result.trade.pnl}.`,
      );

      await refresh();

      return true;
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          `Could not close ${trade.symbol}.`,
        ),
      );

      return false;
    } finally {
      setActionLoading(false);
    }
  };

  const filteredTrades =
    useMemo(() => {
      const normalizedSearch =
        search.trim().toUpperCase();

      return trades.filter((trade) => {
        if (
          normalizedSearch &&
          !trade.symbol
            .toUpperCase()
            .includes(normalizedSearch)
        ) {
          return false;
        }

        if (
          statusFilter === "OPEN" &&
          trade.status !== "OPEN"
        ) {
          return false;
        }

        if (
          statusFilter === "CLOSED" &&
          trade.status === "OPEN"
        ) {
          return false;
        }

        if (
          statusFilter === "WINNERS" &&
          (
            trade.status === "OPEN" ||
            (trade.pnl ?? 0) <= 0
          )
        ) {
          return false;
        }

        if (
          statusFilter === "LOSERS" &&
          (
            trade.status === "OPEN" ||
            (trade.pnl ?? 0) >= 0
          )
        ) {
          return false;
        }

        return true;
      });
    }, [
      trades,
      search,
      statusFilter,
    ]);

  return {
    trades,
    filteredTrades,
    summary,

    search,
    setSearch,

    statusFilter,
    setStatusFilter,

    loading,
    actionLoading,

    error,
    success,

    refresh,
    runExitCheck,
    runCleanup,
    closeTrade,
  };
}