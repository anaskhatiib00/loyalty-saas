"use client"

import { useEffect } from "react"
import {
  CheckCircle2,
  Clock3,
  Loader2,
  MapPin,
  RefreshCw,
  ScanLine,
  UserRound,
} from "lucide-react"

import { useEmployeePOS } from "../hooks/useEmployeePOS"
import { CameraScanner } from "../scanner/CameraScanner"

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

export function EmployeePOS() {
  const {
    manualCardInput,
    setManualCardInput,
    recentActivity,
    scanResult,
    isLoadingActivity,
    isScanning,
    error,
    scanCard,
    loadRecentActivity,
    reset,
  } = useEmployeePOS()

  useEffect(() => {
    void loadRecentActivity()
  }, [loadRecentActivity])

  const employeeName = recentActivity?.employee_name ?? "Employee"
  const locationName =
    recentActivity?.location_name ?? "Loading location"

  return (
    <main className="min-h-screen bg-[#07110f] text-white">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-4 sm:px-6 sm:py-6 lg:px-8">
        <header className="flex flex-col gap-4 rounded-3xl border border-white/10 bg-white/[0.04] p-5 shadow-2xl shadow-black/20 backdrop-blur-xl sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-medium uppercase tracking-[0.2em] text-emerald-300/70">
              Employee POS
            </p>

            <h1 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
              Loyalty checkout
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
                  {employeeName}
                </p>
              </div>
            </div>

            <div className="flex min-w-52 items-center gap-3 rounded-2xl border border-white/10 bg-black/20 px-4 py-3">
              <div className="flex size-10 items-center justify-center rounded-xl bg-sky-400/10 text-sky-300">
                <MapPin className="size-5" />
              </div>

              <div>
                <p className="text-xs uppercase tracking-wide text-white/40">
                  Location
                </p>
                <p className="font-medium text-white">
                  {locationName}
                </p>
              </div>
            </div>
          </div>
        </header>

        <div className="mt-6 grid flex-1 items-start gap-6 lg:grid-cols-[1.25fr_0.75fr]">
          <section className="flex min-h-[620px] flex-col rounded-3xl border border-white/10 bg-gradient-to-b from-white/[0.06] to-white/[0.02] p-5 shadow-2xl shadow-black/20 sm:p-7">
            <div>
              <p className="text-sm font-medium text-emerald-300">
                Ready to scan
              </p>

              <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
                Scan the customer loyalty card
              </h2>

              <p className="mt-2 max-w-2xl text-sm leading-6 text-white/55 sm:text-base">
                The platform automatically identifies the employee,
                location, loyalty program, progress, and available
                rewards.
              </p>
            </div>

            <div className="mt-8 flex flex-col">
              <CameraScanner
                disabled={isScanning}
                onDetected={(identifier) => {
                  void scanCard(identifier)
                }}
              />

              <div className="my-6 flex items-center gap-4">
                <div className="h-px flex-1 bg-white/10" />

                <span className="text-xs font-medium uppercase tracking-[0.2em] text-white/30">
                  Manual fallback
                </span>

                <div className="h-px flex-1 bg-white/10" />
              </div>

              <form
                className="flex flex-col gap-3 sm:flex-row"
                onSubmit={(event) => {
                  event.preventDefault()
                  void scanCard()
                }}
              >
                <label
                  className="sr-only"
                  htmlFor="loyalty-card-identifier"
                >
                  Loyalty card identifier
                </label>

                <div className="relative flex-1">
                  <ScanLine className="absolute left-4 top-1/2 size-5 -translate-y-1/2 text-white/35" />

                  <input
                    id="loyalty-card-identifier"
                    type="text"
                    value={manualCardInput}
                    onChange={(event) =>
                      setManualCardInput(event.target.value)
                    }
                    placeholder="Enter loyalty card code"
                    disabled={isScanning}
                    className="h-14 w-full rounded-2xl border border-white/10 bg-black/25 pl-12 pr-4 text-base text-white outline-none transition placeholder:text-white/25 focus:border-emerald-300/40 focus:ring-4 focus:ring-emerald-300/10 disabled:cursor-not-allowed disabled:opacity-60"
                  />
                </div>

                <button
                  type="submit"
                  disabled={isScanning}
                  className="inline-flex h-14 items-center justify-center gap-2 rounded-2xl bg-white px-6 font-semibold text-[#07110f] transition hover:bg-emerald-100 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {isScanning ? (
                    <>
                      <Loader2 className="size-5 animate-spin" />
                      Processing
                    </>
                  ) : (
                    <>
                      <ScanLine className="size-5" />
                      Process card
                    </>
                  )}
                </button>
              </form>

              {error ? (
                <div className="mt-4 rounded-2xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-100">
                  {error}
                </div>
              ) : null}

              {scanResult ? (
                <div className="mt-4 rounded-2xl border border-emerald-300/20 bg-emerald-400/10 p-4">
                  <div className="flex items-start gap-3">
                    <CheckCircle2 className="mt-0.5 size-6 shrink-0 text-emerald-300" />

                    <div className="flex-1">
                      <p className="font-semibold text-emerald-100">
                        Loyalty activity completed
                      </p>

                      <p className="mt-1 text-sm text-white/60">
                        Program:{" "}
                        {formatActivityLabel(
                          scanResult.program_type
                        )}
                        {" · "}
                        Progress: {scanResult.current_progress}
                      </p>

                      {scanResult.reward_available ? (
                        <p className="mt-2 text-sm font-medium text-amber-200">
                          A reward is now available.
                        </p>
                      ) : null}
                    </div>

                    <button
                      type="button"
                      onClick={reset}
                      className="rounded-xl border border-white/10 px-3 py-2 text-sm text-white/60 transition hover:bg-white/5 hover:text-white"
                    >
                      Clear
                    </button>
                  </div>
                </div>
              ) : null}
            </div>
          </section>

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
                onClick={() => void loadRecentActivity()}
                disabled={isLoadingActivity}
                className="inline-flex size-11 items-center justify-center rounded-2xl border border-white/10 bg-black/20 text-white/60 transition hover:bg-white/5 hover:text-white disabled:opacity-50"
                aria-label="Refresh recent activity"
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
                    <article
                      key={activity.id}
                      className="rounded-2xl border border-white/10 bg-black/20 p-4"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <p className="font-medium text-white">
                            {activity.customer_name}
                          </p>

                          <p className="mt-1 text-sm text-white/45">
                            {formatActivityLabel(
                              activity.activity_type
                            )}
                          </p>
                        </div>

                        <div className="flex items-center gap-1.5 text-xs text-white/35">
                          <Clock3 className="size-3.5" />
                          {formatActivityTime(
                            activity.created_at
                          )}
                        </div>
                      </div>

                      <div className="mt-4 flex items-center justify-between rounded-xl bg-white/[0.04] px-3 py-2">
                        <span className="text-xs uppercase tracking-wide text-white/35">
                          Progress
                        </span>

                        <span className="text-sm font-semibold text-emerald-200">
                          {activity.balance_before} →{" "}
                          {activity.balance_after}
                        </span>
                      </div>

                      {activity.reward_name ? (
                        <p className="mt-3 text-sm text-amber-200">
                          Reward: {activity.reward_name}
                        </p>
                      ) : null}
                    </article>
                  ))}
                </div>
              ) : (
                <div className="flex h-full min-h-80 flex-col items-center justify-center rounded-2xl border border-dashed border-white/10 bg-black/10 px-6 text-center">
                  <Clock3 className="size-8 text-white/20" />

                  <p className="mt-4 font-medium text-white/70">
                    No activity yet
                  </p>

                  <p className="mt-2 max-w-xs text-sm leading-6 text-white/35">
                    Completed loyalty scans will appear here for the
                    current employee and location.
                  </p>
                </div>
              )}
            </div>

            <div className="mt-5 rounded-2xl border border-white/10 bg-black/20 p-4">
              <p className="text-xs uppercase tracking-[0.18em] text-white/30">
                Session total
              </p>

              <p className="mt-1 text-2xl font-semibold">
                {recentActivity?.total_activities ?? 0}
              </p>
            </div>
          </aside>
        </div>
      </div>
    </main>
  )
}