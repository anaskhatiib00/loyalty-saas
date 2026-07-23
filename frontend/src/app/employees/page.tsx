"use client"

import {
  UserCheck,
  UserMinus,
  UserPlus,
  Users,
} from "lucide-react"

import { DashboardShell } from "@/components/layout/DashboardShell"
import {
  CreateEmployeeDialog,
  EmployeeSearch,
  EmployeeStatCard,
  EmployeeTable,
  EmployeesEmptyState,
  EmployeesLoadingState,
  useEmployees,
} from "@/features/employees"

export default function EmployeesPage() {
  const {
    search,
    setSearch,
    loading,
    error,
    employees,
    employeeStats,
    refreshEmployees,
  } = useEmployees()

  return (
    <DashboardShell>
      <div className="space-y-6 text-white">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm text-white/50">Business</p>

            <h1 className="mt-1 text-4xl font-semibold tracking-tight">
              Employees
            </h1>

            <p className="mt-2 text-sm text-white/50">
              Invite staff, assign roles and manage access to your business.
            </p>
          </div>

          <CreateEmployeeDialog
            onEmployeeCreated={refreshEmployees}
            trigger={
              <button
                type="button"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-white/90"
              >
                <UserPlus className="h-4 w-4" />
                Invite Employee
              </button>
            }
          />
        </div>

        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <EmployeeStatCard
            label="Total Employees"
            value={employeeStats.total}
            icon={Users}
          />

          <EmployeeStatCard
            label="Active"
            value={employeeStats.active}
            icon={UserCheck}
          />

          <EmployeeStatCard
            label="Invited"
            value={employeeStats.invited}
            icon={UserPlus}
          />

          <EmployeeStatCard
            label="Inactive"
            value={employeeStats.inactive}
            icon={UserMinus}
          />
        </div>

        <EmployeeSearch
          value={search}
          onChange={setSearch}
        />

        {loading && <EmployeesLoadingState />}

        {!loading && error && (
          <div className="rounded-3xl border border-red-500/20 bg-red-500/10 p-5 text-sm text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && employees.length === 0 && (
          <EmployeesEmptyState hasSearch={Boolean(search.trim())} />
        )}

        {!loading && !error && employees.length > 0 && (
          <EmployeeTable employees={employees} />
        )}
      </div>
    </DashboardShell>
  )
}
