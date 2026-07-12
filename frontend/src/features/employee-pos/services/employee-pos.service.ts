import { api } from "@/services/api"

import type {
  POSActivityInput,
  POSActivityResult,
  POSLocation,
  ScanResolveResponse,
} from "../types/employee-pos"

export const employeePOSService = {
  async getLocations(): Promise<POSLocation[]> {
    const response = await api.get<POSLocation[]>("/locations")

    return response.data
  },

  async resolveScan(identifier: string): Promise<ScanResolveResponse> {
    const response = await api.post<ScanResolveResponse>("/scan/resolve", {
      identifier,
    })

    return response.data
  },

  async createActivity(
    data: POSActivityInput
  ): Promise<POSActivityResult> {
    const response = await api.post<POSActivityResult>(
      "/loyalty-activities",
      data
    )

    return response.data
  },
}