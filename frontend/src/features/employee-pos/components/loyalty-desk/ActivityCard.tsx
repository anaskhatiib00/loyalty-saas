import { Clock3 } from "lucide-react"

import type { POSActivityItem } from "../../types/employee-pos"

type ActivityCardProps = {
  activity: POSActivityItem
}

function formatActivityTime(value: string) {
  return new Intl.DateTimeFormat("en", {
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value))
}

function formatActivityLabel(activityType: string) {
  return activityType
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

export function ActivityCard({
  activity,
}: ActivityCardProps) {
  return (
    <article className="rounded-2xl border border-white/10 bg-black/20 p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="font-medium text-white">
            {activity.customer_name}
          </p>

          <p className="mt-1 text-sm text-white/45">
            {formatActivityLabel(activity.activity_type)}
          </p>
        </div>

        <div className="flex items-center gap-1.5 text-xs text-white/35">
          <Clock3 className="size-3.5" />
          {formatActivityTime(activity.created_at)}
        </div>
      </div>

      <div className="mt-4 flex items-center justify-between rounded-xl bg-white/[0.04] px-3 py-2">
        <span className="text-xs uppercase tracking-wide text-white/35">
          Progress
        </span>

        <span className="text-sm font-semibold text-emerald-200">
          {activity.balance_before} → {activity.balance_after}
        </span>
      </div>

      {activity.reward_name ? (
        <p className="mt-3 text-sm text-amber-200">
          Reward: {activity.reward_name}
        </p>
      ) : null}
    </article>
  )
}