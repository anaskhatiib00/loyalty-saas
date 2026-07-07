import { TrendingUp } from "lucide-react"

type Props = {
  currentProgress: number
  targetCount: number | null
  programName: string | null
  rewardDescription: string | null
}

export function CustomerProgressPanel({
  currentProgress,
  targetCount,
  programName,
  rewardDescription,
}: Props) {
  const safeTarget = targetCount && targetCount > 0 ? targetCount : null

  const progressPercentage = safeTarget
    ? Math.min((currentProgress / safeTarget) * 100, 100)
    : 0

  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <div className="flex items-start gap-3">
        <div className="rounded-2xl border border-white/10 bg-white/5 p-3">
          <TrendingUp className="h-5 w-5 text-white/60" />
        </div>

        <div>
          <h2 className="text-lg font-semibold">Loyalty progress</h2>
          <p className="mt-1 text-sm text-white/50">
            Current progress toward the next reward.
          </p>
        </div>
      </div>

      <div className="mt-6 rounded-2xl border border-white/10 bg-black/30 p-4">
        <p className="text-sm text-white/40">Program</p>
        <p className="mt-1 font-medium">
          {programName || "No active loyalty program"}
        </p>

        {rewardDescription && (
          <p className="mt-2 text-sm text-white/50">{rewardDescription}</p>
        )}
      </div>

      <div className="mt-6">
        <div className="flex justify-between text-sm text-white/50">
          <span>Progress</span>
          <span>
            {currentProgress}
            {safeTarget ? ` / ${safeTarget}` : ""}
          </span>
        </div>

        <div className="mt-3 h-3 overflow-hidden rounded-full bg-white/10">
          <div
            className="h-full rounded-full bg-white transition-all"
            style={{ width: `${progressPercentage}%` }}
          />
        </div>

        <p className="mt-3 text-sm text-white/40">
          {safeTarget
            ? `${Math.round(progressPercentage)}% complete`
            : "No target configured yet"}
        </p>
      </div>
    </div>
  )
}