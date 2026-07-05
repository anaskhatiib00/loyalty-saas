"use client"

import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react"

import { authService } from "@/services/auth.service"
import { CurrentUser } from "@/types/auth"

type AuthContextType = {
  token: string | null
  user: CurrentUser | null
  isAuthenticated: boolean
  login: (token: string) => Promise<void>
  logout: () => void
  loadCurrentUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({
  children,
}: {
  children: React.ReactNode
}) {
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<CurrentUser | null>(null)

  async function loadCurrentUser() {
    const currentUser = await authService.getCurrentUser()
    setUser(currentUser)
  }

  useEffect(() => {
    const storedToken = localStorage.getItem("access_token")

    if (storedToken) {
      setToken(storedToken)
      loadCurrentUser().catch(() => {
        localStorage.removeItem("access_token")
        setToken(null)
        setUser(null)
      })
    }
  }, [])

  async function login(newToken: string) {
    localStorage.setItem("access_token", newToken)
    setToken(newToken)
    await loadCurrentUser()
  }

  function logout() {
    localStorage.removeItem("access_token")
    setToken(null)
    setUser(null)
  }

  const value = useMemo(
    () => ({
      token,
      user,
      isAuthenticated: !!token,
      login,
      logout,
      loadCurrentUser,
    }),
    [token, user]
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuthContext() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error("useAuthContext must be used inside AuthProvider")
  }

  return context
}