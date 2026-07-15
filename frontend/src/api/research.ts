import { api } from "./api";

import type {
  ResearchResult,
} from "../types/trading";

export async function getResearch(
  symbol: string,
  options?: {
    refresh?: boolean;
    capital?: number;
    riskPercent?: number;
  },
): Promise<ResearchResult> {
  const response =
    await api.get<ResearchResult>(
      `/research/${encodeURIComponent(
        symbol.toUpperCase(),
      )}`,
      {
        params: {
          refresh:
            options?.refresh ?? false,

          capital:
            options?.capital ?? 100000,

          risk_percent:
            options?.riskPercent ?? 1,
        },
      },
    );

  return response.data;
}