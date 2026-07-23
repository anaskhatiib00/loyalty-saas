import {
  BriefcaseBusiness,
  CalendarClock,
  ShieldCheck,
  UserRound,
} from "lucide-react"

import type { EmployeeInvitationPreview as EmployeeInvitationPreviewData } from "../types/employee-identity"

type Props = {
  preview: EmployeeInvitationPreviewData
}

function formatRole(role: string): string {
  return role
    .split("_")
    .map(
      (part) =>
        part.charAt(0).toUpperCase() +
        part.slice(1).toLowerCase()
    )
    .join(" ")
}

function formatExpiration(expiresAt: string): string {
  const expirationDate = new Date(expiresAt)

  if (Number.isNaN(expirationDate.getTime())) {
    return "Expiration date unavailable"
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(expirationDate)
}

export function EmployeeInvitationPreview({
  preview,
}: Props) {
  const formattedRole = formatRole(preview.role)

  return (
    <section className="mb-7 overflow-hidden rounded-3xl border border-white/10 bg-white/[0.025]">
      <div className="border-b border-white/10 bg-white/[0.035] px-5 py-5">
        <div className="flex items-start gap-3">
          <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl bg-white/10">
            <ShieldCheck className="h-5 w-5 text-white/80" />
          </div>

          <div>
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-white/40">
              You have been invited to join
            </p>

            <h2 className="mt-1 text-2xl font-semibold tracking-tight text-white">
              {preview.business_name}
            </h2>

            <p className="mt-2 text-sm leading-6 text-white/55">
              Confirm your details and create a secure password
              to activate your employee account.
            </p>
          </div>
        </div>
      </div>

      <div className="grid gap-3 p-5 sm:grid-cols-2">
        <div className="rounded-2xl border border-white/10 bg-black/20 p-4">
          <div className="flex items-center gap-2 text-white/45">
            <UserRound className="h-4 w-4" />

            <p className="text-xs font-medium uppercase tracking-[0.14em]">
              Employee
            </p>
          </div>

          <p className="mt-2 font-medium text-white">
            {preview.employee_name}
          </p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-black/20 p-4">
          <div className="flex items-center gap-2 text-white/45">
            <BriefcaseBusiness className="h-4 w-4" />

            <p className="text-xs font-medium uppercase tracking-[0.14em]">
              Assigned role
            </p>
          </div>

          <p className="mt-2 font-medium text-white">
            {formattedRole}
          </p>
        </div>

        <div className="rounded-2xl border border-white/10 bg-black/20 p-4 sm:col-span-2">
          <div className="flex items-center gap-2 text-white/45">
            <CalendarClock className="h-4 w-4" />

            <p className="text-xs font-medium uppercase tracking-[0.14em]">
              Invitation expires
            </p>
          </div>

          <p className="mt-2 font-medium text-white">
            {formatExpiration(preview.expires_at)}
          </p>
        </div>
      </div>
    </section>
  )
}