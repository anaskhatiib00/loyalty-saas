import { AlertTriangle } from "lucide-react"

type Props = {
  title: string
  description: string
  icon: React.ElementType
  selected: boolean
  disabled: boolean
  onClick: () => void
}

export function PrimaryAction({
  title,
  description,
  icon: Icon,
  selected,
  disabled,
  onClick,
}: Props) {
  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={
        selected
          ? "w-full rounded-3xl border border-white bg-white p-6 text-left text-black transition disabled:cursor-not-allowed disabled:opacity-50"
          : "w-full rounded-3xl border border-white/10 bg-black/30 p-6 text-left text-white transition hover:bg-white/5 disabled:cursor-not-allowed disabled:opacity-50"
      }
    >
      <div className="flex items-start justify-between gap-6">
        <div>
          <p
            className={
              selected
                ? "text-xs font-medium uppercase tracking-[0.2em] text-black/50"
                : "text-xs font-medium uppercase tracking-[0.2em] text-white/40"
            }
          >
            Recommended Action
          </p>

          <h2 className="mt-3 text-3xl font-bold">{title}</h2>

          <p
            className={
              selected
                ? "mt-3 text-sm text-black/60"
                : "mt-3 text-sm text-white/50"
            }
          >
            {description}
          </p>
        </div>

        <div
          className={
            selected
              ? "rounded-2xl bg-black/10 p-4"
              : "rounded-2xl bg-white/10 p-4"
          }
        >
          <Icon className="h-8 w-8" />
        </div>
      </div>

      {disabled && (
        <div className="mt-6 flex items-center gap-2 rounded-2xl border border-amber-500/20 bg-amber-500/10 p-3 text-sm text-amber-300">
          <AlertTriangle className="h-4 w-4" />
          This action is unavailable for this customer.
        </div>
      )}
    </button>
  )
}