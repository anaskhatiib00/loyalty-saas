import { api } from "@/services/api"

import type { Location } from "../types/locations"

export const locationsService = {
  async listLocations(): Promise<Location[]> {
    const response = await api.get<Location[]>("/locations")

    return response.data
  },
}