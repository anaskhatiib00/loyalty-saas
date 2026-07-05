import type { Customer } from "@/features/customers"
import { CustomerActions } from "@/features/customers"

type CustomerTableProps = {
  customers: Customer[]
}

export function CustomerTable({ customers }: CustomerTableProps) {
  return (
    <div className="overflow-hidden rounded-3xl border border-white/10">
      <table className="w-full text-left text-sm text-white">
        <thead className="border-b border-white/10 bg-white/[0.03] text-white/50">
          <tr>
            <th className="px-5 py-4 font-medium">Customer</th>
            <th className="px-5 py-4 font-medium">Email</th>
            <th className="px-5 py-4 font-medium">Phone</th>
            <th className="px-5 py-4 font-medium">Status</th>
            <th className="w-20 px-5 py-4 text-right font-medium">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {customers.map((customer) => (
            <tr
              key={customer.id}
              className="border-b border-white/5 transition hover:bg-white/[0.03] last:border-0"
            >
              <td className="px-5 py-4 font-medium">
                {customer.first_name} {customer.last_name ?? ""}
              </td>

              <td className="px-5 py-4 text-white/60">
                {customer.email || "—"}
              </td>

              <td className="px-5 py-4 text-white/60">
                {customer.phone || "—"}
              </td>

              <td className="px-5 py-4">
                <span className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-300">
                  Active
                </span>
              </td>

              <td className="px-5 py-4 text-right">
                <CustomerActions customer={customer} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}