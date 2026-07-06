"use client"

import { useState } from "react"
import { AxiosError } from "axios"
import { toast } from "sonner"

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"

import {
  CustomerForm,
  customerService,
  type CreateCustomerInput,
} from "@/features/customers"

type CreateCustomerDialogProps = {
  trigger: React.ReactNode
  onCustomerCreated?: () => void
}

type BackendValidationError = {
  detail?: string | { msg?: string }[]
}

function getErrorMessage(error: unknown) {
  if (error instanceof AxiosError) {
    const data = error.response?.data as BackendValidationError | undefined

    if (typeof data?.detail === "string") {
      return data.detail
    }

    if (Array.isArray(data?.detail)) {
      return data.detail[0]?.msg || "Invalid customer information."
    }

    if (error.response?.status === 409) {
      return "A customer with this email or phone already exists."
    }

    if (error.response?.status === 404) {
      return "Selected location was not found."
    }

    if (error.response?.status === 422) {
      return "Please check the required fields."
    }
  }

  return "Could not create customer."
}

export function CreateCustomerDialog({
  trigger,
  onCustomerCreated,
}: CreateCustomerDialogProps) {
  const [open, setOpen] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  async function handleCreateCustomer(data: CreateCustomerInput) {
    try {
      setSubmitting(true)

      const customer = await customerService.createCustomer(data)

      toast.success(
        `${customer.first_name} ${customer.last_name ?? ""} created successfully.`
      )

      setOpen(false)
      onCustomerCreated?.()
    } catch (error) {
      toast.error(getErrorMessage(error))
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>{trigger}</DialogTrigger>

      <DialogContent className="max-w-2xl border-white/10 bg-neutral-950 text-white">
        <DialogHeader>
          <DialogTitle className="text-2xl">New Customer</DialogTitle>
        </DialogHeader>

        <CustomerForm
          onSubmit={handleCreateCustomer}
          onCancel={() => setOpen(false)}
          submitting={submitting}
        />
      </DialogContent>
    </Dialog>
  )
}