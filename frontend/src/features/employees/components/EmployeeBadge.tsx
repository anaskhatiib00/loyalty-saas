type EmployeeBadgeProps = {
  value: string
}

export function EmployeeBadge({ value }: EmployeeBadgeProps) {
  const normalizedValue = value.toLowerCase()

  const style =
    normalizedValue === "active"
      ? "border-emerald-500/20 bg-emerald-500/10 text-emerald-300"
      : normalizedValue === "invited"
        ? "border-amber-500/20 bg-amber-500/10 text-amber-300"
        : normalizedValue === "inactive"
          ? "border-red-500/20 bg-red-500/10 text-red-300"
          : "border-white/10 bg-white/[0.04] text-white/70"

  return (
    <span
      className={`inline-flex rounded-full border px-3 py-1 text-xs font-medium capitalize ${style}`}
    >
      {value.replaceAll("_", " ")}
    </span>
  )
}
