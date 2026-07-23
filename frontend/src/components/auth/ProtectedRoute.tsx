"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

import { useAuth } from "@/hooks/useAuth"

export function ProtectedRoute({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const {
    isAuthenticated,
    isInitializing,
  } = useAuth()

  useEffect(() => {
    if (!isInitializing && !isAuthenticated) {
      router.replace("/login")
    }
  }, [isAuthenticated, isInitializing, router])

  if (isInitializing) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-black text-sm text-white/50">
        Checking authentication...
      </main>
    )
  }

  if (!isAuthenticated) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-black text-sm text-white/50">
        Redirecting to login...
      </main>
    )
  }

  return <>{children}</>
}