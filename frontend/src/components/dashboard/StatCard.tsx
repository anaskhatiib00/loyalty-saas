import { LucideIcon } from "lucide-react"

type StatCardProps = {
  title: string
  value: string
  change: string
  icon: LucideIcon
}

export function StatCard({ title, value, change, icon: Icon }: StatCardProps) {
  return (
    <div className="group rounded-3xl border border-white/10 bg-white/[0.035] p-5 text-white transition hover:-translate-y-0.5 hover:border-white/20 hover:bg-white/[0.06]">
      <div className="flex items-center justify-between">
        <p className="text-sm text-white/50">{title}</p>
        <div className="rounded-xl border border-white/10 p-2 text-white/40 group-hover:text-white">
          <Icon className="h-4 w-4" />
        </div>
      </div>

      <p className="mt-5 text-3xl font-semibold tracking-tight">{value}</p>
      <p className="mt-2 text-sm text-emerald-400">{change}</p>
    </div>
  )
}