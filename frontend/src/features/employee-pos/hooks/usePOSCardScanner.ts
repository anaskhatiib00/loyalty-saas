"use client"

import { useCallback, useState } from "react"

import { employeePOSService } from "../services/employee-pos.service"
import type { POSScanResponse } from "../types/employee-pos"

export function usePOSCardScanner() {
  const [manualCardInput, setManualCardInput] = useState("")

  const [scanResult, setScanResult] =
    useState<POSScanResponse | null>(null)

  const [isScanning, setIsScanning] = useState(false)

  const [scanError, setScanError] = useState<string | null>(null)

  const scanCard = useCallback(
    async (identifierOverride?: string) => {
      const identifier = (
        identifierOverride ?? manualCardInput
      ).trim()

      if (!identifier) {
        setScanResult(null)
        setScanError("Scan or enter a loyalty card first.")
        return
      }

      try {
        setIsScanning(true)
        setScanError(null)
        setScanResult(null)

        const result = await employeePOSService.scanCard({
          loyalty_card_identifier: identifier,
        })

        setScanResult(result)
        setManualCardInput("")
      } catch {
        setScanResult(null)
        setScanError("Unable to process this loyalty card.")
      } finally {
        setIsScanning(false)
      }
    },
    [manualCardInput]
  )

  const resetScan = useCallback(() => {
    setManualCardInput("")
    setScanResult(null)
    setScanError(null)
  }, [])

  return {
    manualCardInput,
    setManualCardInput,

    scanResult,
    isScanning,
    scanError,

    scanCard,
    resetScan,
  }
}