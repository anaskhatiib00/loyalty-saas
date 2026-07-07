export type Customer = {
  id: number
  business_id?: number
  location_id?: number
  first_name: string
  last_name: string | null
  email: string | null
  phone: string | null
  date_of_birth: string | null
  current_progress?: number
  total_rewards_redeemed?: number
  is_active?: boolean
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

export type LoyaltyCard = {
  id: number
  customer_id: number
  card_number: string
  public_id: string
  status: string
}

export type LoyaltyProgram = {
  id: number
  business_id: number
  name: string
  description: string | null
  program_type: string
  earn_unit: string
  earn_rate: number
  target_count: number | null
  target_reward_description: string | null
  is_active: boolean
}

export type Reward = {
  id: number
  business_id: number
  name: string
  description: string | null
  required_value: number
  reward_type: string
  reward_value: string | null
  is_active: boolean
  redemption_behavior: string
  redemption_mode: string
}

export type LoyaltyActivity = {
  id: number
  business_id: number
  location_id: number
  employee_id: number | null
  customer_id: number
  loyalty_card_id: number
  activity_type: string
  status: string
  purchase_amount: number
  qualifying_quantity: number
  earned_progress: number
  balance_after: number
  note: string | null
}

export type ProgressLedgerEntry = {
  id: number
  business_id: number
  customer_id: number
  change_amount: number
  balance_after: number
  entry_type: string
  reference_type: string | null
  reference_id: string | null
  note: string | null
}

export type CustomerProfile = {
  customer: Customer
  loyaltyCard: LoyaltyCard | null
  loyaltyProgram: LoyaltyProgram | null
  rewards: Reward[]
  activities: LoyaltyActivity[]
  progressLedger: ProgressLedgerEntry[]
}