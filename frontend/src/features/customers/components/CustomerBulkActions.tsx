type CustomerBulkActionsProps = {
  selectedCount: number
  onClearSelection: () => void
}

export function CustomerBulkActions({
  selectedCount,
  onClearSelection,
}: CustomerBulkActionsProps) {
  if (selectedCount === 0) {
    return null
  }

  return (
    <div className="flex flex-col gap-3 rounded-3xl border border-white/10 bg-white/[0.04] px-5 py-4 text-sm text-white sm:flex-row sm:items-center sm:justify-between">
      <p>
        <span className="font-medium text-white">{selectedCount}</span>{" "}
        selected
      </p>

      <div className="flex flex-wrap gap-2">
        <button className="rounded-full border border-white/10 px-4 py-2 text-white/70 transition hover:bg-white/10 hover:text-white">
          Issue Wallet
        </button>

        <button className="rounded-full border border-white/10 px-4 py-2 text-white/70 transition hover:bg-white/10 hover:text-white">
          Export
        </button>

        <button
          onClick={onClearSelection}
          className="rounded-full border border-white/10 px-4 py-2 text-white/50 transition hover:bg-white/10 hover:text-white"
        >
          Clear
        </button>
      </div>
    </div>
  )
}