export type AcceptEmployeeInvitationRequest = {
  token: string
  password: string
}

export type AcceptedEmployeeUser = {
  id: number
  email: string
  full_name: string
  role: string
}

export type AcceptEmployeeInvitationResponse = {
  message: string
  employee_id: number
  user: AcceptedEmployeeUser
}

export type EmployeeInvitationPreview = {
  business_name: string
  employee_name: string
  role: string
  expires_at: string
}