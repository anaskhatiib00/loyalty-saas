export type AccountType = "business_owner" | "employee"

export type BusinessSummary = {
  id: number
  name: string
}

export type CurrentEmployeeSummary = {
  id: number
  business_id: number
  location_id: number | null
  role: string
  status: string
}

export type CurrentUser = {
  id: number
  full_name: string
  email: string
  role: string
  account_type: AccountType
  business: BusinessSummary | null
  employee: CurrentEmployeeSummary | null
}