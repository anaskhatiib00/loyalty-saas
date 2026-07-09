import type { Customer, LoyaltyProgram } from "../../../types/customer"

type Props = {
  customer: Customer
  loyaltyProgram: LoyaltyProgram | null
}

export function ProgramOverview({ customer, loyaltyProgram }: Props) {
  const currentProgress = customer.current_progress ?? 0
  const targetCount = loyaltyProgram?.target_count ?? null

  const progressPercentage = targetCount
    ? Math.min((currentProgress / targetCount) * 100, 100)
    : 0

  return (
    <div className="rounded-3xl border border-white/10 bg-black/30 p-5">
      <p className="text-xs font-medium uppercase tracking-[0.2em] text-white/40">
        Active Program
      </p>

      <h3 className="mt-3 text-2xl font-semibold">
        {loyaltyProgram?.name ?? "No Active Program"}
      </h3>

      <p className="mt-2 text-sm capitalize text-white/50">
        {loyaltyProgram?.program_type ?? "No program configured"}
      </p>

      <div className="mt-8 flex items-end justify-between">
        <div>
          <p className="text-sm text-white/40">Current Progress</p>

          <p className="mt-1 text-4xl font-bold">{currentProgress}</p>
        </div>

        <div className="text-right">
          <p className="text-sm text-white/40">Target</p>

          <p className="mt-1 text-3xl font-semibold">
            {targetCount ?? "-"}
          </p>
        </div>
      </div>

      <div className="mt-8 h-3 overflow-hidden rounded-full bg-white/10">
        <div
          className="h-full rounded-full bg-white transition-all"
          style={{ width: `${progressPercentage}%` }}
        />
      </div>
    </div>
  )
}