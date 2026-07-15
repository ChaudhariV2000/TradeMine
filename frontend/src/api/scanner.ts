import { api } from "./api";

import type {
  OpenTradeResponse,
  ScanResult,
} from "../types/trading";

export async function getScannerResults():
Promise<ScanResult[]> {
  const response =
    await api.get<ScanResult[]>("/scan");

  return response.data;
}

export async function openScannerTrade(
  symbol: string,
): Promise<OpenTradeResponse> {
  const response =
    await api.post<OpenTradeResponse>(
      `/paper-trade/open/${encodeURIComponent(
        symbol,
      )}`,
    );

  return response.data;
}