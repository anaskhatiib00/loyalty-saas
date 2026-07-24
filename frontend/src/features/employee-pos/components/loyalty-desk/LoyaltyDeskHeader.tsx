import { MapPin, UserRound } from "lucide-react"

type LoyaltyDeskHeaderProps = {
  businessName: string
  employeeName: string
  locationName: string
  isLoading: boolean
}

export function LoyaltyDeskHeader({
  businessName,
  employeeName,
  locationName,
  isLoading,
}: LoyaltyDeskHeaderProps) {
  return (
    <header className="flex flex-col gap-4 rounded-3xl border border-white/10 bg-white/[0.04] p-5 shadow-2xl shadow-black/20 backdrop-blur-xl sm:flex-row sm:items-center sm:justify-between">
      <div>
        <p className="text-sm font-medium uppercase tracking-[0.2em] text-emerald-300/70">
          Employee POS
        </p>

        <h1 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
          {businessName}
        </h1>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        <div className="flex min-w-52 items-center gap-3 rounded-2xl border border-white/10 bg-black/20 px-4 py-3">
          <div className="flex size-10 items-center justify-center rounded-xl bg-emerald-400/10 text-emerald-300">
            <UserRound className="size-5" />
          </div>

          <div>
            <p className="text-xs uppercase tracking-wide text-white/40">
              Signed in as
            </p>

            <p className="font-medium text-white">
              {isLoading ? "Loading employee" : employeeName}
            </p>
          </div>
        </div>

        <div className="flex min-w-52 items-center gap-3 rounded-2xl border border-white/10 bg-black/20 px-4 py-3">
          <div className="flex size-10 items-center justify-center rounded-xl bg-sky-400/10 text-sky-300">
            <MapPin className="size-5" />
          </div>

          <div>
            <p className="text-xs uppercase tracking-wide text-white/40">
              Assigned location
            </p>

            <p className="font-medium text-white">
              {isLoading ? "Loading location" : locationName}
            </p>
          </div>
        </div>
      </div>
    </header>
  )
}