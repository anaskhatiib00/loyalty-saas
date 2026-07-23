import { Search } from "lucide-react"

type EmployeeSearchProps = {
  value: string
  onChange: (value: string) => void
}

export function EmployeeSearch({
  value,
  onChange,
}: EmployeeSearchProps) {
  return (
    <div className="relative">
      <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-white/40" />

      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Search employees by name, email, role or status"
        aria-label="Search employees"
        className="w-full rounded-2xl border border-white/10 bg-white/[0.03] py-3 pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-white/30 focus:border-white/25 focus:bg-white/[0.05]"
      />
    </div>
  )
}