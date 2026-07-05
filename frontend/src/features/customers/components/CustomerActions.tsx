"use client"

import { MoreHorizontal, Eye, WalletCards, Star, Gift, Pencil, Trash2 } from "lucide-react"

import type { Customer } from "@/features/customers"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"

type CustomerActionsProps = {
  customer: Customer
}

export function CustomerActions({ customer }: CustomerActionsProps) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger className="rounded-full p-2 text-white/50 transition hover:bg-white/10 hover:text-white">
        <MoreHorizontal className="h-4 w-4" />
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end" className="w-56">
        <DropdownMenuItem>
          <Eye className="mr-2 h-4 w-4" />
          View Profile
        </DropdownMenuItem>

        <DropdownMenuItem>
          <WalletCards className="mr-2 h-4 w-4" />
          Issue Wallet
        </DropdownMenuItem>

        <DropdownMenuItem>
          <Star className="mr-2 h-4 w-4" />
          Add Progress
        </DropdownMenuItem>

        <DropdownMenuItem>
          <Gift className="mr-2 h-4 w-4" />
          Redeem Reward
        </DropdownMenuItem>

        <DropdownMenuSeparator />

        <DropdownMenuItem>
          <Pencil className="mr-2 h-4 w-4" />
          Edit Customer
        </DropdownMenuItem>

        <DropdownMenuItem className="text-red-500">
          <Trash2 className="mr-2 h-4 w-4" />
          Delete Customer
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  )
}