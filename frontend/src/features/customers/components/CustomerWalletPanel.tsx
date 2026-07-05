import { Smartphone, WalletCards } from "lucide-react"

export function CustomerWalletPanel() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <h2 className="text-lg font-semibold">Wallet status</h2>
      <p className="mt-1 text-sm text-white/50">
        Issue and manage digital wallet credentials.
      </p>

      <div className="mt-6 grid gap-3 sm:grid-cols-2">
        <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
          <WalletCards className="h-5 w-5 text-white/60" />
          <p className="mt-3 font-medium">Apple Wallet</p>
          <p className="mt-1 text-sm text-white/40">Not issued yet</p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
          <Smartphone className="h-5 w-5 text-white/60" />
          <p className="mt-3 font-medium">Google Wallet</p>
          <p className="mt-1 text-sm text-white/40">Not issued yet</p>
        </div>
      </div>
    </div>
  )
}