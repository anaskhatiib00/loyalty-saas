"use client"

import { useState } from "react"

import type {
  CreateEmployeeInvitationInput,
  EmployeeRole,
} from "@/features/employees"
import type { Location } from "@/features/locations"

type EmployeeFormState = {
  full_name: string
  email: string
  phone: string
  role: Exclude<EmployeeRole, "owner">
  location_id: string
}

type EmployeeFormProps = {
  locations: Location[]
  submitLabel?: string
  submittingLabel?: string
  onSubmit: (data: CreateEmployeeInvitationInput) => Promise<void>
  onCancel: () => void
  submitting?: boolean
}

export function EmployeeForm({
  locations,
  submitLabel = "Send invitation",
  submittingLabel = "Sending invitation...",
  onSubmit,
  onCancel,
  submitting = false,
}: EmployeeFormProps) {
  const [formData, setFormData] = useState<EmployeeFormState>({
    full_name: "",
    email: "",
    phone: "",
    role: "cashier",
    location_id: "",
  })

  function updateField(
    field: keyof EmployeeFormState,
    value: string
  ) {
    setFormData((current) => ({
      ...current,
      [field]: value,
    }))
  }

  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()

    await onSubmit({
      full_name: formData.full_name.trim(),
      email: formData.email.trim(),
      phone: formData.phone.trim() || undefined,
      role: formData.role,
      location_id: formData.location_id
        ? Number(formData.location_id)
        : null,
    })
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      <p className="rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3 text-sm text-white/50">
        Fields marked with{" "}
        <span className="text-red-400">*</span> are required.
      </p>

      <div className="grid gap-4 md:grid-cols-2">
        <div className="md:col-span-2">
          <label
            htmlFor="employee-full-name"
            className="text-sm text-white/60"
          >
            Full name <span className="text-red-400">*</span>
          </label>

          <input
            id="employee-full-name"
            required
            autoComplete="name"
            value={formData.full_name}
            onChange={(event) =>
              updateField("full_name", event.target.value)
            }
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none placeholder:text-white/30 focus:border-white/30"
            placeholder="Omar Saleh"
          />
        </div>

        <div>
          <label
            htmlFor="employee-email"
            className="text-sm text-white/60"
          >
            Email <span className="text-red-400">*</span>
          </label>

          <input
            id="employee-email"
            required
            type="email"
            autoComplete="email"
            value={formData.email}
            onChange={(event) =>
              updateField("email", event.target.value)
            }
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none placeholder:text-white/30 focus:border-white/30"
            placeholder="employee@example.com"
          />
        </div>

        <div>
          <label
            htmlFor="employee-phone"
            className="text-sm text-white/60"
          >
            Phone number
          </label>

          <input
            id="employee-phone"
            type="tel"
            autoComplete="tel"
            value={formData.phone}
            onChange={(event) =>
              updateField("phone", event.target.value)
            }
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none placeholder:text-white/30 focus:border-white/30"
            placeholder="+962 7 9000 0000"
          />
        </div>

        <div>
          <label
            htmlFor="employee-role"
            className="text-sm text-white/60"
          >
            Role <span className="text-red-400">*</span>
          </label>

          <select
            id="employee-role"
            required
            value={formData.role}
            onChange={(event) =>
              updateField("role", event.target.value)
            }
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none focus:border-white/30"
          >
            <option value="cashier">Cashier</option>
            <option value="manager">Manager</option>
          </select>
        </div>

        <div>
          <label
            htmlFor="employee-location"
            className="text-sm text-white/60"
          >
            Assigned location
          </label>

          <select
            id="employee-location"
            value={formData.location_id}
            onChange={(event) =>
              updateField("location_id", event.target.value)
            }
            className="mt-2 w-full rounded-2xl border border-white/10 bg-black px-4 py-3 text-sm text-white outline-none focus:border-white/30"
          >
            <option value="">No location assigned</option>

            {locations.map((location) => (
              <option key={location.id} value={location.id}>
                {location.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      <p className="text-xs leading-5 text-white/40">
        The employee will use the invitation to create a password and
        activate their account. Their assigned location determines where
        they can operate the POS.
      </p>

      <div className="flex flex-col-reverse gap-3 pt-2 sm:flex-row sm:justify-end">
        <button
          type="button"
          onClick={onCancel}
          disabled={submitting}
          className="rounded-full border border-white/10 px-5 py-2.5 text-sm text-white/70 transition hover:bg-white/10 hover:text-white disabled:cursor-not-allowed disabled:opacity-60"
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