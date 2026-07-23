import { AccountTypeRoute } from "@/components/auth/AccountTypeRoute"
import { ProtectedRoute } from "@/components/auth/ProtectedRoute"
import { EmployeePOS } from "@/features/employee-pos"

export default function POSPage() {
  return (
    <ProtectedRoute>
      <AccountTypeRoute allowedAccountTypes={["employee"]}>
        <EmployeePOS />
      </AccountTypeRoute>
    </ProtectedRoute>
  )
}