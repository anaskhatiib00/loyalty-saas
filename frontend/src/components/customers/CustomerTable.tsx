import { Customer } from "@/types/customer"

type CustomerTableProps = {
  customers: Customer[]
}

export function CustomerTable({ customers }: CustomerTableProps) {
  if (customers.length === 0) {
    return (
      <div className="rounded-3xl border border-dashed border-white/10 p-10 text-center">
        <h3 className="text-lg font-semibold text-white">No customers yet</h3>
        <p className="mt-2 text-sm text-white/50">
          Add your first customer to start tracking loyalty progress.
        </p>
      </div>
    )
  }

  return (
    <div className="overflow-hidden rounded-3xl border border-white/10">
      <table className="w-full text-left text-sm text-white">
        <thead className="border-b border-white/10 bg-white/[0.03] text-white/50">
          <tr>
            <th className="px-5 py-4 font-medium">Customer</th>
            <th className="px-5 py-4 font-medium">Email</th>
            <th className="px-5 py-4 font-medium">Phone</th>
            <th className="px-5 py-4 font-medium">Status</th>
          </tr>
        </thead>

        <tbody>
          {customers.map((customer) => (
            <tr
              key={customer.id}
              className="border-b border-white/5 last:border-0 hover:bg-white/[0.03]"
            >
              <td className="px-5 py-4 font-medium">
                {customer.first_name} {customer.last_name || ""}
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
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}