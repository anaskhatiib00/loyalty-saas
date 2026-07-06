"use client"

import { useEffect, useMemo, useState } from "react"

import {
  customerService,
  type Customer,
} from "@/features/customers"

type CustomerSortValue = "newest" | "oldest" | "name_asc" | "name_desc"

const pageSize = 10

export function useCustomers() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [search, setSearch] = useState("")
  const [sort, setSort] = useState<CustomerSortValue>("newest")
  const [currentPage, setCurrentPage] = useState(1)
  const [selectedCustomerIds, setSelectedCustomerIds] = useState<number[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function refreshCustomers() {
    const customers = await customerService.getCustomers()
    setCustomers(customers)
  }

  useEffect(() => {
    async function fetchCustomers() {
      try {
        setLoading(true)
        setError(null)

        await refreshCustomers()
      } catch {
        setError("Could not load customers.")
      } finally {
        setLoading(false)
      }
    }

    fetchCustomers()
  }, [])

  useEffect(() => {
    setCurrentPage(1)
  }, [search, sort])

  const filteredCustomers = useMemo(() => {
    const query = search.toLowerCase().trim()

    if (!query) return customers

    return customers.filter((customer) => {
      const fullName =
        `${customer.first_name} ${customer.last_name ?? ""}`.toLowerCase()

      return (
        fullName.includes(query) ||
        customer.email?.toLowerCase().includes(query) ||
        customer.phone?.toLowerCase().includes(query)
      )
    })
  }, [customers, search])

  const sortedCustomers = useMemo(() => {
    return [...filteredCustomers].sort((a, b) => {
      const nameA = `${a.first_name} ${a.last_name ?? ""}`.toLowerCase()
      const nameB = `${b.first_name} ${b.last_name ?? ""}`.toLowerCase()

      if (sort === "name_asc") return nameA.localeCompare(nameB)
      if (sort === "name_desc") return nameB.localeCompare(nameA)
      if (sort === "oldest") return (a.id ?? 0) - (b.id ?? 0)

      return (b.id ?? 0) - (a.id ?? 0)
    })
  }, [filteredCustomers, sort])

  const totalPages = Math.ceil(sortedCustomers.length / pageSize)

  const paginatedCustomers = sortedCustomers.slice(
    (currentPage - 1) * pageSize,
    currentPage * pageSize
  )

  const pageCustomerIds = paginatedCustomers.map((customer) => customer.id)

  const allPageSelected =
    pageCustomerIds.length > 0 &&
    pageCustomerIds.every((id) => selectedCustomerIds.includes(id))

  function toggleCustomerSelection(customerId: number) {
    setSelectedCustomerIds((current) =>
      current.includes(customerId)
        ? current.filter((id) => id !== customerId)
        : [...current, customerId]
    )
  }

  function togglePageSelection() {
    const allSelected = pageCustomerIds.every((id) =>
      selectedCustomerIds.includes(id)
    )

    if (allSelected) {
      setSelectedCustomerIds((current) =>
        current.filter((id) => !pageCustomerIds.includes(id))
      )
      return
    }

    setSelectedCustomerIds((current) =>
      Array.from(new Set([...current, ...pageCustomerIds]))
    )
  }

  function clearSelection() {
    setSelectedCustomerIds([])
  }

  return {
    search,
    setSearch,
    sort,
    setSort,
    currentPage,
    setCurrentPage,
    loading,
    error,
    totalPages,
    totalCustomers: sortedCustomers.length,
    paginatedCustomers,
    selectedCustomerIds,
    allPageSelected,
    toggleCustomerSelection,
    togglePageSelection,
    clearSelection,
    refreshCustomers,
  }
}