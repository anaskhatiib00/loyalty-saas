"use client"

import { useState } from "react"
import { AxiosError } from "axios"
import { toast } from "sonner"

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog"

import {
  customerService,
  type Customer,
} from "@/features/customers"

type DeleteCustomerDialogProps = {
  customer: Customer
  trigger: React.ReactNode
  onCustomerDeleted?: () => void
}

function getErrorMessage(error: unknown) {
  if (error instanceof AxiosError) {
    const detail = error.response?.data?.detail

    if (typeof detail === "string") {
      return detail
    }
  }

  return "Could not delete customer."
}

export function DeleteCustomerDialog({
  customer,
  trigger,
  onCustomerDeleted,
}: DeleteCustomerDialogProps) {
  const [deleting, setDeleting] = useState(false)

  async function handleDelete() {
    try {
      setDeleting(true)

      await customerService.deleteCustomer(customer.id)

      toast.success(
        `${customer.first_name} ${customer.last_name ?? ""} deleted successfully.`
      )

      onCustomerDeleted?.()
    } catch (error) {
      toast.error(getErrorMessage(error))
    } finally {
      setDeleting(false)
    }
  }

  return (
    <AlertDialog>
      <AlertDialogTrigger asChild>
        {trigger}
      </AlertDialogTrigger>

      <AlertDialogContent className="border-white/10 bg-neutral-950 text-white">
        <AlertDialogHeader>
          <AlertDialogTitle>
            Delete customer?
          </AlertDialogTitle>

          <AlertDialogDescription className="text-white/60">
            This will permanently delete{" "}
            <strong>
              {customer.first_name} {customer.last_name}
            </strong>
            .
            <br />
            <br />
            This action cannot be undone.
          </AlertDialogDescription>
        </AlertDialogHeader>

        <AlertDialogFooter className="bg-neutral-950">
          <AlertDialogCancel className="rounded-full border border-white/10 bg-transparent px-5 py-2.5 text-white/70 hover:bg-white/10 hover:text-white">
            Cancel
          </AlertDialogCancel>

          <AlertDialogAction
            onClick={handleDelete}
            disabled={deleting}
            className="bg-red-600 hover:bg-red-700"
          >
            {deleting ? "Deleting..." : "Delete Customer"}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}