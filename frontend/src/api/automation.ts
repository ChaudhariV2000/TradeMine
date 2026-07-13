import { api } from "./api";

import type {
  AutomationStatus,
  DailyBriefing,
} from "../types/trading";

export async function getDailyBriefing():
Promise<DailyBriefing> {
  const response =
    await api.get<DailyBriefing>(
      "/daily-briefing",
    );

  return response.data;
}

export async function getAutomationStatus():
Promise<AutomationStatus> {
  const response =
    await api.get<AutomationStatus>(
      "/automation/status",
    );

  return response.data;
}

export async function runAutoTrader():
Promise<void> {
  await api.post("/automation/run-now");
}

export async function runDailyScheduler():
Promise<void> {
  await api.post("/scheduler/run-daily");
}

export async function enableAutomation():
Promise<AutomationStatus> {
  const response =
    await api.post<AutomationStatus>(
      "/automation/enable",
    );

  return response.data;
}

export async function disableAutomation():
Promise<AutomationStatus> {
  const response =
    await api.post<AutomationStatus>(
      "/automation/disable",
    );

  return response.data;
}