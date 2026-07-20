import { api } from "@/services/api"

import type {
  POSRecentActivityResponse,
  POSScanRequest,
  POSScanResponse,
} from "../types/employee-pos"

export const employeePOSService = {
  async scanCard(data: POSScanRequest): Promise<POSScanResponse> {
    const response = await api.post<POSScanResponse>("/pos/scan", data)

    return response.data
  },

  async getRecentActivity(
    limit = 10
  ): Promise<POSRecentActivityResponse> {
    const response = await api.get<POSRecentActivityResponse>(
      "/pos/activity",
      {
        params: {
          limit,
        },
      }
    )

    return response.data
  },
}