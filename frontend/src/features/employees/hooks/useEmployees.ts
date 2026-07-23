"use client"

import { useCallback, useEffect, useMemo, useState } from "react"

import { employeesService } from "../services/employees.service"
import type { Employee } from "../types/employees"

export function useEmployees() {
  const [employees, setEmployees] = useState<Employee[]>([])
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const refreshEmployees = useCallback(async () => {
    const employees = await employeesService.listEmployees()

    setEmployees(employees)
  }, [])

  useEffect(() => {
    async function fetchEmployees() {
      try {
        setLoading(true)
        setError(null)

        await refreshEmployees()
      } catch {
        setError("Could not load employees.")
      } finally {
        setLoading(false)
      }
    }

    void fetchEmployees()
  }, [refreshEmployees])

  const filteredEmployees = useMemo(() => {
    const query = search.trim().toLowerCase()

    if (!query) {
      return employees
    }

    return employees.filter((employee) => {
      return (
        employee.full_name.toLowerCase().includes(query) ||
        employee.email?.toLowerCase().includes(query) ||
        employee.phone?.toLowerCase().includes(query) ||
        employee.role.toLowerCase().includes(query) ||
        employee.status.toLowerCase().includes(query)
      )
    })
  }, [employees, search])

  const employeeStats = useMemo(() => {
    return {
      total: employees.length,
      active: employees.filter(
        (employee) => employee.status === "active"
      ).length,
      invited: employees.filter(
        (employee) => employee.status === "invited"
      ).length,
      inactive: employees.filter(
        (employee) => employee.status === "inactive"
      ).length,
    }
  }, [employees])

  return {
    search,
    setSearch,
    loading,
    error,
    employees: filteredEmployees,
    employeeStats,
    refreshEmployees,
  }
}