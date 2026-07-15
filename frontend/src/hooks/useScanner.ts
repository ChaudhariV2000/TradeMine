import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  getScannerResults,
  openScannerTrade,
} from "../api/scanner";

import { getApiError } from "../api/api";

import type {
  ScanResult,
} from "../types/trading";

export type RecommendationFilter =
  | "ALL"
  | "STRONG BUY"
  | "BUY"
  | "HOLD"
  | "WATCH"
  | "AVOID"
  | "SELL";

export function useScanner() {
  const [results, setResults] =
    useState<ScanResult[]>([]);

  const [search, setSearch] =
    useState("");

  const [
    recommendationFilter,
    setRecommendationFilter,
  ] =
    useState<RecommendationFilter>("ALL");

  const [
    minimumConfidence,
    setMinimumConfidence,
  ] = useState(0);

  const [loading, setLoading] =
    useState(true);

  const [actionSymbol, setActionSymbol] =
    useState<string | null>(null);

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState("");

  const refresh = useCallback(async () => {
    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const rows =
        await getScannerResults();

      setResults(rows);
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          "Could not load market scanner.",
        ),
      );
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const openTrade = async (
    symbol: string,
  ) => {
    setActionSymbol(symbol);
    setError("");
    setSuccess("");

    try {
      const result =
        await openScannerTrade(symbol);

      if (result.status === "OPENED") {
        setSuccess(
          `${symbol} paper trade opened successfully.`,
        );
      } else {
        setError(
          result.reason ??
            `${symbol} trade was skipped.`,
        );
      }

      return result;
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          `Could not open ${symbol}.`,
        ),
      );

      return null;
    } finally {
      setActionSymbol(null);
    }
  };

  const filteredResults =
    useMemo(() => {
      const normalizedSearch =
        search.trim().toUpperCase();

      return results
        .filter((row) => {
          if (
            normalizedSearch &&
            !row.symbol
              .toUpperCase()
              .includes(normalizedSearch)
          ) {
            return false;
          }

          if (
            recommendationFilter !==
              "ALL" &&
            row.recommendation !==
              recommendationFilter
          ) {
            return false;
          }

          if (
            (row.confidence ?? 0) <
            minimumConfidence
          ) {
            return false;
          }

          return true;
        })
        .sort(
          (first, second) =>
            (second.confidence ?? 0) -
            (first.confidence ?? 0),
        );
    }, [
      results,
      search,
      recommendationFilter,
      minimumConfidence,
    ]);

  const validCount =
    results.filter(
      (row) => !row.error,
    ).length;

  const errorCount =
    results.filter(
      (row) => Boolean(row.error),
    ).length;

  const buyCount =
    results.filter((row) =>
      ["STRONG BUY", "BUY"].includes(
        row.recommendation ?? "",
      ),
    ).length;

  return {
    results,
    filteredResults,

    search,
    setSearch,

    recommendationFilter,
    setRecommendationFilter,

    minimumConfidence,
    setMinimumConfidence,

    loading,
    actionSymbol,
    error,
    success,

    validCount,
    errorCount,
    buyCount,

    refresh,
    openTrade,
  };
}