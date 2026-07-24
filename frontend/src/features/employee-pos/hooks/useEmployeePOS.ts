"use client"

import { usePOSCardScanner } from "./usePOSCardScanner"
import { usePOSRecentActivity } from "./usePOSRecentActivity"
import { usePOSWorkspace } from "./usePOSWorkspace"

export function useEmployeePOS() {
  const {
    workspaceContext,
    isLoadingContext,
    isWorkspaceUnavailable,
    contextError,
  } = usePOSWorkspace()

  const {
    recentActivity,
    isLoadingActivity,
    activityError,
    loadRecentActivity,
  } = usePOSRecentActivity()

  const {
    manualCardInput,
    setManualCardInput,
    scanResult,
    isScanning,
    scanError,
    scanCard,
    resetScan,
  } = usePOSCardScanner()

  const error = scanError ?? activityError

  return {
    workspaceContext,
    recentActivity,
    scanResult,

    manualCardInput,
    setManualCardInput,

    isLoadingContext,
    isLoadingActivity,
    isScanning,
    isWorkspaceUnavailable,

    contextError,
    error,

    scanCard,
    loadRecentActivity,
    reset: resetScan,
  }
}