import {
  AlertCircle,
  Smartphone,
  WalletCards,
} from "lucide-react"

import type { LoyaltyCard } from "@/features/customers"

type Props = {
  loyaltyCard: LoyaltyCard | null
}

export function CustomerWalletActions({ loyaltyCard }: Props) {
  const hasCard = Boolean(loyaltyCard)

  return (
    <div className="space-y-4">
      <div className="rounded-2xl border border-amber-500/20 bg-amber-500/10 p-4">
        <div className="flex items-start gap-3">
          <AlertCircle className="mt-0.5 h-5 w-5 text-amber-400" />

          <div>
            <p className="font-medium text-amber-300">
              Wallet integration not configured
            </p>

            <p className="mt-1 text-sm text-amber-200/70">
              Apple Wallet and Google Wallet providers are not yet connected.
              Customers can already receive loyalty cards, and wallet issuance
              will become available once the providers are configured.
            </p>
          </div>
        </div>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <button
          type="button"
          disabled
          className="flex items-center justify-between rounded-2xl border border-white/10 bg-black/30 px-4 py-3 text-left text-white opacity-60"
        >
          <div className="flex items-center gap-3">
            <WalletCards className="h-5 w-5 text-white/50" />

            <div>
              <p className="font-medium">Apple Wallet</p>

              <p className="text-xs text-white/40">
                {hasCard
                  ? "Provider not configured"
                  : "Issue loyalty card first"}
              </p>
            </div>
          </div>

          <span className="rounded-full border border-amber-500/20 bg-amber-500/10 px-3 py-1 text-xs text-amber-300">
            Coming Soon
          </span>
        </button>

        <button
          type="button"
          disabled
          className="flex items-center justify-between rounded-2xl border border-white/10 bg-black/30 px-4 py-3 text-left text-white opacity-60"
        >
          <div className="flex items-center gap-3">
            <Smartphone className="h-5 w-5 text-white/50" />

            <div>
              <p className="font-medium">Google Wallet</p>

              <p className="text-xs text-white/40">
                {hasCard
                  ? "Provider not configured"
                  : "Issue loyalty card first"}
              </p>
            </div>
          </div>

          <span className="rounded-full border border-amber-500/20 bg-amber-500/10 px-3 py-1 text-xs text-amber-300">
            Coming Soon
          </span>
        </button>
      </div>
    </div>
  )
}