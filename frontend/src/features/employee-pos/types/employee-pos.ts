export type POSCustomer = {
  id: number
  first_name: string
  last_name: string | null
  phone: string | null
  email: string | null
  current_progress: number
  is_active: boolean
}

export type POSLoyaltyCard = {
  id: number
  card_number: string
  public_id: string
  status: string
}

export type ScanResolveResponse = {
  loyalty_card: POSLoyaltyCard
  customer: POSCustomer
}

export type POSActivityType =
  | "purchase"
  | "visit"
  | "stamp_scan"
  | "product_purchase"

export type POSActivityInput = {
  loyalty_card_identifier: string
  location_id: number
  employee_id?: number
  activity_type: POSActivityType
  purchase_amount?: number
  qualifying_quantity?: number
  note?: string
}

export type POSUnlockedReward = {
  id: number
  name: string
  description: string | null
  required_value: number
  reward_type: string
  reward_value: string | null
}

export type POSActivityResult = {
  activity: Record<string, never>
  unlocked_rewards: POSUnlockedReward[]
  reward_collected?: boolean
}

export type POSLocation = {
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