import { api } from "@/services/api"
import { CurrentUser } from "@/types/auth"

export const authService = {
  async getCurrentUser(): Promise<CurrentUser> {
    const response = await api.get("/auth/me")
    return response.data
  },
}