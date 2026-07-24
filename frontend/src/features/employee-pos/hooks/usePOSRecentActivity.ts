"use client"

import { useCallback, useState } from "react"

import { employeePOSService } from "../services/employee-pos.service"
import type { POSRecentActivityResponse } from "../types/employee-pos"

export function usePOSRecentActivity() {
  const [recentActivity, setRecentActivity] =
    useState<POSRecentActivityResponse | null>(null)

  const [isLoadingActivity, setIsLoadingActivity] = useState(false)

  const [activityError, setActivityError] = useState<string | null>(
    null
  )

  const loadRecentActivity = useCallback(async () => {
    try {
      setIsLoadingActivity(true)
      setActivityError(null)

      const result =
        await employeePOSService.getRecentActivity()

      setRecentActivity(result)
    } catch {
      setActivityError("Unable to load recent POS activity.")
    } finally {
      setIsLoadingActivity(false)
    }
  }, [])

  return {
    recentActivity,
    isLoadingActivity,
    activityError,
    loadRecentActivity,
  }
}