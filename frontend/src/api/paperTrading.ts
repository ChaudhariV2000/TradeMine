import { api } from "./api";

import type {
  CleanupResult,
  ExitCheckResult,
  PaperTrade,
  PaperTradeSummary,
} from "../types/trading";

export async function getPaperTrades():
Promise<PaperTrade[]> {
  const response =
    await api.get<PaperTrade[]>(
      "/paper-trades",
    );

  return response.data;
}

export async function getPaperTradeSummary():
Promise<PaperTradeSummary> {
  const response =
    await api.get<PaperTradeSummary>(
      "/paper-trades/summary",
    );

  return response.data;
}

export async function checkPaperTradeExits():
Promise<ExitCheckResult> {
  const response =
    await api.post<ExitCheckResult>(
      "/paper-trades/check-exits",
    );

  return response.data;
}

export async function cleanupPaperTrades():
Promise<CleanupResult> {
  const response =
    await api.post<CleanupResult>(
      "/paper-trades/cleanup",
    );

  return response.data;
}