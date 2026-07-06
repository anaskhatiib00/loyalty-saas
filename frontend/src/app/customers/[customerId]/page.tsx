"use client"

import { useCallback, useEffect, useState } from "react"
import { useParams, useRouter } from "next/navigation"

import { DashboardShell } from "@/components/layout/DashboardShell"

import {
  CustomerActivityTimeline,
  CustomerProfileHeader,
  CustomerProgressPanel,
  CustomerWalletPanel,
  customerService,
  type Customer,
} from "@/features/customers"

export default function CustomerDetailsPage() {
  const params = useParams()
  const router = useRouter()

  const customerId = Number(params.customerId)

  const [customer, setCustomer] = useState<Customer | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchCustomer = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)

      const customer = await customerService.getCustomer(customerId)
      setCustomer(customer)
    } catch {
      setError("Could not load customer.")
    } finally {
      setLoading(false)
    }
  }, [customerId])

  useEffect(() => {
    if (customerId) {
      fetchCustomer()
    }
  }, [customerId, fetchCustomer])

  return (
    <DashboardShell>
      <div className="space-y-6">
        {loading && (
          <div className="rounded-3xl border border-white/10 p-10 text-center text-sm text-white/50">
            Loading customer...
          </div>
        )}

        {!loading && error && (
          <div className="rounded-3xl border border-red-500/20 bg-red-500/10 p-5 text-sm text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && customer && (
          <>
            <CustomerProfileHeader
              customer={customer}
              onCustomerUpdated={fetchCustomer}
              onCustomerDeleted={() => router.push("/customers")}
            />

            <div className="grid gap-6 xl:grid-cols-2">
              <CustomerWalletPanel />
              <CustomerProgressPanel />
            </div>

            <CustomerActivityTimeline />
          </>
        )}
      </div>
    </DashboardShell>
  )
}