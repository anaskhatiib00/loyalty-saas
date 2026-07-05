import { api } from "@/services/api"
import type { Customer } from "../types/customer"

export const customerService = {
  async getCustomers(): Promise<Customer[]> {
    const response = await api.get("/customers")
    return response.data
  },

  async getCustomer(customerId: number): Promise<Customer> {
    const response = await api.get(`/customers/${customerId}`)
    return response.data
  },
}