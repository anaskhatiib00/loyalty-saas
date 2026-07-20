"use client"

import { useCallback, useState } from "react"

import { employeePOSService } from "../services/employee-pos.service"
import type {
  POSRecentActivityResponse,
  POSScanResponse,
} from "../types/employee-pos"

export function useEmployeePOS() {
  const [manualCardInput, setManualCardInput] = useState("")
  const [recentActivity, setRecentActivity] =
    useState<POSRecentActivityResponse | null>(null)

  const [scanResult, setScanResult] =
    useState<POSScanResponse | null>(null)

  const [isLoadingActivity, setIsLoadingActivity] = useState(true)
  const [isScanning, setIsScanning] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const loadRecentActivity = useCallback(async () => {
    try {
      setIsLoadingActivity(true)
      setError(null)

      const result =
        await employeePOSService.getRecentActivity()

      setRecentActivity(result)
    } catch {
      setError("Unable to load recent POS activity.")
    } finally {
      setIsLoadingActivity(false)
    }
  }, [])

  const scanCard = async () => {
  const identifier = manualCardInput.trim()

  if (!identifier) {
    setScanResult(null)
    setError("Scan or enter a loyalty card first.")
    return
  }

  try {
    setIsScanning(true)
    setError(null)
    setScanResult(null)

    const result = await employeePOSService.scanCard({
      loyalty_card_identifier: identifier,
    })

    setScanResult(result)

    await loadRecentActivity()
  } catch {
    setScanResult(null)
    setError("Unable to process this loyalty card.")
  } finally {
    setIsScanning(false)
  }
}

  const reset = () => {
    setManualCardInput("")
    setScanResult(null)
    setError(null)
  }

  return {
    manualCardInput,
    setManualCardInput,

    recentActivity,
    scanResult,

    isLoadingActivity,
    isScanning,

    error,

    scanCard,
    loadRecentActivity,
    reset,
  }
}