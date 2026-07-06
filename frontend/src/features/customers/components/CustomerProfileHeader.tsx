import Link from "next/link"
import { ArrowLeft, Mail, Phone, Pencil, Trash2 } from "lucide-react"

import {
  DeleteCustomerDialog,
  EditCustomerDialog,
  type Customer,
} from "@/features/customers"

type Props = {
  customer: Customer
  onCustomerUpdated?: () => void
  onCustomerDeleted?: () => void
}

export function CustomerProfileHeader({
  customer,
  onCustomerUpdated,
  onCustomerDeleted,
}: Props) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <Link
        href="/customers"
        className="inline-flex items-center gap-2 text-sm text-white/50 transition hover:text-white"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to customers
      </Link>

      <div className="mt-6 flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <h1 className="text-4xl font-semibold tracking-tight">
            {customer.first_name} {customer.last_name ?? ""}
          </h1>

          <div className="mt-3 flex flex-wrap gap-4 text-sm text-white/50">
            <span className="inline-flex items-center gap-2">
              <Mail className="h-4 w-4" />
              {customer.email || "No email"}
            </span>

            <span className="inline-flex items-center gap-2">
              <Phone className="h-4 w-4" />
              {customer.phone || "No phone"}
            </span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-4 py-2 text-sm text-emerald-300">
            Active
          </span>

          <EditCustomerDialog
            customer={customer}
            onCustomerUpdated={onCustomerUpdated}
            trigger={
              <button className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-white transition hover:bg-white/10">
                <Pencil className="h-4 w-4" />
                Edit Customer
              </button>
            }
          />

          <DeleteCustomerDialog
            customer={customer}
            onCustomerDeleted={onCustomerDeleted}
            trigger={
              <button className="inline-flex items-center gap-2 rounded-full border border-red-500/20 bg-red-500/10 px-4 py-2 text-sm text-red-300 transition hover:bg-red-500/20">
                <Trash2 className="h-4 w-4" />
                Delete
              </button>
            }
          />
        </div>
      </div>
    </div>
  )
}