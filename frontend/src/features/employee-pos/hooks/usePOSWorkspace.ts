"use client"

import { useEffect, useMemo, useState } from "react"

import { employeePOSService } from "../services/employee-pos.service"
import type { POSWorkspaceContext } from "../types/employee-pos"

export function usePOSWorkspace() {
  const [workspaceContext, setWorkspaceContext] =
    useState<POSWorkspaceContext | null>(null)

  const [isLoadingContext, setIsLoadingContext] = useState(true)

  const [contextError, setContextError] = useState<string | null>(
    null
  )

  useEffect(() => {
    let isActive = true

    async function loadWorkspaceContext() {
      try {
        const result =
          await employeePOSService.getWorkspaceContext()

        if (!isActive) {
          return
        }

        setWorkspaceContext(result)
        setContextError(null)
      } catch {
        if (!isActive) {
          return
        }

        setWorkspaceContext(null)
        setContextError("Unable to load the POS workspace.")
      } finally {
        if (isActive) {
          setIsLoadingContext(false)
        }
      }
    }

    void loadWorkspaceContext()

    return () => {
      isActive = false
    }
  }, [])

  const isWorkspaceUnavailable = useMemo(
    () =>
      isLoadingContext ||
      Boolean(contextError) ||
      workspaceContext === null,
    [contextError, isLoadingContext, workspaceContext]
  )

  return {
    workspaceContext,
    isLoadingContext,
    isWorkspaceUnavailable,
    contextError,
  }
}