export type BusinessSummary = {
  id: number
  name: string
}

export type CurrentUser = {
  id: number
  full_name: string
  email: string
  role: string
  business: BusinessSummary | null
}