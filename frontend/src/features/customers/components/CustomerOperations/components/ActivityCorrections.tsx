import { History } from "lucide-react"

import type { LoyaltyActivity } from "../../../types/customer"

type Props = {
  activities: LoyaltyActivity[]
}

export function ActivityCorrections({ activities }: Props) {
  const recentActivities = activities.slice(0, 5)

  return (
    <div className="rounded-3xl border border-white/10 bg-black/30 p-5">
      <div className="flex items-start gap-3">
        <div className="rounded-2xl bg-white/10 p-3">
          <History className="h-5 w-5 text-white/60" />
        </div>

        <div>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-white/40">
            Recent Activity
          </p>

          <h3 className="mt-2 text-xl font-semibold">
            Activity Corrections
          </h3>

          <p className="mt-2 text-sm leading-6 text-white/50">
            Soon, managers will correct specific activities directly from this
            list.
          </p>
        </div>
      </div>

      <div className="mt-5 space-y-3">
        {recentActivities.length === 0 && (
          <div className="rounded-2xl border border-dashed border-white/10 p-5 text-center text-sm text-white/40">
            No recent activity yet.
          </div>
        )}

        {recentActivities.map((activity) => (
          <div
            key={activity.id}
            className="flex items-center justify-between gap-4 rounded-2xl border border-white/10 bg-white/[0.03] p-4"
          >
            <div>
              <p className="text-sm font-medium capitalize">
                {activity.activity_type.replaceAll("_", " ")}
              </p>

              <p className="mt-1 text-xs text-white/40">
                {activity.note || "No note"}
              </p>
            </div>

            <div className="text-right">
              <p className="text-sm font-medium">
                +{activity.earned_progress}
              </p>

              <p className="mt-1 text-xs text-white/40">
                Balance {activity.balance_after}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}