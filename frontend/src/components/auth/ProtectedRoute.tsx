"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"

import { useAuth } from "@/hooks/useAuth"

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const router = useRouter()
  const { isAuthenticated } = useAuth()
  const [checking, setChecking] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem("access_token")

    if (!token) {
      router.replace("/login")
      return
    }

    setChecking(false)
  }, [router, isAuthenticated])

  if (checking) {
    return (
      <main className="flex min-h-screen items-center justify-center bg-black text-sm text-white/50">
        Checking authentication...
      </main>
    )
  }

  return <>{children}</>
}