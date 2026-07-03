"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { LucideIcon } from "lucide-react"

type NavItem = {
  title: string
  href: string
  icon: LucideIcon
}

type NavSectionProps = {
  title: string
  items: NavItem[]
}

export function NavSection({ title, items }: NavSectionProps) {
  const pathname = usePathname()

  return (
    <div className="space-y-2">
      <p className="px-3 text-xs font-medium uppercase tracking-[0.2em] text-white/30">
        {title}
      </p>

      <div className="space-y-1">
        {items.map((item) => {
          const Icon = item.icon
          const active = pathname === item.href

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-3 rounded-2xl px-3 py-2.5 text-sm transition ${
                active
                  ? "bg-white text-black shadow-sm"
                  : "text-white/60 hover:bg-white/10 hover:text-white"
              }`}
            >
              <Icon className="h-4 w-4" />
              {item.title}
            </Link>
          )
        })}
      </div>
    </div>
  )
}