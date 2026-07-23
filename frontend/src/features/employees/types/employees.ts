export type EmployeeRole = "owner" | "manager" | "cashier"

export type EmployeeStatus =
  | "invited"
  | "active"
  | "inactive"

export type Employee = {
  id: number
  business_id: number
  location_id: number | null
  full_name: string
  email: string | null
  phone: string | null
  role: EmployeeRole
  status: EmployeeStatus
}

export type CreateEmployeeInvitationInput = {
  location_id?: number | null
  full_name: string
  email: string
  phone?: string | null
  role: Exclude<EmployeeRole, "owner">
}

export type IdentityInvitationStatus =
  | "pending"
  | "accepted"
  | "expired"
  | "revoked"

export type IdentityInvitation = {
  id: number
  business_id: number
  employee_id: number | null
  email: string
  role: EmployeeRole
  status: IdentityInvitationStatus
  expires_at: string
  created_at: string
}

export type CreateEmployeeInvitationResponse = {
  invitation: IdentityInvitation
  employee_id: number
  delivery_status: string
  development_invitation_token: string | null
  development_accept_url: string | null
}

export type AcceptEmployeeInvitationInput = {
  token: string
  password: string
}

export type InvitationAcceptedUser = {
  id: number
  full_name: string
  email: string
  role: string
}

export type AcceptEmployeeInvitationResponse = {
  message: string
  employee_id: number
  user: InvitationAcceptedUser
}

