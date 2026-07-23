"use client"

import { useEffect, useState } from "react"
import { AxiosError } from "axios"
import { Check, Copy, ExternalLink } from "lucide-react"
import { toast } from "sonner"

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

import {
  EmployeeForm,
  employeesService,
  type CreateEmployeeInvitationInput,
  type CreateEmployeeInvitationResponse,
} from "@/features/employees"
import {
  locationsService,
  type Location,
} from "@/features/locations"

type CreateEmployeeDialogProps = {
  trigger: React.ReactNode
  onEmployeeCreated?: () => void | Promise<void>
}

type BackendValidationError = {
  detail?: string | { msg?: string }[]
}

function getErrorMessage(error: unknown) {
  if (error instanceof AxiosError) {
    const data = error.response?.data as BackendValidationError | undefined

    if (typeof data?.detail === "string") {
      return data.detail
    }

    if (Array.isArray(data?.detail)) {
      return data.detail[0]?.msg || "Invalid employee information."
    }

    if (error.response?.status === 404) {
      return "The selected location could not be found."
    }

    if (error.response?.status === 409) {
      return "An employee or invitation with this email already exists."
    }

    if (error.response?.status === 422) {
      return "Please check the required fields."
    }
  }

  return "Could not create the employee invitation."
}

export function CreateEmployeeDialog({
  trigger,
  onEmployeeCreated,
}: CreateEmployeeDialogProps) {
  const [open, setOpen] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [loadingLocations, setLoadingLocations] = useState(false)
  const [locations, setLocations] = useState<Location[]>([])
  const [locationError, setLocationError] = useState<string | null>(null)
  const [invitationResult, setInvitationResult] =
    useState<CreateEmployeeInvitationResponse | null>(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    if (!open) {
      return
    }

    async function loadLocations() {
      try {
        setLoadingLocations(true)
        setLocationError(null)

        const availableLocations = await locationsService.listLocations()

        setLocations(availableLocations)
      } catch {
        setLocationError("Could not load business locations.")
      } finally {
        setLoadingLocations(false)
      }
    }

    void loadLocations()
  }, [open])

  function handleOpenChange(nextOpen: boolean) {
    setOpen(nextOpen)

    if (!nextOpen) {
      setInvitationResult(null)
      setCopied(false)
    }
  }

  async function handleCreateEmployee(
    data: CreateEmployeeInvitationInput
  ) {
    try {
      setSubmitting(true)

      const result = await employeesService.createInvitation(data)

      setInvitationResult(result)

      toast.success("Employee invitation created successfully.")

      await onEmployeeCreated?.()
    } catch (error) {
      toast.error(getErrorMessage(error))
    } finally {
      setSubmitting(false)
    }
  }

  async function handleCopyInvitationLink() {
    const invitationUrl = invitationResult?.development_accept_url

    if (!invitationUrl) {
      return
    }

    try {
      await navigator.clipboard.writeText(invitationUrl)
      setCopied(true)
      toast.success("Invitation link copied.")

      window.setTimeout(() => {
        setCopied(false)
      }, 2000)
    } catch {
      toast.error("Could not copy the invitation link.")
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>

      <DialogContent className="max-w-2xl border-white/10 bg-neutral-950 text-white">
        <DialogHeader>
          <DialogTitle className="text-2xl">
            {invitationResult
              ? "Invitation Created"
              : "Invite Employee"}
          </DialogTitle>
        </DialogHeader>

        {invitationResult ? (
          <div className="space-y-5">
            <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/10 p-4">
              <div className="flex items-start gap-3">
                <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-emerald-500/15">
                  <Check className="h-4 w-4 text-emerald-300" />
                </div>

                <div>
                  <p className="font-medium text-emerald-200">
                    The employee invitation is ready.
                  </p>

                  <p className="mt-1 text-sm leading-6 text-emerald-100/60">
                    The employee has been added with invited status and can
                    activate their account using the invitation.
                  </p>
                </div>
              </div>
            </div>

            <div className="rounded-2xl border border-white/10 bg-white/[0.03] p-4">
              <p className="text-sm text-white/50">
                Invitation email
              </p>

              <p className="mt-1 break-all text-sm text-white">
                {invitationResult.invitation.email}
              </p>

              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <div>
                  <p className="text-xs uppercase tracking-wide text-white/35">
                    Role
                  </p>

                  <p className="mt-1 text-sm capitalize text-white/80">
                    {invitationResult.invitation.role}
                  </p>
                </div>

                <div>
                  <p className="text-xs uppercase tracking-wide text-white/35">
                    Delivery
                  </p>

                  <p className="mt-1 text-sm capitalize text-white/80">
                    {invitationResult.delivery_status}
                  </p>
                </div>
              </div>
            </div>

            {invitationResult.development_accept_url && (
              <div className="space-y-3 rounded-2xl border border-amber-500/20 bg-amber-500/10 p-4">
                <div>
                  <p className="font-medium text-amber-100">
                    Development invitation link
                  </p>

                  <p className="mt-1 text-sm leading-6 text-amber-100/60">
                    Email delivery is not active in development mode. Copy
                    this link and open it to test employee account
                    activation.
                  </p>
                </div>

                <div className="rounded-xl border border-white/10 bg-black/30 p-3">
                  <p className="break-all text-xs leading-5 text-white/60">
                    {invitationResult.development_accept_url}
                  </p>
                </div>

                <div className="flex flex-col gap-3 sm:flex-row">
                  <button
                    type="button"
                    onClick={handleCopyInvitationLink}
                    className="inline-flex items-center justify-center gap-2 rounded-full border border-white/10 px-4 py-2.5 text-sm text-white/80 transition hover:bg-white/10 hover:text-white"
                  >
                    {copied ? (
                      <Check className="h-4 w-4" />
                    ) : (
                      <Copy className="h-4 w-4" />
                    )}

                    {copied ? "Copied" : "Copy Link"}
                  </button>

                  <a
                    href={invitationResult.development_accept_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center justify-center gap-2 rounded-full bg-white px-4 py-2.5 text-sm font-medium text-black transition hover:bg-white/90"
                  >
                    <ExternalLink className="h-4 w-4" />
                    Open Invitation
                  </a>
                </div>
              </div>
            )}

            <div className="flex justify-end">
              <button
                type="button"
                onClick={() => handleOpenChange(false)}
                className="rounded-full bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-white/90"
              >
                Done
              </button>
            </div>
          </div>
        ) : (
          <>
            {locationError && (
              <div className="rounded-2xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                {locationError}
              </div>
            )}

            {loadingLocations ? (
              <div className="space-y-4">
                {[1, 2, 3].map((item) => (
                  <div
                    key={item}
                    className="h-12 animate-pulse rounded-2xl bg-white/[0.06]"
                  />
                ))}
              </div>
            ) : (
              <EmployeeForm
                locations={locations}
                onSubmit={handleCreateEmployee}
                onCancel={() => handleOpenChange(false)}
                submitting={submitting}
              />
            )}
          </>
        )}
      </DialogContent>
    </Dialog>
  )
}
