"use client"

import { useState, type FormEvent } from "react"
import axios from "axios"
import { Eye, EyeOff, LoaderCircle, LockKeyhole } from "lucide-react"

import { employeeIdentityService } from "../services/employee-identity.service"
import type { AcceptEmployeeInvitationResponse } from "../types/employee-identity"

type AcceptInvitationFormProps = {
  token: string
  onAccepted: (
    response: AcceptEmployeeInvitationResponse
  ) => void
}

function getInvitationErrorMessage(error: unknown): string {
  if (!axios.isAxiosError(error)) {
    return "Something went wrong. Please try again."
  }

  const detail = error.response?.data?.detail

  if (typeof detail === "string") {
    return detail
  }

  if (error.response?.status === 400) {
    return "This invitation is invalid, expired, or has already been accepted."
  }

  if (error.response?.status === 422) {
    return "Please check your password and try again."
  }

  return "We could not activate your account. Please try again."
}

export function AcceptInvitationForm({
  token,
  onAccepted,
}: AcceptInvitationFormProps) {
  const [password, setPassword] = useState("")
  const [confirmPassword, setConfirmPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(
    event: FormEvent<HTMLFormElement>
  ) {
    event.preventDefault()
    setError(null)

    if (!token) {
      setError(
        "This invitation link is missing its security token."
      )
      return
    }

    if (password.length < 8) {
      setError(
        "Your password must contain at least 8 characters."
      )
      return
    }

    if (password !== confirmPassword) {
      setError("The passwords do not match.")
      return
    }

    try {
      setIsSubmitting(true)

      const response =
        await employeeIdentityService.acceptInvitation({
          token,
          password,
        })

      onAccepted(response)
    } catch (submitError) {
      setError(getInvitationErrorMessage(submitError))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-5"
      noValidate
    >
      <div>
        <label
          htmlFor="password"
          className="text-sm font-medium text-white/70"
        >
          Create password
        </label>

        <div className="relative mt-2">
          <LockKeyhole
            aria-hidden="true"
            className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-white/35"
          />

          <input
            id="password"
            type={showPassword ? "text" : "password"}
            autoComplete="new-password"
            minLength={8}
            value={password}
            onChange={(event) =>
              setPassword(event.target.value)
            }
            disabled={isSubmitting}
            placeholder="Minimum 8 characters"
            className="w-full rounded-2xl border border-white/10 bg-black/40 py-3 pl-11 pr-12 text-sm text-white outline-none transition placeholder:text-white/25 focus:border-white/30 disabled:cursor-not-allowed disabled:opacity-60"
            required
          />

          <button
            type="button"
            onClick={() =>
              setShowPassword((current) => !current)
            }
            disabled={isSubmitting}
            aria-label={
              showPassword
                ? "Hide password"
                : "Show password"
            }
            className="absolute right-4 top-1/2 -translate-y-1/2 text-white/40 transition hover:text-white disabled:cursor-not-allowed"
          >
            {showPassword ? (
              <EyeOff
                aria-hidden="true"
                className="h-4 w-4"
              />
            ) : (
              <Eye
                aria-hidden="true"
                className="h-4 w-4"
              />
            )}
          </button>
        </div>
      </div>

      <div>
        <label
          htmlFor="confirm-password"
          className="text-sm font-medium text-white/70"
        >
          Confirm password
        </label>

        <div className="relative mt-2">
          <LockKeyhole
            aria-hidden="true"
            className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-white/35"
          />

          <input
            id="confirm-password"
            type={showPassword ? "text" : "password"}
            autoComplete="new-password"
            minLength={8}
            value={confirmPassword}
            onChange={(event) =>
              setConfirmPassword(event.target.value)
            }
            disabled={isSubmitting}
            placeholder="Enter the password again"
            className="w-full rounded-2xl border border-white/10 bg-black/40 py-3 pl-11 pr-4 text-sm text-white outline-none transition placeholder:text-white/25 focus:border-white/30 disabled:cursor-not-allowed disabled:opacity-60"
            required
          />
        </div>
      </div>

      <p className="text-xs leading-5 text-white/40">
        Use at least 8 characters. Choose a password that
        you do not use for another account.
      </p>

      {error && (
        <div
          role="alert"
          className="rounded-2xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm leading-6 text-red-300"
        >
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={isSubmitting || !token}
        className="flex w-full items-center justify-center gap-2 rounded-2xl bg-white px-4 py-3 text-sm font-semibold text-black transition hover:bg-white/90 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {isSubmitting && (
          <LoaderCircle
            aria-hidden="true"
            className="h-4 w-4 animate-spin"
          />
        )}

        {isSubmitting
          ? "Activating account..."
          : "Activate account"}
      </button>
    </form>
  )
}