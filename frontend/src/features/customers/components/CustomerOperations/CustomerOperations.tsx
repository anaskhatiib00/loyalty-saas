"use client"

import type {
  Customer,
  LoyaltyActivity,
  LoyaltyCard,
  LoyaltyProgram,
} from "../../types/customer"
import { ActivityCorrections } from "./components/ActivityCorrections"
import { ManualTools } from "./components/ManualTools"
import { PrimaryAction } from "./components/PrimaryAction"
import { ProgramOverview } from "./components/ProgramOverview"
import { useCustomerOperations } from "./hooks/useCustomerOperations"

type Props = {
  customer: Customer
  loyaltyCard: LoyaltyCard | null
  loyaltyProgram: LoyaltyProgram | null
  activities: LoyaltyActivity[]
  onActionCompleted: () => Promise<void> | void
}

export function CustomerOperations({
  customer,
  loyaltyCard,
  loyaltyProgram,
  activities,
  onActionCompleted,
}: Props) {
  const {
    recommendedOperation,
    selectedIsRecommended,
    correctionAmount,
    setCorrectionAmount,
    correctionReason,
    setCorrectionReason,
    submitting,
    hasCard,
    submitPrimaryAction,
    submitManualCorrection,
  } = useCustomerOperations({
    customer,
    loyaltyCard,
    loyaltyProgram,
    onActionCompleted,
  })

  return (
    <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <div className="mb-6">
        <p className="text-sm text-white/50">Customer Operations</p>

        <h2 className="mt-1 text-xl font-semibold tracking-tight">
          Loyalty control center
        </h2>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-white/50">
          Manage this customer&apos;s loyalty progress, review recent activity,
          and correct mistakes from one clean workspace.
        </p>
      </div>

      <div className="grid gap-4 xl:grid-cols-[1fr_1.2fr]">
        <ProgramOverview customer={customer} loyaltyProgram={loyaltyProgram} />

        <PrimaryAction
          title={recommendedOperation?.title ?? "No program action"}
          description={
            recommendedOperation?.description ??
            "Create or activate a loyalty program to enable the main customer action."
          }
          icon={recommendedOperation?.icon ?? (() => null)}
          selected={selectedIsRecommended}
          disabled={!hasCard || submitting || !recommendedOperation}
          onClick={submitPrimaryAction}
        />
      </div>

      <div className="mt-4 grid gap-4 xl:grid-cols-[1fr_1fr]">
        <ActivityCorrections activities={activities} />

        <ManualTools
          amount={correctionAmount}
          reason={correctionReason}
          submitting={submitting}
          disabled={!hasCard}
          onAmountChange={setCorrectionAmount}
          onReasonChange={setCorrectionReason}
          onSubmit={submitManualCorrection}
        />
      </div>
    </section>
  )
}