export type POSBusinessContext = {
  id: number
  name: string
}

export type POSEmployeeContext = {
  id: number
  full_name: string
  role: string
}

export type POSLocationContext = {
  id: number
  name: string
  address: string
  city: string | null
  state: string | null
  country: string | null
}

export type POSWorkspaceContext = {
  business: POSBusinessContext
  employee: POSEmployeeContext
  location: POSLocationContext
}

export type POSScanRequest = {
  loyalty_card_identifier: string
}

export type POSReward = {
  id: number
  name: string
  description: string | null
  reward_type: string
  reward_value: string | null
  required_value: number
}

export type POSScanResponse = {
  customer_id: number
  loyalty_card_id: number
  program_type: string
  current_progress: number
  reward_available: boolean
  reward_collected: boolean
  unlocked_rewards: POSReward[]
}

export type POSActivityItem = {
  id: number

  customer_id: number
  customer_name: string

  employee_id: number
  employee_name: string

  location_id: number
  location_name: string

  program_type: string
  event_type: string
  activity_type: string
  source: string

  progress_change: number
  balance_before: number
  balance_after: number

  reward_id: number | null
  reward_name: string | null

  created_at: string
}

export type POSRecentActivityResponse = {
  employee_id: number
  employee_name: string

  location_id: number
  location_name: string

  total_activities: number
  activities: POSActivityItem[]
}