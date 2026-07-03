"use client"

import { CreditCard, UserCircle } from "lucide-react"

import { navigationSections } from "@/config/navigation"
import { NavSection } from "./NavSection"

export function Sidebar() {
  return (
    <aside className="hidden h-screen w-72 border-r border-white/10 bg-black px-4 py-5 text-white lg:flex lg:flex-col">
      <div className="mb-8 flex items-center gap-3 px-2">
        <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-white text-black">
          <CreditCard className="h-5 w-5" />
        </div>

        <div>
          <p className="text-sm text-white/50">Loyalty SaaS</p>
          <h1 className="font-semibold tracking-tight">Business Console</h1>
        </div>
      </div>

      <nav className="flex-1 space-y-6">
        {navigationSections.map((section) => (
          <NavSection
            key={section.title}
            title={section.title}
            items={section.items}
          />
        ))}
      </nav>

      <div className="mt-6 rounded-3xl border border-white/10 bg-white/[0.03] p-4">
        <div className="flex items-center gap-3">
          <UserCircle className="h-9 w-9 text-white/60" />
          <div>
            <p className="text-sm font-medium">Abdullah</p>
            <p className="text-xs text-white/40">Owner</p>
          </div>
        </div>
      </div>
    </aside>
  )
}