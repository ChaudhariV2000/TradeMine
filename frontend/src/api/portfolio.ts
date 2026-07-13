import { api } from "./api";

import type {
  ManualCloseResponse,
  Portfolio,
} from "../types/trading";

export async function getPortfolio():
Promise<Portfolio> {
  const response = await api.get<Portfolio>(
    "/portfolio",
  );

  return response.data;
}

export async function depositCash(
  amount: number,
): Promise<Portfolio> {
  const response = await api.post<{
    status: string;
    deposit: number;
    monthly_budget: number;
    portfolio: Portfolio;
  }>("/portfolio/deposit", {
    amount,
  });

  return response.data.portfolio;
}

export async function closePaperTrade(
  tradeId: number,
  exitPrice?: number,
): Promise<ManualCloseResponse> {
  const response =
    await api.post<ManualCloseResponse>(
      `/paper-trades/${tradeId}/close`,
      {
        exit_price: exitPrice ?? null,
      },
    );

  return response.data;
}