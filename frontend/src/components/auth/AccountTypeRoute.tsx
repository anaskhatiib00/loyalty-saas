"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

import { useAuth } from "@/hooks/useAuth"
import type { AccountType } from "@/types/auth"

type AccountTypeRouteProps = {
  allowedAccountTypes: AccountType[]
  children: React.ReactNode
}

function getDefaultRoute(accountType: AccountType) {
  if (accountType === "employee") {
    return "/pos"
  }

  return "/customers"
}

export function AccountTypeRoute({
  allowedAccountTypes,
  children,
}: AccountTypeRouteProps) {
  const router = useRouter()
  const {
    user,
    isAuthenticated,
    isInitializing,
  } = useAuth()

  const isAllowed = user
    ? allowedAccountTypes.includes(user.account_type)
    : false


  useEffect(() => {
    if (
      isInitializing ||
      !isAuthenticated ||
      !user ||
      isAllowed
    ) {
      return
    }

    router.replace(getDefaultRoute(user.account_type))
  }, [
    isAllowed,
    isAuthenticated,
    isInitializing,
    router,
    user,
  ])

  if (isInitializing || !isAuthenticated || !user) {
    return null
  }

  if (!isAllowed) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-black text-sm text-white/50">
        Redirecting to your workspace...
      </main>
    )
  }

  return <>{children}</>
}