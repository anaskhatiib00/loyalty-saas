"use client"

import { useEffect, useState } from "react"
import axios from "axios"

import { employeeIdentityService } from "../services/employee-identity.service"
import type { EmployeeInvitationPreview } from "../types/employee-identity"

type UseEmployeeInvitationPreviewResult = {
  preview: EmployeeInvitationPreview | null
  isLoading: boolean
  error: string | null
}

function getPreviewErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail

    if (typeof detail === "string") {
      return detail
    }
  }

  return "Could not load this employee invitation."
}

export function useEmployeeInvitationPreview(
  token: string
): UseEmployeeInvitationPreviewResult {
  const [preview, setPreview] =
    useState<EmployeeInvitationPreview | null>(null)
  const [isLoading, setIsLoading] = useState(Boolean(token))
  const [error, setError] = useState<string | null>(
    token ? null : "This invitation link is missing its token."
  )

  useEffect(() => {
    if (!token) {
      return
    }

    let isActive = true

    async function loadPreview() {
      setIsLoading(true)
      setError(null)

      try {
        const invitationPreview =
          await employeeIdentityService.getInvitationPreview(token)

        if (isActive) {
          setPreview(invitationPreview)
        }
      } catch (requestError) {
        if (isActive) {
          setPreview(null)
          setError(getPreviewErrorMessage(requestError))
        }
      } finally {
        if (isActive) {
          setIsLoading(false)
        }
      }
    }

    void loadPreview()

    return () => {
      isActive = false
    }
  }, [token])

  return {
    preview,
    isLoading,
    error,
  }
}