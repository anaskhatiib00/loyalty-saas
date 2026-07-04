export type Customer = {
  id: number
  first_name: string
  last_name: string | null
  email: string | null
  phone: string | null
  status?: string
  created_at?: string
}