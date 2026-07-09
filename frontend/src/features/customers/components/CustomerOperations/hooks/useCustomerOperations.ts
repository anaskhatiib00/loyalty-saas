"use client"

import { useMemo, useState } from "react"
import { toast } from "sonner"

import { customerService } from "../../../services/customer.service"
import type {
  Customer,
  LoyaltyCard,
  LoyaltyProgram,
} from "../../../types/customer"
import {
  type CustomerOperationType,
  getRecommendedCustomerOperation,
} from "../operations"

type UseCustomerOperationsProps = {
  customer: Customer
  loyaltyCard: LoyaltyCard | null
  loyaltyProgram: LoyaltyProgram | null
  onActionCompleted: () => Promise<void> | void
}

export function useCustomerOperations({
  customer,
  loyaltyCard,
  loyaltyProgram,
  onActionCompleted,
}: UseCustomerOperationsProps) {
  const recommendedOperation = useMemo(
    () => getRecommendedCustomerOperation(loyaltyProgram?.program_type),
    [loyaltyProgram?.program_type]
  )

  const [selectedOperation, setSelectedOperation] =
    useState<CustomerOperationType>(recommendedOperation?.type ?? "correction")
  const [correctionAmount, setCorrectionAmount] = useState("1")
  const [correctionReason, setCorrectionReason] = useState("")
  const [submitting, setSubmitting] = useState(false)

  const hasCard = Boolean(loyaltyCard)
  const selectedIsRecommended =
    selectedOperation === recommendedOperation?.type

  async function submitPrimaryAction() {
    if (!loyaltyCard) {
      toast.error("This customer does not have a loyalty card yet.")
      return
    }

    if (!recommendedOperation) {
      toast.error("No active loyalty program action is available.")
      return
    }

    try {
      setSubmitting(true)

      await customerService.createLoyaltyActivity({
        loyalty_card_identifier: loyaltyCard.public_id,
        location_id: customer.location_id ?? 1,
        activity_type:
          recommendedOperation.type === "stamp"
            ? "stamp_scan"
            : recommendedOperation.type === "spend"
              ? "purchase"
              : recommendedOperation.type === "points"
                ? "manual_adjustment"
                : "visit",
        purchase_amount: recommendedOperation.type === "spend" ? 1 : 0,
        qualifying_quantity: 1,
        note: `Customer operation: ${recommendedOperation.title}`,
      })

      toast.success(`${recommendedOperation.title} saved.`)
      await onActionCompleted()
    } catch {
      toast.error("Could not complete customer operation.")
    } finally {
      setSubmitting(false)
    }
  }

  async function submitManualCorrection() {
    const numericAmount = Number(correctionAmount)

    if (!Number.isFinite(numericAmount) || numericAmount <= 0) {
      toast.error("Enter a valid correction amount.")
      return
    }

    if (correctionReason.trim().length < 5) {
      toast.error("A correction reason is required.")
      return
    }

    try {
      setSubmitting(true)

      await customerService.createManualProgressAdjustment({
        customer_id: customer.id,
        change_amount: -Math.abs(numericAmount),
        entry_type: "adjustment",
        reference_type: "manager_adjustment",
        note: correctionReason.trim(),
      })

      toast.success("Correction saved.")
      setCorrectionAmount("1")
      setCorrectionReason("")
      await onActionCompleted()
    } catch {
      toast.error("Could not save correction.")
    } finally {
      setSubmitting(false)
    }
  }

  return {
    recommendedOperation,
    selectedOperation,
    setSelectedOperation,
    selectedIsRecommended,
    correctionAmount,
    setCorrectionAmount,
    correctionReason,
    setCorrectionReason,
    submitting,
    hasCard,
    submitPrimaryAction,
    submitManualCorrection,
  }
}