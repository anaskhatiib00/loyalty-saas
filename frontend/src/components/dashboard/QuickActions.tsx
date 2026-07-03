import { Gift, QrCode, UserPlus, WalletCards } from "lucide-react"

const actions = [
  { title: "New Customer", icon: UserPlus },
  { title: "Scan QR", icon: QrCode },
  { title: "Issue Wallet", icon: WalletCards },
  { title: "Add Reward", icon: Gift },
]

export function QuickActions() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <h2 className="text-lg font-semibold">Quick actions</h2>
      <p className="mt-1 text-sm text-white/50">
        Common tasks for your business.
      </p>

      <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        {actions.map((action) => {
          const Icon = action.icon

          return (
            <button
              key={action.title}
              className="flex items-center gap-3 rounded-2xl border border-white/10 bg-black/40 px-4 py-3 text-left text-sm transition hover:bg-white/10"
            >
              <Icon className="h-4 w-4 text-white/60" />
              {action.title}
            </button>
          )
        })}
      </div>
    </div>
  )
}