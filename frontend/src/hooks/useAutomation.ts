import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  disableAutomation,
  enableAutomation,
  getAutomationStatus,
  getDailyBriefing,
  runAutoTrader,
  runDailyScheduler,
} from "../api/automation";

import { getApiError } from "../api/api";

import type {
  AutomationStatus,
  DailyBriefing,
} from "../types/trading";

export function useAutomation() {
  const [briefing, setBriefing] =
    useState<DailyBriefing | null>(null);

  const [automation, setAutomation] =
    useState<AutomationStatus | null>(null);

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
          briefingResult,
          automationResult,
        ] = await Promise.all([
          getDailyBriefing(),
          getAutomationStatus(),
        ]);

        setBriefing(briefingResult);
        setAutomation(automationResult);
      } catch (requestError) {
        setError(
          getApiError(
            requestError,
            "Could not load dashboard.",
          ),
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const performAction = async (
    action: () => Promise<unknown>,
    message: string,
  ) => {
    setActionLoading(true);
    setError("");
    setSuccess("");

    try {
      await action();
      setSuccess(message);
      await refresh();
    } catch (requestError) {
      setError(
        getApiError(
          requestError,
          "Action failed.",
        ),
      );
    } finally {
      setActionLoading(false);
    }
  };

  const runDaily = async () => {
    await performAction(
      runDailyScheduler,
      "Daily cycle completed.",
    );
  };

  const runAutomation = async () => {
    await performAction(
      runAutoTrader,
      "Automatic trading cycle completed.",
    );
  };

  const toggleAutomation = async () => {
    if (!automation) {
      return;
    }

    await performAction(
      automation.enabled
        ? disableAutomation
        : enableAutomation,

      automation.enabled
        ? "Automation disabled."
        : "Automation enabled.",
    );
  };

  return {
    briefing,
    automation,
    loading,
    actionLoading,
    error,
    success,
    refresh,
    runDaily,
    runAutomation,
    toggleAutomation,
  };
}