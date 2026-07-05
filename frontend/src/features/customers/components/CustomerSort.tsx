"use client"

type CustomerSortValue = "newest" | "oldest" | "name_asc" | "name_desc"

type CustomerSortProps = {
  value: CustomerSortValue
  onChange: (value: CustomerSortValue) => void
}

export function CustomerSort({ value, onChange }: CustomerSortProps) {
  return (
    <select
      value={value}
      onChange={(event) => onChange(event.target.value as CustomerSortValue)}
      className="rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3 text-sm text-white outline-none"
    >
      <option value="newest" className="bg-black">
        Newest
      </option>
      <option value="oldest" className="bg-black">
        Oldest
      </option>
      <option value="name_asc" className="bg-black">
        Name A-Z
      </option>
      <option value="name_desc" className="bg-black">
        Name Z-A
      </option>
    </select>
  )
}