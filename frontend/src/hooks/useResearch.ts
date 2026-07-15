import {
  useState,
} from "react";

import {
  getResearch,
} from "../api/research";

import {
  getApiError,
} from "../api/api";

import type {
  ResearchResult,
} from "../types/trading";

export function useResearch() {
  const [research, setResearch] =
    useState<ResearchResult | null>(
      null,
    );

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState("");

  const analyze = async (
    symbol: string,
    options?: {
      refresh?: boolean;
      capital?: number;
      riskPercent?: number;
    },
  ) => {
    const normalizedSymbol =
      symbol.trim().toUpperCase();

    if (!normalizedSymbol) {
      setError(
        "Enter a stock symbol.",
      );
      return false;
    }

    setLoading(true);
    setError("");
    setSuccess("");

    try {
      const result =
        await getResearch(
          normalizedSymbol,
          options,
        );

      setResearch(result);

      setSuccess(
        `${normalizedSymbol} research completed.`,
      );

      return true;
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          `Could not research ${normalizedSymbol}.`,
        ),
      );

      return false;
    } finally {
      setLoading(false);
    }
  };

  return {
    research,
    loading,
    error,
    success,
    analyze,
  };
}