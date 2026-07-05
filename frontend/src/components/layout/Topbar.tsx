"use client"

import { Bell, Search } from "lucide-react"

import { useAuth } from "@/hooks/useAuth"
import { MobileSidebar } from "./MobileSidebar"
import { UserMenu } from "./UserMenu"

export function Topbar() {
  const { user } = useAuth()

  const businessName = user?.business?.name || "Business Console"

  return (
    <header className="flex h-16 items-center justify-between border-b border-white/10 bg-black px-4 text-white md:px-6">
      <div className="flex items-center gap-3">
        <MobileSidebar />

        <div>
          <p className="text-sm font-medium">{businessName}</p>
          <p className="text-xs text-white/40">All locations</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <button className="hidden items-center gap-2 rounded-full border border-white/10 px-4 py-2 text-sm text-white/50 transition hover:bg-white/10 hover:text-white md:flex">
          <Search className="h-4 w-4" />
          Search
          <span className="ml-4 text-xs text-white/30">Ctrl K</span>
        </button>

        <button className="rounded-full border border-white/10 p-2 text-white/60 transition hover:bg-white/10 hover:text-white">
          <Bell className="h-4 w-4" />
        </button>

        <UserMenu />
      </div>
    </header>
  )
}