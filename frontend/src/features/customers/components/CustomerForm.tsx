"use client"

import { useState } from "react"

import type { CreateCustomerInput, Customer } from "@/features/customers"

type CustomerFormState = {
  first_name: string
  last_name: string
  email: string
  phone: string
  date_of_birth: string
}

type CustomerFormProps = {
  customer?: Customer
  submitLabel?: string
  submittingLabel?: string
  onSubmit: (data: CreateCustomerInput) => Promise<void>
  onCancel: () => void
  submitting?: boolean
}

export function CustomerForm({
  customer,
  submitLabel = "Create customer",
  submittingLabel = "Saving...",
  onSubmit,
  onCancel,
  submitting = false,
}: CustomerFormProps) {
  const [formData, setFormData] = useState<CustomerFormState>({
    first_name: customer?.first_name ?? "",
    last_name: customer?.last_name ?? "",
    email: customer?.email ?? "",
    phone: customer?.phone ?? "",
    date_of_birth: customer?.date_of_birth ?? "",
  })

  function updateField(field: keyof CustomerFormState, value: string) {
    setFormData((current) => ({
      ...current,
      [field]: value,
    }))
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()

    await onSubmit({
      location_id: 3,
      first_name: formData.first_name.trim(),
      last_name: formData.last_name.trim(),
      email: formData.email.trim() || undefined,
      phone: formData.phone.trim(),
      date_of_birth: formData.date_of_birth,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <p className="rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3 text-sm text-white/50">
        Fields marked with <span className="text-red-400">*</span> are required.
      </p>

      <div className="grid gap-4 md:grid-cols-2">
        <div>
          <label className="text-sm text-white/60">
            First name <span className="text-red-400">*</span>
          </label>
          <input
            required
            value={formData.first_name}
            onChange={(event) => updateField("first_name", event.target.value)}
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none placeholder:text-white/30 focus:border-white/30"
            placeholder="Ahmad"
          />
        </div>

        <div>
          <label className="text-sm text-white/60">
            Last name <span className="text-red-400">*</span>
          </label>
          <input
            required
            value={formData.last_name}
            onChange={(event) => updateField("last_name", event.target.value)}
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none placeholder:text-white/30 focus:border-white/30"
            placeholder="Saleh"
          />
        </div>

        <div>
          <label className="text-sm text-white/60">Email</label>
          <input
            type="email"
            value={formData.email}
            onChange={(event) => updateField("email", event.target.value)}
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none placeholder:text-white/30 focus:border-white/30"
            placeholder="customer@example.com"
          />
        </div>

        <div>
          <label className="text-sm text-white/60">
            Phone number <span className="text-red-400">*</span>
          </label>
          <input
            required
            value={formData.phone}
            onChange={(event) => updateField("phone", event.target.value)}
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none placeholder:text-white/30 focus:border-white/30"
            placeholder="+1 555 123 4567"
          />
        </div>

        <div>
          <label className="text-sm text-white/60">
            Date of birth <span className="text-red-400">*</span>
          </label>
          <input
            required
            type="date"
            value={formData.date_of_birth}
            onChange={(event) =>
              updateField("date_of_birth", event.target.value)
            }
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none focus:border-white/30"
          />
        </div>
      </div>

      <div className="flex flex-col-reverse gap-3 pt-2 sm:flex-row sm:justify-end">
        <button
          type="button"
          onClick={onCancel}
          className="rounded-full border border-white/10 px-5 py-2.5 text-sm text-white/70 transition hover:bg-white/10 hover:text-white"
        >
          Cancel
        </button>

        <button
          type="submit"
          disabled={submitting}
          className="rounded-full bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {submitting ? submittingLabel : submitLabel}
        </button>
      </div>
    </form>
  )
}