import { Loader2, ScanLine } from "lucide-react"

import type { POSScanResponse } from "../../types/employee-pos"
import { CameraScanner } from "../../scanner/CameraScanner"

type LoyaltyScannerProps = {
  manualCardInput: string
  setManualCardInput: (value: string) => void
  isScanning: boolean
  isWorkspaceUnavailable: boolean
  error: string | null
  scanResult: POSScanResponse | null
  onScan: (identifierOverride?: string) => Promise<void>
  onReset: () => void
}

function formatActivityLabel(activityType: string) {
  return activityType
    .replaceAll("_", " ")
    .replace(/\b\w/g, (character) => character.toUpperCase())
}

export function LoyaltyScanner({
  manualCardInput,
  setManualCardInput,
  isScanning,
  isWorkspaceUnavailable,
  error,
  scanResult,
  onScan,
  onReset,
}: LoyaltyScannerProps) {
  return (
    <section className="flex min-h-[620px] flex-col rounded-3xl border border-white/10 bg-gradient-to-b from-white/[0.06] to-white/[0.02] p-5 shadow-2xl shadow-black/20 sm:p-7">
      <div>
        <p className="text-sm font-medium text-emerald-300">
          Ready to scan
        </p>

        <h2 className="mt-1 text-2xl font-semibold tracking-tight sm:text-3xl">
          Scan the customer loyalty card
        </h2>

        <p className="mt-2 max-w-2xl text-sm leading-6 text-white/55 sm:text-base">
          The platform automatically identifies the customer,
          loyalty program, current progress, and available rewards
          using your assigned employee and location context.
        </p>
      </div>

      <div className="mt-8 flex flex-col">
        <CameraScanner
          disabled={isScanning || isWorkspaceUnavailable}
          onDetected={(identifier) => {
            void onScan(identifier)
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
            void onScan()
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
              disabled={isScanning || isWorkspaceUnavailable}
              className="h-14 w-full rounded-2xl border border-white/10 bg-black/25 pl-12 pr-4 text-base text-white outline-none transition placeholder:text-white/25 focus:border-emerald-300/40 focus:ring-4 focus:ring-emerald-300/10 disabled:cursor-not-allowed disabled:opacity-60"
            />
          </div>

          <button
            type="submit"
            disabled={isScanning || isWorkspaceUnavailable}
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
              <div className="flex-1">
                <p className="font-semibold text-emerald-100">
                  Loyalty activity completed
                </p>

                <p className="mt-1 text-sm text-white/60">
                  Program:{" "}
                  {formatActivityLabel(scanResult.program_type)}
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
                onClick={onReset}
                className="rounded-xl border border-white/10 px-3 py-2 text-sm text-white/60 transition hover:bg-white/5 hover:text-white"
              >
                Clear
              </button>
            </div>
          </div>
        ) : null}
      </div>
    </section>
  )
}