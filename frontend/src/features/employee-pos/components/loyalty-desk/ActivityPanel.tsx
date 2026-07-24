import {
  Clock3,
  Loader2,
  RefreshCw,
} from "lucide-react"

import type { POSRecentActivityResponse } from "../../types/employee-pos"
import { ActivityCard } from "./ActivityCard"

type ActivityPanelProps = {
  recentActivity: POSRecentActivityResponse | null
  isLoadingActivity: boolean
  onLoadActivity: () => Promise<void>
}

export function ActivityPanel({
  recentActivity,
  isLoadingActivity,
  onLoadActivity,
}: ActivityPanelProps) {
  return (
    <aside className="flex min-h-[620px] flex-col rounded-3xl border border-white/10 bg-white/[0.04] p-5 shadow-2xl shadow-black/20 sm:p-6">
      <div className="flex items-center justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-sky-300">
            Live session
          </p>

          <h2 className="mt-1 text-xl font-semibold">
            Recent activity
          </h2>
        </div>

        <button
          type="button"
          onClick={() => void onLoadActivity()}
          disabled={isLoadingActivity}
          className="inline-flex size-11 items-center justify-center rounded-2xl border border-white/10 bg-black/20 text-white/60 transition hover:bg-white/5 hover:text-white disabled:opacity-50"
          aria-label="Load recent activity"
        >
          <RefreshCw
            className={`size-5 ${
              isLoadingActivity ? "animate-spin" : ""
            }`}
          />
        </button>
      </div>

      <div className="mt-5 flex-1">
        {isLoadingActivity ? (
          <div className="flex h-full min-h-80 flex-col items-center justify-center text-center">
            <Loader2 className="size-7 animate-spin text-emerald-300" />

            <p className="mt-3 text-sm text-white/45">
              Loading recent activity
            </p>
          </div>
        ) : recentActivity?.activities.length ? (
          <div className="space-y-3">
            {recentActivity.activities.map((activity) => (
              <ActivityCard
                key={activity.id}
                activity={activity}
              />
            ))}
          </div>
        ) : recentActivity ? (
          <div className="flex h-full min-h-80 flex-col items-center justify-center rounded-2xl border border-dashed border-white/10 bg-black/10 px-6 text-center">
            <Clock3 className="size-8 text-white/20" />

            <p className="mt-4 font-medium text-white/70">
              No activity yet
            </p>

            <p className="mt-2 max-w-xs text-sm leading-6 text-white/35">
              Completed loyalty activity will appear here for the
              current employee and location.
            </p>
          </div>
        ) : (
          <div className="flex h-full min-h-80 flex-col items-center justify-center rounded-2xl border border-dashed border-white/10 bg-black/10 px-6 text-center">
            <Clock3 className="size-8 text-white/20" />

            <p className="mt-4 font-medium text-white/70">
              Activity not loaded
            </p>

            <p className="mt-2 max-w-xs text-sm leading-6 text-white/35">
              Use the refresh button to load activity when needed.
            </p>
          </div>
        )}
      </div>

      <div className="mt-5 rounded-2xl border border-white/10 bg-black/20 p-4">
        <p className="text-xs uppercase tracking-[0.18em] text-white/30">
          Loaded activity total
        </p>

        <p className="mt-1 text-2xl font-semibold">
          {recentActivity?.total_activities ?? "—"}
        </p>
      </div>
    </aside>
  )
}