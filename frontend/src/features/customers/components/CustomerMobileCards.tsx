"use client"

import { useRouter } from "next/navigation"
import { Mail, Phone } from "lucide-react"

import type { Customer } from "@/features/customers"
import { CustomerActions } from "@/features/customers"

type CustomerMobileCardsProps = {
  customers: Customer[]
  selectedCustomerIds: number[]
  onToggleCustomer: (customerId: number) => void
  onCustomerDeleted?: () => void
}

export function CustomerMobileCards({
  customers,
  selectedCustomerIds,
  onToggleCustomer,
  onCustomerDeleted,
}: CustomerMobileCardsProps) {
  const router = useRouter()

  return (
    <div className="space-y-3 md:hidden">
      {customers.map((customer) => {
        const selected = selectedCustomerIds.includes(customer.id)

        return (
          <div
            key={customer.id}
            onClick={() => router.push(`/customers/${customer.id}`)}
            className={`rounded-3xl border p-5 text-white transition ${
              selected
                ? "border-white/30 bg-white/[0.08]"
                : "border-white/10 bg-white/[0.03] hover:bg-white/[0.06]"
            }`}
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex gap-3">
                <div onClick={(event) => event.stopPropagation()}>
                  <input
                    type="checkbox"
                    checked={selected}
                    onChange={() => onToggleCustomer(customer.id)}
                    className="mt-1 h-4 w-4 rounded border-white/20 bg-black"
                  />
                </div>

                <div>
                  <h3 className="font-semibold">
                    {customer.first_name} {customer.last_name ?? ""}
                  </h3>

                  <div className="mt-3 space-y-2 text-sm text-white/50">
                    <p className="flex items-center gap-2">
                      <Mail className="h-4 w-4" />
                      {customer.email || "No email"}
                    </p>

                    <p className="flex items-center gap-2">
                      <Phone className="h-4 w-4" />
                      {customer.phone || "No phone"}
                    </p>
                  </div>
                </div>
              </div>

              <div onClick={(event) => event.stopPropagation()}>
                <CustomerActions
                  customer={customer}
                  onCustomerDeleted={onCustomerDeleted}
                />
              </div>
            </div>

            <div className="mt-4">
              <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-300">
                Active
              </span>
            </div>
          </div>
        )
      })}
    </div>
  )
}