import { Activity, Gift, Users, WalletCards } from "lucide-react"

import { DashboardShell } from "@/components/layout/DashboardShell"
import { QuickActions } from "@/components/dashboard/QuickActions"
import { RecentActivity } from "@/components/dashboard/RecentActivity"
import { StatCard } from "@/components/dashboard/StatCard"
import {
  customerService,
  type Customer,
} from "@/features/customers"

export default function DashboardPage() {
  return (
    <DashboardShell>
      <div className="space-y-8 text-white">
        <section className="max-w-3xl">
          <p className="text-sm text-white/50">Good afternoon 👋</p>
          <h1 className="mt-2 text-4xl font-semibold tracking-tight">
            Dashboard
          </h1>
          <p className="mt-3 text-sm leading-6 text-white/50">
            A simple command center for customers, rewards, wallet passes, and
            loyalty activity.
          </p>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          <StatCard title="Customers" value="0" change="+0 this week" icon={Users} />
          <StatCard title="Rewards" value="0" change="+0 active" icon={Gift} />
          <StatCard title="Activities" value="0" change="+0 today" icon={Activity} />
          <StatCard title="Wallet Passes" value="0" change="+0 issued" icon={WalletCards} />
        </section>

        <QuickActions />

        <RecentActivity />
      </div>
    </DashboardShell>
  )
}