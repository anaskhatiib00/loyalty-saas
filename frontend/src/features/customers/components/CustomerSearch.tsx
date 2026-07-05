"use client"

import { Search } from "lucide-react"

type CustomerSearchProps = {
  value: string
  onChange: (value: string) => void
}

export function CustomerSearch({
  value,
  onChange,
}: CustomerSearchProps) {
  return (
    <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3">
      <Search className="h-4 w-4 text-white/40" />

      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search customers..."
        className="w-full bg-transparent text-sm outline-none placeholder:text-white/35"
      />
    </div>
  )
}