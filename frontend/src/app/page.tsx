"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"

import { ProtectedRoute } from "@/components/auth/ProtectedRoute"
import { useAuth } from "@/hooks/useAuth"

function HomeRedirect() {
  const router = useRouter()
  const { user } = useAuth()

  useEffect(() => {
    if (!user) {
      return
    }

    if (user.account_type === "employee") {
      router.replace("/pos")
      return
    }

    router.replace("/customers")
  }, [router, user])

  return (
    <main className="flex min-h-screen items-center justify-center bg-black text-sm text-white/50">
      Opening your workspace...
    </main>
  )
}

export default function HomePage() {
  return (
    <ProtectedRoute>
      <HomeRedirect />
    </ProtectedRoute>
  )
}