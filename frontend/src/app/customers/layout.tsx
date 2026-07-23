import type { ReactNode } from "react"

import { AccountTypeRoute } from "@/components/auth/AccountTypeRoute"
import { ProtectedRoute } from "@/components/auth/ProtectedRoute"

type CustomersLayoutProps = {
  children: ReactNode
}

export default function CustomersLayout({
  children,
}: CustomersLayoutProps) {
  return (
    <ProtectedRoute>
      <AccountTypeRoute allowedAccountTypes={["business_owner"]}>
        {children}
      </AccountTypeRoute>
    </ProtectedRoute>
  )
}