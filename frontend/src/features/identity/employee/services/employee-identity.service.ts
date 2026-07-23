import { api } from "@/services/api"

import type {
  AcceptEmployeeInvitationRequest,
  AcceptEmployeeInvitationResponse,
  EmployeeInvitationPreview,
} from "../types/employee-identity"

export const employeeIdentityService = {
  async getInvitationPreview(
    token: string
  ): Promise<EmployeeInvitationPreview> {
    const response = await api.get<EmployeeInvitationPreview>(
      "/employees/invitations/preview",
      {
        params: {
          token,
        },
      }
    )

    return response.data
  },

  async acceptInvitation(
    data: AcceptEmployeeInvitationRequest
  ): Promise<AcceptEmployeeInvitationResponse> {
    const response =
      await api.post<AcceptEmployeeInvitationResponse>(
        "/employees/invitations/accept",
        data
      )

    return response.data
  },
}