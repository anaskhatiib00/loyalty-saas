"use client"

import { useEffect, useMemo, useState } from "react"

import { employeePOSService } from "../services/employee-pos.service"
import type {
  POSActivityResult,
  POSActivityType,
  POSLocation,
  ScanResolveResponse,
} from "../types/employee-pos"

type SubmitActivityInput = {
  activityType: POSActivityType
  purchaseAmount?: number
  qualifyingQuantity?: number
  note?: string
}

export function useEmployeePOS() {
  const [scanInput, setScanInput] = useState("")
  const [locations, setLocations] = useState<POSLocation[]>([])
  const [resolvedScan, setResolvedScan] =
    useState<ScanResolveResponse | null>(null)
  const [activityResult, setActivityResult] =
    useState<POSActivityResult | null>(null)

  const [isLoadingLocations, setIsLoadingLocations] = useState(true)
  const [isResolving, setIsResolving] = useState(false)
  const [isSubmittingActivity, setIsSubmittingActivity] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const activeLocation = useMemo(() => {
    return (
      locations.find((location) => location.is_default) ??
      locations[0] ??
      null
    )
  }, [locations])

  useEffect(() => {
    const loadLocations = async () => {
      try {
        setIsLoadingLocations(true)
        setError(null)

        const result = await employeePOSService.getLocations()

        setLocations(result)
      } catch {
        setError("We could not load your business locations.")
      } finally {
        setIsLoadingLocations(false)
      }
    }

    void loadLocations()
  }, [])

  const resolveScan = async () => {
    const identifier = scanInput.trim()

    if (!identifier) {
      setError("Scan or enter a loyalty card code first.")
      return
    }

    try {
      setIsResolving(true)
      setError(null)
      setActivityResult(null)

      const result = await employeePOSService.resolveScan(identifier)

      setResolvedScan(result)
    } catch {
      setResolvedScan(null)
      setError("We could not find this loyalty card.")
    } finally {
      setIsResolving(false)
    }
  }

  const submitActivity = async ({
    activityType,
    purchaseAmount,
    qualifyingQuantity,
    note,
  }: SubmitActivityInput) => {
    if (!resolvedScan) {
      setError("Scan a loyalty card before adding progress.")
      return
    }

    if (!activeLocation) {
      setError("No business location is available for this POS session.")
      return
    }

    try {
      setIsSubmittingActivity(true)
      setError(null)

      const result = await employeePOSService.createActivity({
        loyalty_card_identifier: resolvedScan.loyalty_card.public_id,
        location_id: activeLocation.id,
        activity_type: activityType,
        purchase_amount: purchaseAmount,
        qualifying_quantity: qualifyingQuantity,
        note,
      })

      setActivityResult(result)
    } catch {
      setError("Progress could not be added. Please try again.")
    } finally {
      setIsSubmittingActivity(false)
    }
  }

  const resetPOS = () => {
    setScanInput("")
    setResolvedScan(null)
    setActivityResult(null)
    setError(null)
  }

  return {
    scanInput,
    setScanInput,
    locations,
    activeLocation,
    resolvedScan,
    activityResult,
    isLoadingLocations,
    isResolving,
    isSubmittingActivity,
    error,
    resolveScan,
    submitActivity,
    resetPOS,
  }
}