import { Activity } from "lucide-react"

import type { LoyaltyActivity } from "@/features/customers"

type Props = {
  activities: LoyaltyActivity[]
}

export function CustomerActivityTimeline({ activities }: Props) {
  return (
    <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <div className="flex items-center gap-3">
        <Activity className="h-5 w-5 text-white/60" />
        <div>
          <h2 className="text-lg font-semibold">Activity Timeline</h2>
          <p className="text-sm text-white/50">
            Recent earning and redemption activity.
          </p>
        </div>
      </div>

      <div className="mt-6 space-y-3">
        {activities.length === 0 && (
          <div className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-white/40">
            No loyalty activity yet.
          </div>
        )}

        {activities.slice(0, 8).map((activity) => (
          <div
            key={activity.id}
            className="rounded-2xl border border-white/10 bg-black/30 p-4"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="font-medium capitalize">
                  {activity.activity_type.replaceAll("_", " ")}
                </p>
                <p className="mt-1 text-sm text-white/40">
                  {activity.note || "No note"}
                </p>
              </div>

              <div className="text-right">
                <p className="font-medium">
                  +{activity.earned_progress}
                </p>
                <p className="text-sm text-white/40">
                  Balance {activity.balance_after}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </section>
  )
}