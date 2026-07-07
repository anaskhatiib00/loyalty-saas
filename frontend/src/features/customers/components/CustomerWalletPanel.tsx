import { QrCode, Smartphone, WalletCards } from "lucide-react"

import type { LoyaltyCard } from "@/features/customers"

type Props = {
  loyaltyCard: LoyaltyCard | null
}

export function CustomerWalletPanel({ loyaltyCard }: Props) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-lg font-semibold">Wallet status</h2>
          <p className="mt-1 text-sm text-white/50">
            Issue and manage digital wallet credentials.
          </p>
        </div>

        <span className="rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-white/60">
          {loyaltyCard ? loyaltyCard.status : "Not issued"}
        </span>
      </div>

      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
          <WalletCards className="h-5 w-5 text-white/60" />
          <p className="mt-3 font-medium">Apple Wallet</p>
          <p className="mt-1 text-sm text-white/40">
            Ready for credential issuing
          </p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
          <Smartphone className="h-5 w-5 text-white/60" />
          <p className="mt-3 font-medium">Google Wallet</p>
          <p className="mt-1 text-sm text-white/40">
            Ready for credential issuing
          </p>
        </div>
      </div>

      <div className="mt-4 rounded-2xl border border-white/10 bg-black/30 p-4">
        <div className="flex items-center gap-3">
          <QrCode className="h-5 w-5 text-white/60" />
          <div>
            <p className="font-medium">QR / Card Identifier</p>
            <p className="mt-1 break-all text-sm text-white/40">
              {loyaltyCard?.public_id ?? "No loyalty card issued yet"}
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}