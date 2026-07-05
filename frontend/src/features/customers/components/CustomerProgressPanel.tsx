export function CustomerProgressPanel() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <h2 className="text-lg font-semibold">Loyalty progress</h2>
      <p className="mt-1 text-sm text-white/50">
        Current progress toward the next reward.
      </p>

      <div className="mt-6">
        <div className="flex justify-between text-sm text-white/50">
          <span>Progress</span>
          <span>0 / 10</span>
        </div>

        <div className="mt-3 h-3 overflow-hidden rounded-full bg-white/10">
          <div className="h-full w-0 rounded-full bg-white" />
        </div>
      </div>
    </div>
  )
}