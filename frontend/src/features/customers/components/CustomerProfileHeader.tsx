import Link from "next/link"
import { ArrowLeft, Mail, Phone } from "lucide-react"

import type { Customer } from "@/features/customers"

type Props = {
  customer: Customer
}

export function CustomerProfileHeader({ customer }: Props) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
      <Link
        href="/customers"
        className="inline-flex items-center gap-2 text-sm text-white/50 hover:text-white"
      >
        <ArrowLeft className="h-4 w-4" />
        Back to customers
      </Link>

      <div className="mt-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 className="text-4xl font-semibold tracking-tight">
            {customer.first_name} {customer.last_name || ""}
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

        <span className="w-fit rounded-full border border-emerald-400/20 bg-emerald-400/10 px-4 py-2 text-sm text-emerald-300">
          Active
        </span>
      </div>
    </div>
  )
}