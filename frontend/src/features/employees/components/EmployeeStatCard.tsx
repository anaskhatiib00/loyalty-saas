import { LucideIcon } from "lucide-react"

type EmployeeStatCardProps = {
  label: string
  value: number
  icon: LucideIcon
}

export function EmployeeStatCard({
  label,
  value,
  icon: Icon,
}: EmployeeStatCardProps) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-5">
      <div className="flex items-center justify-between">
        <p className="text-sm text-white/50">{label}</p>

        <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-2.5">
          <Icon className="h-4 w-4 text-white/70" />
        </div>
      </div>

      <p className="mt-5 text-3xl font-semibold tracking-tight">
        {value}
      </p>
    </div>
  )
}