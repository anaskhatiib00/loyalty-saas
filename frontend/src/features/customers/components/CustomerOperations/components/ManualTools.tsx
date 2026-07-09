import { Loader2, MinusCircle } from "lucide-react"

type Props = {
  amount: string
  reason: string
  submitting: boolean
  disabled: boolean
  onAmountChange: (value: string) => void
  onReasonChange: (value: string) => void
  onSubmit: () => void
}

export function ManualTools({
  amount,
  reason,
  submitting,
  disabled,
  onAmountChange,
  onReasonChange,
  onSubmit,
}: Props) {
  return (
    <div className="rounded-3xl border border-white/10 bg-black/30 p-5">
      <div className="flex items-start gap-3">
        <div className="rounded-2xl bg-white/10 p-3">
          <MinusCircle className="h-5 w-5 text-white/60" />
        </div>

        <div>
          <p className="text-xs font-medium uppercase tracking-[0.2em] text-white/40">
            Manager Tool
          </p>

          <h3 className="mt-2 text-xl font-semibold">Manual Correction</h3>

          <p className="mt-2 text-sm leading-6 text-white/50">
            Use this only when customer progress needs to be corrected. A reason
            is required for audit history.
          </p>
        </div>
      </div>

      <div className="mt-5 space-y-4">
        <div>
          <label className="text-sm font-medium text-white/70">
            Correction amount
          </label>

          <input
            type="number"
            min="1"
            step="1"
            value={amount}
            disabled={disabled || submitting}
            onChange={(event) => onAmountChange(event.target.value)}
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black/40 px-4 py-3 text-sm text-white outline-none transition placeholder:text-white/30 focus:border-white/30 disabled:cursor-not-allowed disabled:opacity-50"
            placeholder="Enter amount to subtract"
          />
        </div>

        <div>
          <label className="text-sm font-medium text-white/70">
            Reason required
          </label>

          <textarea
            value={reason}
            disabled={disabled || submitting}
            onChange={(event) => onReasonChange(event.target.value)}
            rows={3}
            className="mt-2 w-full resize-none rounded-2xl border border-white/10 bg-black/40 px-4 py-3 text-sm text-white outline-none transition placeholder:text-white/30 focus:border-white/30 disabled:cursor-not-allowed disabled:opacity-50"
            placeholder="Explain why this correction is needed..."
          />
        </div>

        <button
          type="button"
          disabled={disabled || submitting}
          onClick={onSubmit}
          className="inline-flex w-full items-center justify-center gap-2 rounded-full bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {submitting && <Loader2 className="h-4 w-4 animate-spin" />}
          Save Correction
        </button>
      </div>
    </div>
  )
}