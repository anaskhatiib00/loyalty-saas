"use client"

import { useCallback, useEffect, useMemo, useState } from "react"
import { useParams, useRouter } from "next/navigation"
import {
  Activity,
  BadgeCheck,
  Gift,
  History,
  TrendingUp,
} from "lucide-react"

import { DashboardShell } from "@/components/layout/DashboardShell"

import {
  CustomerActivityTimeline,
  CustomerDigitalCard,
  CustomerOperations,
  CustomerProfileHeader,
  CustomerProgressPanel,
  CustomerWalletPanel,
  customerService,
  type CustomerProfile,
} from "@/features/customers"

export default function CustomerDetailsPage() {
  const params = useParams()
  const router = useRouter()

  const customerId = Number(params.customerId)

  const [profile, setProfile] = useState<CustomerProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchCustomerProfile = useCallback(async () => {
    try {
      setLoading(true)
      setError(null)

      const profile = await customerService.getCustomerProfile(customerId)
      setProfile(profile)
    } catch {
      setError("Could not load customer profile.")
    } finally {
      setLoading(false)
    }
  }, [customerId])

  const refreshCustomerProfile = useCallback(async () => {
    try {
      setError(null)

      const profile = await customerService.getCustomerProfile(customerId)
      setProfile(profile)
    } catch {
      setError("Could not refresh customer profile.")
    }
  }, [customerId])

  useEffect(() => {
    if (customerId) {
      fetchCustomerProfile()
    }
  }, [customerId, fetchCustomerProfile])

  const availableRewards = useMemo(() => {
    if (!profile) return []

    return profile.rewards
      .filter((reward) => reward.is_active)
      .map((reward) => ({
        ...reward,
        isAvailable:
          (profile.customer.current_progress ?? 0) >= reward.required_value,
        remaining:
          reward.required_value - (profile.customer.current_progress ?? 0),
      }))
      .sort((a, b) => a.required_value - b.required_value)
  }, [profile])

  return (
    <DashboardShell>
      <div className="space-y-6">
        {loading && (
          <div className="rounded-3xl border border-white/10 p-10 text-center text-sm text-white/50">
            Loading customer profile...
          </div>
        )}

        {!loading && error && (
          <div className="rounded-3xl border border-red-500/20 bg-red-500/10 p-5 text-sm text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && profile && (
          <>
            <CustomerProfileHeader
              customer={profile.customer}
              onCustomerUpdated={refreshCustomerProfile}
              onCustomerDeleted={() => router.push("/customers")}
            />

            <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
              <StatCard
                icon={TrendingUp}
                label="Current Progress"
                value={profile.customer.current_progress ?? 0}
              />

              <StatCard
                icon={Gift}
                label="Available Rewards"
                value={
                  availableRewards.filter((reward) => reward.isAvailable)
                    .length
                }
              />

              <StatCard
                icon={Activity}
                label="Total Activities"
                value={profile.activities.length}
              />

              <StatCard
                icon={BadgeCheck}
                label="Rewards Redeemed"
                value={profile.customer.total_rewards_redeemed ?? 0}
              />
            </div>

            <CustomerOperations
              customer={profile.customer}
              loyaltyCard={profile.loyaltyCard}
              loyaltyProgram={profile.loyaltyProgram}
              activities={profile.activities}
              onActionCompleted={refreshCustomerProfile}
            />

            <div className="grid gap-6 xl:grid-cols-2">
              <CustomerWalletPanel loyaltyCard={profile.loyaltyCard} />

              <CustomerProgressPanel
                currentProgress={profile.customer.current_progress ?? 0}
                targetCount={profile.loyaltyProgram?.target_count ?? null}
                programName={profile.loyaltyProgram?.name ?? null}
                rewardDescription={
                  profile.loyaltyProgram?.target_reward_description ?? null
                }
              />
            </div>

            <div className="grid gap-6 xl:grid-cols-2">
              <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
                <div className="flex items-center gap-3">
                  <Gift className="h-5 w-5 text-white/60" />

                  <div>
                    <h2 className="text-lg font-semibold">
                      Available Rewards
                    </h2>

                    <p className="text-sm text-white/50">
                      Rewards this customer can unlock or redeem.
                    </p>
                  </div>
                </div>

                <div className="mt-6 space-y-3">
                  {availableRewards.length === 0 && (
                    <div className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-white/40">
                      No rewards configured yet.
                    </div>
                  )}

                  {availableRewards.map((reward) => (
                    <div
                      key={reward.id}
                      className="rounded-2xl border border-white/10 bg-black/30 p-4"
                    >
                      <div className="flex items-start justify-between gap-4">
                        <div>
                          <p className="font-medium">{reward.name}</p>

                          <p className="mt-1 text-sm text-white/40">
                            {reward.description || "No description"}
                          </p>
                        </div>

                        <span
                          className={
                            reward.isAvailable
                              ? "rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-300"
                              : "rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs text-white/50"
                          }
                        >
                          {reward.isAvailable
                            ? "Available"
                            : `${Math.max(reward.remaining, 0)} more`}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

              <CustomerDigitalCard
                customer={profile.customer}
                loyaltyCard={profile.loyaltyCard}
                businessName="Anas Bakery"
                programName={profile.loyaltyProgram?.name ?? "Loyalty Program"}
                targetCount={profile.loyaltyProgram?.target_count ?? null}
              />
            </div>

            <div className="grid gap-6 xl:grid-cols-2">
              <CustomerActivityTimeline activities={profile.activities} />

              <section className="rounded-3xl border border-white/10 bg-white/[0.03] p-6 text-white">
                <div className="flex items-center gap-3">
                  <History className="h-5 w-5 text-white/60" />

                  <div>
                    <h2 className="text-lg font-semibold">
                      Progress Ledger
                    </h2>

                    <p className="text-sm text-white/50">
                      Balance changes and manual adjustments.
                    </p>
                  </div>
                </div>

                <div className="mt-6 space-y-3">
                  {profile.progressLedger.length === 0 && (
                    <div className="rounded-2xl border border-dashed border-white/10 p-6 text-center text-sm text-white/40">
                      No ledger entries yet.
                    </div>
                  )}

                  {profile.progressLedger.slice(0, 8).map((entry) => (
                    <div
                      key={entry.id}
                      className="flex items-center justify-between rounded-2xl border border-white/10 bg-black/30 p-4"
                    >
                      <div>
                        <p className="font-medium capitalize">
                          {entry.entry_type.replaceAll("_", " ")}
                        </p>

                        <p className="text-sm text-white/40">
                          {entry.note || "No note"}
                        </p>
                      </div>

                      <div className="text-right">
                        <p className="font-medium">
                          {entry.change_amount > 0 ? "+" : ""}
                          {entry.change_amount}
                        </p>

                        <p className="text-sm text-white/40">
                          Balance {entry.balance_after}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            </div>
          </>
        )}
      </div>
    </DashboardShell>
  )
}

type StatCardProps = {
  icon: React.ElementType
  label: string
  value: string | number
}

function StatCard({ icon: Icon, label, value }: StatCardProps) {
  return (
    <div className="rounded-3xl border border-white/10 bg-white/[0.03] p-5 text-white">
      <Icon className="h-5 w-5 text-white/50" />

      <p className="mt-4 text-2xl font-semibold">{value}</p>

      <p className="mt-1 text-sm text-white/40">{label}</p>
    </div>
  )
}