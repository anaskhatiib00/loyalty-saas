import { api } from "@/services/api"
import { Customer } from "@/types/customer"

export const customerService = {
  async getCustomers(): Promise<Customer[]> {
    const response = await api.get("/customers")
    return response.data
  },
}