import { EmployeeBadge } from "@/features/employees"
import type { Employee } from "@/features/employees"

type EmployeeTableProps = {
  employees: Employee[]
}

export function EmployeeTable({ employees }: EmployeeTableProps) {
  return (
    <div className="overflow-hidden rounded-3xl border border-white/10 bg-white/[0.03]">
      <div className="hidden grid-cols-[1.5fr_1.4fr_1fr_1fr] gap-4 border-b border-white/10 px-6 py-4 text-xs font-medium uppercase tracking-wider text-white/40 md:grid">
        <span>Employee</span>
        <span>Contact</span>
        <span>Role</span>
        <span>Status</span>
      </div>

      <div className="divide-y divide-white/10">
        {employees.map((employee) => (
          <div
            key={employee.id}
            className="grid gap-4 px-6 py-5 transition hover:bg-white/[0.02] md:grid-cols-[1.5fr_1.4fr_1fr_1fr] md:items-center"
          >
            <div>
              <p className="font-medium text-white">{employee.full_name}</p>

              <p className="mt-1 text-xs text-white/40">
                Employee #{employee.id}
              </p>
            </div>

            <div className="text-sm">
              <p className="text-white/75">
                {employee.email || "No email"}
              </p>

              <p className="mt-1 text-xs text-white/40">
                {employee.phone || "No phone number"}
              </p>
            </div>

            <div>
              <EmployeeBadge value={employee.role} />
            </div>

            <div>
              <EmployeeBadge value={employee.status} />
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}