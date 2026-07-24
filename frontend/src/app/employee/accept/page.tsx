import { Suspense } from "react"
import { LoaderCircle } from "lucide-react"

import { EmployeeInvitationAcceptanceContent } from "./EmployeeInvitationAcceptanceContent"

function EmployeeInvitationAcceptanceFallback() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-black px-6 py-16 text-white">
      <div className="flex min-h-48 w-full max-w-lg flex-col items-center justify-center rounded-3xl border border-white/10 bg-white/[0.03] p-8 text-center shadow-2xl">
        <LoaderCircle className="mb-4 h-7 w-7 animate-spin text-white/70" />

        <p className="font-medium text-white">
          Loading invitation
        </p>

        <p className="mt-2 text-sm text-white/50">
          Please wait while we prepare the invitation.
        </p>
      </div>
    </main>
  )
}

export default function EmployeeInvitationAcceptancePage() {
  return (
    <Suspense fallback={<EmployeeInvitationAcceptanceFallback />}>
      <EmployeeInvitationAcceptanceContent />
    </Suspense>
  )
}