import { api } from "@/services/api"

import type {
  AcceptEmployeeInvitationInput,
  AcceptEmployeeInvitationResponse,
  CreateEmployeeInvitationInput,
  CreateEmployeeInvitationResponse,
  Employee,
} from "../types/employees"

export const employeesService = {
  async listEmployees(): Promise<Employee[]> {
    const response = await api.get<Employee[]>("/employees")

    return response.data
  },

  async createInvitation(
    data: CreateEmployeeInvitationInput
  ): Promise<CreateEmployeeInvitationResponse> {
    const response = await api.post<CreateEmployeeInvitationResponse>(
      "/employees/invitations",
      data
    )

    return response.data
  },

  async acceptInvitation(
    data: AcceptEmployeeInvitationInput
  ): Promise<AcceptEmployeeInvitationResponse> {
    const response = await api.post<AcceptEmployeeInvitationResponse>(
      "/employees/invitations/accept",
      data
    )

    return response.data
  },
}