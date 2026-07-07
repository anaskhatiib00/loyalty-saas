import type { Customer, LoyaltyCard } from "@/features/customers"

type Props = {
  customer: Customer
  loyaltyCard: LoyaltyCard | null
  businessName: string
  targetCount?: number | null
}

export function CustomerCardDetails({
  customer,
  loyaltyCard,
  businessName,
  targetCount,
}: Props) {
  const currentProgress = customer.current_progress ?? 0

  return (
    <div className="grid gap-3 sm:grid-cols-2">
      <InfoRow
        label="Program"
        value={businessName}
      />

      <InfoRow
        label="Card Status"
        value={loyaltyCard?.status ?? "Not Issued"}
        badge={Boolean(loyaltyCard)}
      />

      <InfoRow
        label="Current Progress"
        value={
          targetCount
            ? `${currentProgress} / ${targetCount}`
            : String(currentProgress)
        }
      />

      <InfoRow
        label="Rewards Redeemed"
        value={String(customer.total_rewards_redeemed ?? 0)}
      />
    </div>
  )
}

type InfoRowProps = {
  label: string
  value: string
  badge?: boolean
}

function InfoRow({
  label,
  value,
  badge,
}: InfoRowProps) {
  return (
    <div className="flex items-center justify-between rounded-2xl border border-white/10 bg-black/30 px-4 py-3">
      <span className="text-sm text-white/50">
        {label}
      </span>

      {badge ? (
        <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs font-medium capitalize text-emerald-300">
          {value.replaceAll("_", " ")}
        </span>
      ) : (
        <span className="font-medium">
          {value}
        </span>
      )}
    </div>
  )
}