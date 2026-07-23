import Link from "next/link"
import { CheckCircle2, LogIn } from "lucide-react"

import type { AcceptEmployeeInvitationResponse } from "../types/employee-identity"

type InvitationAcceptedProps = {
  result: AcceptEmployeeInvitationResponse
}

export function InvitationAccepted({
  result,
}: InvitationAcceptedProps) {
  return (
    <div className="space-y-6 text-center">
      <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full border border-emerald-500/20 bg-emerald-500/10">
        <CheckCircle2
          aria-hidden="true"
          className="h-8 w-8 text-emerald-400"
        />
      </div>

      <div className="space-y-2">
        <h2 className="text-2xl font-semibold text-white">
          Account activated
        </h2>

        <p className="text-sm leading-6 text-white/55">
          Welcome, {result.user.full_name}. Your employee
          account is now active.
        </p>
      </div>

      <div className="rounded-2xl border border-white/10 bg-black/30 px-4 py-3 text-left">
        <p className="text-xs font-medium uppercase tracking-[0.16em] text-white/35">
          Sign-in email
        </p>

        <p className="mt-1 break-all text-sm text-white/80">
          {result.user.email}
        </p>
      </div>

      <p className="text-xs leading-5 text-white/40">
        For security, activation does not automatically sign
        you in. Continue to the login page and use the password
        you just created.
      </p>

      <Link
        href="/login"
        className="flex w-full items-center justify-center gap-2 rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-black transition hover:bg-white/90"
      >
        <LogIn aria-hidden="true" className="h-4 w-4" />
        Continue to login
      </Link>
    </div>
  )
}
