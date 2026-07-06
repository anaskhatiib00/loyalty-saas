export type Customer = {
  id: number
  first_name: string
  last_name: string | null
  email: string | null
  phone: string | null
  date_of_birth: string | null
  status?: string
  created_at?: string
}

export type CreateCustomerInput = {
  location_id: number
  first_name: string
  last_name?: string
  email?: string
  phone?: string
  date_of_birth?: string
}

