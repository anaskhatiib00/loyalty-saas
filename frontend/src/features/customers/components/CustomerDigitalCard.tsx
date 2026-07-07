import {
  Eye,
  EyeOff,
  QrCode,
  ShieldCheck,
  Sparkles,
} from "lucide-react"
import { useMemo, useState } from "react"

import type { Customer, LoyaltyCard } from "@/features/customers"

type Props = {
  customer: Customer
  loyaltyCard: LoyaltyCard | null
  businessName?: string
  targetCount?: number | null
}

export function CustomerDigitalCard({
  customer,
  loyaltyCard,
  businessName = "Loyalty Program",
  targetCount,
}: Props) {
  const [showCardNumber, setShowCardNumber] = useState(false)

  const customerName = [customer.first_name, customer.last_name]
    .filter(Boolean)
    .join(" ")

  const cardNumber = loyaltyCard?.card_number ?? "Not issued"

  const maskedCardNumber = useMemo(() => {
    if (!loyaltyCard?.card_number) {
      return "Not issued"
    }

    return `•••• ${loyaltyCard.card_number.slice(-4)}`
  }, [loyaltyCard?.card_number])

  const isActive = customer.is_active ?? true

  const currentProgress = customer.current_progress ?? 0

  const progressLabel = targetCount
    ? `${currentProgress} / ${targetCount}`
    : String(currentProgress)

  return (
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <div className="pointer-events-none absolute -right-20 -top-20 h-56 w-56 rounded-full bg-white/10 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-24 -left-24 h-56 w-56 rounded-full bg-white/5 blur-3xl" />

      <div className="relative">
        <div className="mb-5 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl border border-white/10 bg-white/10 p-3">
              <Sparkles className="h-5 w-5 text-white/70" />
            </div>

            <div>
              <h2 className="text-lg font-semibold">Digital Loyalty Card</h2>
              <p className="text-sm text-white/50">
                Customer card identity and membership details.
              </p>
            </div>
          </div>

          <span
            className={
              isActive
                ? "rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-300"
                : "rounded-full border border-red-400/20 bg-red-400/10 px-3 py-1 text-xs text-red-300"
            }
          >
            {isActive ? "Active" : "Inactive"}
          </span>
        </div>

        <div className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-gradient-to-br from-white/15 via-white/[0.06] to-white/[0.02] p-6 shadow-2xl">
          <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.16),transparent_35%),radial-gradient(circle_at_bottom_left,rgba(255,255,255,0.08),transparent_35%)]" />

          <div className="relative space-y-7">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.35em] text-white/40">
                  Loyalty Member
                </p>

                <h3 className="mt-3 text-2xl font-semibold tracking-tight">
                  {businessName}
                </h3>
              </div>

              <ShieldCheck className="h-6 w-6 text-white/50" />
            </div>

            <div>
              <p className="text-sm text-white/40">Customer</p>
              <p className="mt-1 text-xl font-semibold">
                {customerName || "Unnamed Customer"}
              </p>
            </div>

            <div className="flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
              <div className="rounded-3xl border border-white/10 bg-black/30 p-5">
                <QrCode className="h-20 w-20 text-white/80" />
              </div>

              <div className="min-w-0 flex-1 sm:text-right">
                <p className="text-sm text-white/40">Card Number</p>

                <div className="mt-2 flex items-center gap-2 sm:justify-end">
                  <p className="truncate font-mono text-lg font-semibold tracking-wider">
                    {showCardNumber ? cardNumber : maskedCardNumber}
                  </p>

                  {loyaltyCard?.card_number && (
                    <button
                      type="button"
                      onClick={() => setShowCardNumber((value) => !value)}
                      className="rounded-full border border-white/10 bg-white/5 p-2 text-white/60 transition hover:bg-white/10 hover:text-white"
                      aria-label={
                        showCardNumber
                          ? "Hide card number"
                          : "Show card number"
                      }
                    >
                      {showCardNumber ? (
                        <EyeOff className="h-4 w-4" />
                      ) : (
                        <Eye className="h-4 w-4" />
                      )}
                    </button>
                  )}
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between border-t border-white/10 pt-5">
              <div>
                <p className="text-xs uppercase tracking-[0.25em] text-white/30">
                  Wallet Ready
                </p>
                <p className="mt-1 text-sm text-white/60">
                  Apple Wallet · Google Wallet
                </p>
              </div>

              <div className="h-10 w-10 rounded-full border border-white/10 bg-white/10" />
            </div>
          </div>
        </div>

        <div className="mt-5 grid gap-3 sm:grid-cols-2">
          <InfoRow label="Program" value={businessName} />

          <InfoRow
            label="Card Status"
            value={loyaltyCard?.status ?? "Not Issued"}
            badge={Boolean(loyaltyCard)}
          />

          <InfoRow label="Current Progress" value={progressLabel} />

          <InfoRow
            label="Rewards Redeemed"
            value={String(customer.total_rewards_redeemed ?? 0)}
          />
        </div>
      </div>
    </section>
  )
}

type InfoRowProps = {
  label: string
  value: string
  badge?: boolean
}

function InfoRow({ label, value, badge }: InfoRowProps) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-2xl border border-white/10 bg-black/30 px-4 py-3">
      <span className="text-sm text-white/50">{label}</span>

      {badge ? (
        <span className="rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1 text-xs font-medium capitalize text-emerald-300">
          {value.replaceAll("_", " ")}
        </span>
      ) : (
        <span className="text-right font-medium">{value}</span>
      )}
    </div>
  )
}