"use client"

import { useRouter } from "next/navigation"

import type { Customer } from "@/features/customers"
import { CustomerActions } from "@/features/customers"

type CustomerTableProps = {
  customers: Customer[]
  selectedCustomerIds: number[]
  allPageSelected: boolean
  onToggleCustomer: (customerId: number) => void
  onTogglePageSelection: () => void
  onCustomerDeleted?: () => void
}

export function CustomerTable({
  customers,
  selectedCustomerIds,
  allPageSelected,
  onToggleCustomer,
  onTogglePageSelection,
  onCustomerDeleted,
}: CustomerTableProps) {
  const router = useRouter()

  return (
    <div className="overflow-hidden rounded-3xl border border-white/10">
      <table className="w-full text-left text-sm text-white">
        <thead className="border-b border-white/10 bg-white/[0.03] text-white/50">
          <tr>
            <th className="w-12 px-5 py-4">
              <input
                type="checkbox"
                checked={allPageSelected}
                onChange={onTogglePageSelection}
                className="h-4 w-4 rounded border-white/20 bg-black"
              />
            </th>
            <th className="px-5 py-4 font-medium">Customer</th>
            <th className="px-5 py-4 font-medium">Email</th>
            <th className="px-5 py-4 font-medium">Phone</th>
            <th className="px-5 py-4 font-medium">Status</th>
            <th className="w-20 px-5 py-4 text-right font-medium">Actions</th>
          </tr>
        </thead>

        <tbody>
          {customers.map((customer) => {
            const selected = selectedCustomerIds.includes(customer.id)

            return (
              <tr
                key={customer.id}
                onClick={() => router.push(`/customers/${customer.id}`)}
                className={`group cursor-pointer border-b border-l-2 border-white/5 transition-all duration-200 last:border-b-0 ${
                  selected
                    ? "border-l-white bg-white/[0.07]"
                    : "border-l-transparent hover:border-l-white hover:bg-white/[0.05]"
                }`}
              >
                <td
                  className="px-5 py-4"
                  onClick={(event) => event.stopPropagation()}
                >
                  <input
                    type="checkbox"
                    checked={selected}
                    onChange={() => onToggleCustomer(customer.id)}
                    className="h-4 w-4 rounded border-white/20 bg-black"
                  />
                </td>

                <td className="px-5 py-4 font-medium text-white/90 transition-colors duration-200 group-hover:text-white">
                  {customer.first_name} {customer.last_name ?? ""}
                </td>

                <td className="px-5 py-4 text-white/60 transition-colors duration-200 group-hover:text-white/80">
                  {customer.email || "—"}
                </td>

                <td className="px-5 py-4 text-white/60 transition-colors duration-200 group-hover:text-white/80">
                  {customer.phone || "—"}
                </td>

                <td className="px-5 py-4">
                  <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-300 transition-all duration-200 group-hover:border-emerald-400/40 group-hover:bg-emerald-400/20">
                    Active
                  </span>
                </td>

                <td className="px-5 py-4 text-right">
                  <CustomerActions
                    customer={customer}
                    onCustomerDeleted={onCustomerDeleted}
                  />
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}