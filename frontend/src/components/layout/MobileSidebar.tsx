"use client"

import { Menu } from "lucide-react"

import { Button } from "@/components/ui/button"
import {
  Sheet,
  SheetContent,
  SheetTrigger,
} from "@/components/ui/sheet"
import { navigationSections } from "@/config/navigation"
import { NavSection } from "./NavSection"

export function MobileSidebar() {
  return (
    <Sheet>
      <SheetTrigger asChild>
        <Button
          variant="outline"
          size="icon"
          className="border-white/10 bg-black text-white hover:bg-white/10 lg:hidden"
        >
          <Menu className="h-5 w-5" />
        </Button>
      </SheetTrigger>

      <SheetContent
        side="left"
        className="w-[86vw] max-w-80 border-white/10 bg-black p-5 text-white"
      >
        <div className="mb-8">
          <p className="text-sm text-white/50">Loyalty SaaS</p>
          <h1 className="font-semibold tracking-tight">Business Console</h1>
        </div>

        <nav className="space-y-6">
          {navigationSections.map((section) => (
            <NavSection
              key={section.title}
              title={section.title}
              items={section.items}
            />
          ))}
        </nav>
      </SheetContent>
    </Sheet>
  )
}