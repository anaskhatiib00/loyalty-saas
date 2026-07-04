"use client"

import { useEffect, useState } from "react"
import { Plus, Search } from "lucide-react"

import { CustomerTable } from "@/components/customers/CustomerTable"
import { DashboardShell } from "@/components/layout/DashboardShell"
import { customerService } from "@/services/customer.service"
import { Customer } from "@/types/customer"

export default function CustomersPage() {
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function fetchCustomers() {
      try {
        setLoading(true)
        const customers = await customerService.getCustomers()
        setCustomers(customers)
      } catch {
        setError("Could not load customers.")
      } finally {
        setLoading(false)
      }
    }

    fetchCustomers()
  }, [])

  return (
    <DashboardShell>
      <div className="space-y-6 text-white">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm text-white/50">Business</p>
            <h1 className="mt-1 text-4xl font-semibold tracking-tight">
              Customers
            </h1>
            <p className="mt-2 text-sm text-white/50">
              Search, manage, and issue wallet passes for your loyalty customers.
            </p>
          </div>

          <button className="inline-flex items-center justify-center gap-2 rounded-full bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-white/90">
            <Plus className="h-4 w-4" />
            New Customer
          </button>
        </div>

        <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3">
          <Search className="h-4 w-4 text-white/40" />
          <input
            placeholder="Search customers..."
            className="w-full bg-transparent text-sm outline-none placeholder:text-white/35"
          />
        </div>

        {loading && (
          <div className="rounded-3xl border border-white/10 p-10 text-center text-sm text-white/50">
            Loading customers...
          </div>
        )}

        {error && (
          <div className="rounded-3xl border border-red-500/20 bg-red-500/10 p-5 text-sm text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && <CustomerTable customers={customers} />}
      </div>
    </DashboardShell>
  )
}