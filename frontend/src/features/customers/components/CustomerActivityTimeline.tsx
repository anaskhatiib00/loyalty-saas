export function CustomerActivityTimeline() {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <h2 className="text-lg font-semibold">Recent activity</h2>
      <p className="mt-1 text-sm text-white/50">
        Customer loyalty activity will appear here.
      </p>

      <div className="mt-6 rounded-2xl border border-dashed border-white/10 p-8 text-center text-sm text-white/40">
        No activity yet
      </div>
    </div>
  )
}