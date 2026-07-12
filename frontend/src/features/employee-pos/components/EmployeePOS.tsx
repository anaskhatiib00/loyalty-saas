"use client"

import { RotateCcw, ScanLine, Sparkles } from "lucide-react"

import { useEmployeePOS } from "../hooks/useEmployeePOS"

export function EmployeePOS() {
  const {
    scanInput,
    setScanInput,
    activeLocation,
    resolvedScan,
    activityResult,
    isLoadingLocations,
    isResolving,
    isSubmittingActivity,
    error,
    resolveScan,
    submitActivity,
    resetPOS,
  } = useEmployeePOS()

  const customerName = resolvedScan
    ? `${resolvedScan.customer.first_name} ${
        resolvedScan.customer.last_name ?? ""
      }`.trim()
    : null

  return (
    <main className="min-h-screen bg-[#050505] px-4 py-6 text-white sm:px-6 lg:px-8">
      <section className="mx-auto flex max-w-3xl flex-col gap-6">
        <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 shadow-2xl shadow-black/30">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-medium uppercase tracking-[0.3em] text-emerald-300">
                Employee POS
              </p>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight">
                Scan loyalty card
              </h1>
              <p className="mt-2 max-w-xl text-sm text-white/60">
                Fast employee workflow for adding customer progress during a
                real transaction.
              </p>

              <p className="mt-3 text-xs text-white/40">
                Location:{" "}
                <span className="text-white/70">
                  {isLoadingLocations
                    ? "Loading..."
                    : activeLocation?.name ?? "No location found"}
                </span>
              </p>
            </div>

            <button
              type="button"
              onClick={resetPOS}
              className="inline-flex items-center justify-center gap-2 rounded-2xl border border-white/10 px-4 py-2 text-sm text-white/70 transition hover:bg-white/5 hover:text-white"
            >
              <RotateCcw className="h-4 w-4" />
              Reset
            </button>
          </div>

          <div className="mt-6 flex flex-col gap-3 sm:flex-row">
            <input
              value={scanInput}
              onChange={(event) => setScanInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === "Enter") {
                  void resolveScan()
                }
              }}
              placeholder="Scan or enter card code"
              className="min-h-12 flex-1 rounded-2xl border border-white/10 bg-black/40 px-4 text-sm text-white outline-none transition placeholder:text-white/30 focus:border-emerald-400/60"
            />

            <button
              type="button"
              onClick={() => void resolveScan()}
              disabled={isResolving || isLoadingLocations}
              className="inline-flex min-h-12 items-center justify-center gap-2 rounded-2xl bg-emerald-400 px-5 text-sm font-semibold text-black transition hover:bg-emerald-300 disabled:cursor-not-allowed disabled:opacity-60"
            >
              <ScanLine className="h-4 w-4" />
              {isResolving ? "Checking..." : "Resolve"}
            </button>
          </div>

          {error ? (
            <div className="mt-4 rounded-2xl border border-red-400/20 bg-red-500/10 px-4 py-3 text-sm text-red-200">
              {error}
            </div>
          ) : null}
        </div>

        {resolvedScan ? (
          <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
            <p className="text-sm text-white/50">Customer</p>
            <h2 className="mt-1 text-2xl font-semibold">{customerName}</h2>

            <div className="mt-5 grid gap-3 sm:grid-cols-3">
              <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-white/40">
                  Progress
                </p>
                <p className="mt-2 text-2xl font-semibold">
                  {resolvedScan.customer.current_progress}
                </p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-white/40">
                  Card
                </p>
                <p className="mt-2 truncate text-sm font-medium">
                  {resolvedScan.loyalty_card.card_number}
                </p>
              </div>

              <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
                <p className="text-xs uppercase tracking-[0.2em] text-white/40">
                  Status
                </p>
                <p className="mt-2 text-sm font-medium capitalize">
                  {resolvedScan.loyalty_card.status}
                </p>
              </div>
            </div>

            <div className="mt-6 grid gap-3 sm:grid-cols-2">
              <button
                type="button"
                onClick={() =>
                  void submitActivity({
                    activityType: "visit",
                    qualifyingQuantity: 1,
                    note: "Employee POS visit scan",
                  })
                }
                disabled={isSubmittingActivity || !activeLocation}
                className="inline-flex min-h-14 items-center justify-center gap-2 rounded-2xl bg-white px-5 text-sm font-semibold text-black transition hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <Sparkles className="h-4 w-4" />
                {isSubmittingActivity ? "Adding..." : "Add visit"}
              </button>

              <button
                type="button"
                onClick={() =>
                  void submitActivity({
                    activityType: "stamp_scan",
                    qualifyingQuantity: 1,
                    note: "Employee POS stamp scan",
                  })
                }
                disabled={isSubmittingActivity || !activeLocation}
                className="inline-flex min-h-14 items-center justify-center gap-2 rounded-2xl border border-white/10 px-5 text-sm font-semibold text-white transition hover:bg-white/5 disabled:cursor-not-allowed disabled:opacity-60"
              >
                Add stamp
              </button>
            </div>
          </div>
        ) : null}

        {activityResult ? (
          <div className="rounded-3xl border border-emerald-400/20 bg-emerald-500/10 p-6">
            <p className="text-sm font-medium text-emerald-200">
              Progress added successfully
            </p>

            {activityResult.unlocked_rewards.length > 0 ? (
              <div className="mt-4 rounded-2xl border border-emerald-400/20 bg-black/20 p-4">
                <p className="text-sm font-semibold text-white">
                  Reward available
                </p>
                <p className="mt-1 text-sm text-white/60">
                  {activityResult.unlocked_rewards[0]?.name}
                </p>
              </div>
            ) : (
              <p className="mt-2 text-sm text-white/60">
                No reward unlocked yet.
              </p>
            )}
          </div>
        ) : null}
      </section>
    </main>
  )
}