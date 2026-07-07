import { Sparkles } from "lucide-react"

import type { Customer, LoyaltyCard } from "@/features/customers"

import { CustomerCardDetails } from "./CustomerCardDetails"
import { CustomerCardPreview } from "./CustomerCardPreview"
import { CustomerWalletActions } from "./CustomerWalletActions"

type Props = {
  customer: Customer
  loyaltyCard: LoyaltyCard | null
  businessName?: string
  programName?: string
  targetCount?: number | null
}

export function CustomerDigitalCard({
  customer,
  loyaltyCard,
  businessName = "Business",
  programName = "Loyalty Program",
  targetCount,
}: Props) {
  const isActive = customer.is_active ?? true

  return (
    <section className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <div className="pointer-events-none absolute -right-20 -top-20 h-56 w-56 rounded-full bg-white/10 blur-3xl" />
      <div className="pointer-events-none absolute -bottom-24 -left-24 h-56 w-56 rounded-full bg-white/5 blur-3xl" />

      <div className="relative space-y-5">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl border border-white/10 bg-white/10 p-3">
              <Sparkles className="h-5 w-5 text-white/70" />
            </div>

            <div>
              <h2 className="text-lg font-semibold">Digital Loyalty Card</h2>
              <p className="text-sm text-white/50">
                Customer card identity, QR code, and wallet actions.
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

        <CustomerCardPreview
          customer={customer}
          loyaltyCard={loyaltyCard}
          businessName={businessName}
          programName={programName}
        />

        <CustomerWalletActions loyaltyCard={loyaltyCard} />

        <CustomerCardDetails
          customer={customer}
          loyaltyCard={loyaltyCard}
          businessName={programName}
          targetCount={targetCount}
        />
      </div>
    </section>
  )
}