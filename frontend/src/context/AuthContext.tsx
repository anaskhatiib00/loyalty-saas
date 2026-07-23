"use client"

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react"

import { authService } from "@/services/auth.service"
import type { CurrentUser } from "@/types/auth"

type AuthContextType = {
  token: string | null
  user: CurrentUser | null
  isAuthenticated: boolean
  isInitializing: boolean
  login: (token: string) => Promise<CurrentUser>
  logout: () => void
  loadCurrentUser: () => Promise<CurrentUser>
}

type AuthProviderProps = {
  children: ReactNode
}

const AuthContext = createContext<AuthContextType | undefined>(
  undefined
)

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [token, setToken] = useState<string | null>(null)
  const [user, setUser] = useState<CurrentUser | null>(null)
  const [isInitializing, setIsInitializing] = useState(true)

  const loadCurrentUser = useCallback(async () => {
    const currentUser = await authService.getCurrentUser()

    setUser(currentUser)

    return currentUser
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem("access_token")
    setToken(null)
    setUser(null)
    setIsInitializing(false)
  }, [])

  useEffect(() => {
    let isActive = true

    async function initializeAuthentication() {
      await Promise.resolve()

      const storedToken = localStorage.getItem("access_token")

      if (!storedToken) {
        if (isActive) {
          setIsInitializing(false)
        }

        return
      }

      try {
        const currentUser =
          await authService.getCurrentUser()

        if (!isActive) {
          return
        }

        setToken(storedToken)
        setUser(currentUser)
      } catch {
        localStorage.removeItem("access_token")

        if (!isActive) {
          return
        }

        setToken(null)
        setUser(null)
      } finally {
        if (isActive) {
          setIsInitializing(false)
        }
      }
    }

    void initializeAuthentication()

    return () => {
      isActive = false
    }
  }, [])

  const login = useCallback(
    async (newToken: string) => {
      localStorage.setItem("access_token", newToken)
      setIsInitializing(true)

      try {
        const currentUser =
          await authService.getCurrentUser()

        setToken(newToken)
        setUser(currentUser)
        setIsInitializing(false)

        return currentUser
      } catch (error) {
        localStorage.removeItem("access_token")
        setToken(null)
        setUser(null)
        setIsInitializing(false)

        throw error
      }
    },
    []
  )

  const value = useMemo<AuthContextType>(
    () => ({
      token,
      user,
      isAuthenticated: Boolean(token && user),
      isInitializing,
      login,
      logout,
      loadCurrentUser,
    }),
    [
      token,
      user,
      isInitializing,
      login,
      logout,
      loadCurrentUser,
    ]
  )

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuthContext() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error(
      "useAuthContext must be used inside AuthProvider"
    )
  }

  return context
}