import { Users } from "lucide-react"

type EmployeesEmptyStateProps = {
  hasSearch: boolean
}

export function EmployeesEmptyState({
  hasSearch,
}: EmployeesEmptyStateProps) {
  return (
    <div className="rounded-3xl border border-dashed border-white/15 bg-white/[0.02] px-6 py-16 text-center">
      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl border border-white/10 bg-white/[0.04]">
        <Users className="h-5 w-5 text-white/60" />
      </div>

      <h2 className="mt-5 text-lg font-medium">
        {hasSearch ? "No matching employees" : "No employees yet"}
      </h2>

      <p className="mx-auto mt-2 max-w-md text-sm text-white/45">
        {hasSearch
          ? "Try searching with a different name, email, role or status."
          : "Invite your first employee to give them secure access to the employee POS."}
      </p>
    </div>
  )
}