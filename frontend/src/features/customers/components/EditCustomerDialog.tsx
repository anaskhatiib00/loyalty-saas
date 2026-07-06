"use client"

import { useState } from "react"
import { toast } from "sonner"
import { AxiosError } from "axios"

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
  type Customer,
} from "@/features/customers"

type EditCustomerDialogProps = {
  customer: Customer
  trigger: React.ReactNode
  onCustomerUpdated?: () => void
}

function getErrorMessage(error: unknown) {
  if (error instanceof AxiosError) {
    const detail = error.response?.data?.detail

    if (typeof detail === "string") {
      return detail
    }

    if (Array.isArray(detail)) {
      return detail[0]?.msg || "Invalid customer information."
    }
  }

  return "Could not update customer."
}

export function EditCustomerDialog({
  customer,
  trigger,
  onCustomerUpdated,
}: EditCustomerDialogProps) {
  const [open, setOpen] = useState(false)
  const [submitting, setSubmitting] = useState(false)

  async function handleUpdateCustomer(data: CreateCustomerInput) {
    try {
      setSubmitting(true)

      const updatedCustomer = await customerService.updateCustomer(
        customer.id,
        data
      )

      toast.success(
        `${updatedCustomer.first_name} ${
          updatedCustomer.last_name ?? ""
        } updated successfully.`
      )

      setOpen(false)
      onCustomerUpdated?.()
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
          <DialogTitle className="text-2xl">Edit Customer</DialogTitle>
        </DialogHeader>

        <CustomerForm
          customer={customer}
          submitLabel="Save changes"
          submittingLabel="Saving..."
          onSubmit={handleUpdateCustomer}
          onCancel={() => setOpen(false)}
          submitting={submitting}
        />
      </DialogContent>
    </Dialog>
  )
}