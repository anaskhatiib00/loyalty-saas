"use client"

import { useMemo, useState } from "react"
import { useSearchParams } from "next/navigation"
import { AlertTriangle, CreditCard, LoaderCircle } from "lucide-react"

import {
  AcceptInvitationForm,
  EmployeeInvitationPreview,
  InvitationAccepted,
  useEmployeeInvitationPreview,
  type AcceptEmployeeInvitationResponse,
} from "@/features/identity/employee"

export function EmployeeInvitationAcceptanceContent() {
  const searchParams = useSearchParams()

  const token = useMemo(
    () => searchParams.get("token") ?? "",
    [searchParams]
  )

  const [result, setResult] =
    useState<AcceptEmployeeInvitationResponse | null>(null)

  const {
    preview,
    isLoading,
    error,
  } = useEmployeeInvitationPreview(token)

  return (
    <main className="flex min-h-screen items-center justify-center bg-black px-6 py-16 text-white">
      <div className="w-full max-w-lg rounded-3xl border border-white/10 bg-white/[0.03] p-8 shadow-2xl">
        <div className="mb-8 flex items-center gap-4 border-b border-white/10 pb-6">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white text-black">
            <CreditCard className="h-5 w-5" />
          </div>

          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-white/45">
              Loyalty SaaS
            </p>

            <h1 className="mt-1 text-3xl font-semibold tracking-tight">
              Employee Invitation
            </h1>
          </div>
        </div>

        {result ? (
          <InvitationAccepted result={result} />
        ) : isLoading ? (
          <div className="flex min-h-48 flex-col items-center justify-center text-center">
            <LoaderCircle className="mb-4 h-7 w-7 animate-spin text-white/70" />

            <p className="font-medium text-white">
              Loading invitation
            </p>

            <p className="mt-2 text-sm text-white/50">
              Please wait while we verify your invitation.
            </p>
          </div>
        ) : error ? (
          <div className="rounded-2xl border border-red-400/20 bg-red-400/10 p-5">
            <div className="flex items-start gap-3">
              <AlertTriangle className="mt-0.5 h-5 w-5 shrink-0 text-red-300" />

              <div>
                <p className="font-medium text-red-100">
                  Invitation unavailable
                </p>

                <p className="mt-1 text-sm leading-6 text-red-100/70">
                  {error}
                </p>
              </div>
            </div>
          </div>
        ) : preview ? (
          <>
            <EmployeeInvitationPreview preview={preview} />

            <AcceptInvitationForm
              token={token}
              onAccepted={setResult}
            />
          </>
        ) : null}
      </div>
    </main>
  )
}