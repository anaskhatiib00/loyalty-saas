export type Location = {
  id: number
  business_id: number
  name: string
  phone: string | null
  address: string
  city: string | null
  state: string | null
  country: string | null
  postal_code: string | null
  is_default: boolean
}