export function CustomerLoadingSkeleton() {
  return (
    <div className="overflow-hidden rounded-3xl border border-white/10">
      <div className="border-b border-white/10 bg-white/[0.03] px-5 py-4">
        <div className="h-4 w-40 animate-pulse rounded-full bg-white/10" />
      </div>

      <div className="divide-y divide-white/5">
        {Array.from({ length: 6 }).map((_, index) => (
          <div key={index} className="grid gap-4 px-5 py-4 md:grid-cols-4">
            <div className="h-4 animate-pulse rounded-full bg-white/10" />
            <div className="h-4 animate-pulse rounded-full bg-white/10" />
            <div className="h-4 animate-pulse rounded-full bg-white/10" />
            <div className="h-4 w-20 animate-pulse rounded-full bg-white/10" />
          </div>
        ))}
      </div>
    </div>
  )
}