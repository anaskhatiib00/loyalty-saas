import { api } from "@/services/api"
import type {
  CreateCustomerInput,
  CreateLoyaltyActivityInput,
  Customer,
  CustomerProfile,
  LoyaltyActivity,
  LoyaltyActivityResult,
  LoyaltyCard,
  LoyaltyProgram,
  ManualProgressAdjustmentInput,
  ProgressLedgerEntry,
  Reward,
} from "../types/customer"

async function safeGet<T>(url: string): Promise<T | null> {
  try {
    const response = await api.get<T>(url)
    return response.data
  } catch {
    return null
  }
}

export const customerService = {
  async getCustomers(): Promise<Customer[]> {
    const response = await api.get("/customers")
    return response.data
  },

  async getCustomer(customerId: number): Promise<Customer> {
    const response = await api.get(`/customers/${customerId}`)
    return response.data
  },

  async getCustomerProfile(customerId: number): Promise<CustomerProfile> {
    const customer = await this.getCustomer(customerId)

    const [loyaltyCard, loyaltyProgram, rewards, activities, progressLedger] =
      await Promise.all([
        safeGet<LoyaltyCard>(`/loyalty-cards/customer/${customerId}`),
        safeGet<LoyaltyProgram>("/loyalty-program/me"),
        safeGet<Reward[]>("/rewards"),
        safeGet<LoyaltyActivity[]>(`/loyalty-activities/customer/${customerId}`),
        safeGet<ProgressLedgerEntry[]>(
          `/progress-ledger/customer/${customerId}`
        ),
      ])

    return {
      customer,
      loyaltyCard,
      loyaltyProgram,
      rewards: rewards ?? [],
      activities: activities ?? [],
      progressLedger: progressLedger ?? [],
    }
  },

  async createCustomer(data: CreateCustomerInput): Promise<Customer> {
    const response = await api.post("/customers", data)
    return response.data
  },

  async updateCustomer(
    customerId: number,
    data: Partial<CreateCustomerInput>
  ): Promise<Customer> {
    const response = await api.patch(`/customers/${customerId}`, data)
    return response.data
  },

  async deleteCustomer(customerId: number): Promise<void> {
    await api.delete(`/customers/${customerId}`)
  },

  async createLoyaltyActivity(
    data: CreateLoyaltyActivityInput
  ): Promise<LoyaltyActivityResult> {
    const response = await api.post<LoyaltyActivityResult>(
      "/loyalty-activities",
      data
    )

    return response.data
  },

  async createManualProgressAdjustment(
    data: ManualProgressAdjustmentInput
  ): Promise<ProgressLedgerEntry> {
    const response = await api.post<ProgressLedgerEntry>(
      "/progress-ledger",
      data
    )

    return response.data
  },
}