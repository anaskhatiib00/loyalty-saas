import { Eye, EyeOff, ShieldCheck } from "lucide-react"
import { QRCodeCanvas } from "qrcode.react"
import { useMemo, useState } from "react"

import type { Customer, LoyaltyCard } from "@/features/customers"

type Props = {
  customer: Customer
  loyaltyCard: LoyaltyCard | null
  businessName: string
  programName: string
}

export function CustomerCardPreview({
  customer,
  loyaltyCard,
  businessName,
  programName,
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

  const qrValue = loyaltyCard?.public_id ?? loyaltyCard?.card_number ?? "not-issued"

  return (
    <div className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-gradient-to-br from-white/15 via-white/[0.06] to-white/[0.02] p-5 shadow-2xl">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_right,rgba(255,255,255,0.18),transparent_34%),radial-gradient(circle_at_bottom_left,rgba(255,255,255,0.08),transparent_36%)]" />

      <div className="relative space-y-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-white/40">
              Loyalty Member
            </p>

            <h3 className="mt-2 text-2xl font-semibold tracking-tight">
              {businessName}
            </h3>

            <p className="mt-1 text-sm text-white/45">{programName}</p>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/10 p-2.5">
            <ShieldCheck className="h-5 w-5 text-white/60" />
          </div>
        </div>

        <div>
          <p className="text-sm text-white/40">Customer</p>
          <p className="mt-1 text-xl font-semibold">
            {customerName || "Unnamed Customer"}
          </p>
        </div>

        <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div className="rounded-3xl border border-white/10 bg-white p-3">
            {loyaltyCard ? (
              <QRCodeCanvas value={qrValue} size={112} includeMargin />
            ) : (
              <div className="flex h-[112px] w-[112px] items-center justify-center rounded-2xl bg-black/10 text-center text-xs font-medium text-black/50">
                No card issued
              </div>
            )}
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
                    showCardNumber ? "Hide card number" : "Show card number"
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
      </div>
    </div>
  )
}