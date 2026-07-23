export function EmployeesLoadingState() {
  return (
    <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03]">
      {[1, 2, 3].map((item) => (
        <div
          key={item}
          className="grid gap-4 border-b border-white/10 px-6 py-5 last:border-b-0 md:grid-cols-[1.5fr_1.4fr_1fr_1fr]"
        >
          <div className="h-10 animate-pulse rounded-xl bg-white/[0.06]" />
          <div className="h-10 animate-pulse rounded-xl bg-white/[0.06]" />
          <div className="h-8 animate-pulse rounded-xl bg-white/[0.06]" />
          <div className="h-8 animate-pulse rounded-xl bg-white/[0.06]" />
        </div>
      ))}
    </div>
  )
}