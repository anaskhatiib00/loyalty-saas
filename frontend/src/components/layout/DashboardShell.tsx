import { ReactNode } from "react"

import { Sidebar } from "./Sidebar"
import { Topbar } from "./Topbar"

export function DashboardShell({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-black">
      <div className="flex">
        <Sidebar />

        <main className="min-h-screen flex-1">
          <Topbar />
          <div className="p-6 lg:p-8">{children}</div>
        </main>
      </div>
    </div>
  )
}