import { api } from "@/services/api"
import type { CreateCustomerInput, Customer } from "../types/customer"

export const customerService = {
  async getCustomers(): Promise<Customer[]> {
    const response = await api.get("/customers")
    return response.data
  },

  async getCustomer(customerId: number): Promise<Customer> {
    const response = await api.get(`/customers/${customerId}`)
    return response.data
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
}