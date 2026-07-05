import { Plus, Users } from "lucide-react"

export function CustomerEmptyState() {
  return (
    <div className="rounded-3xl border border-dashed border-white/10 p-12 text-center">
      <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-3xl bg-white/5">
        <Users className="h-7 w-7 text-white/60" />
      </div>

      <h3 className="mt-5 text-lg font-semibold text-white">
        No customers yet
      </h3>

      <p className="mx-auto mt-2 max-w-md text-sm leading-6 text-white/50">
        Start growing your loyalty program by adding your first customer.
      </p>

      <button className="mt-6 inline-flex items-center justify-center gap-2 rounded-full bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-white/90">
        <Plus className="h-4 w-4" />
        New Customer
      </button>
    </div>
  )
}