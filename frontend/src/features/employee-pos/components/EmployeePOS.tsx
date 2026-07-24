"use client"

import { useEmployeePOS } from "../hooks/useEmployeePOS"
import { ActivityPanel } from "./loyalty-desk/ActivityPanel"
import { LoyaltyDeskHeader } from "./loyalty-desk/LoyaltyDeskHeader"
import { LoyaltyScanner } from "./loyalty-desk/LoyaltyScanner"

export function EmployeePOS() {
  const {
    workspaceContext,
    recentActivity,
    scanResult,

    manualCardInput,
    setManualCardInput,

    isLoadingContext,
    isLoadingActivity,
    isScanning,
    isWorkspaceUnavailable,

    contextError,
    error,

    scanCard,
    loadRecentActivity,
    reset,
  } = useEmployeePOS()

  const business = workspaceContext?.business
  const employee = workspaceContext?.employee
  const location = workspaceContext?.location

  return (
    <main className="min-h-screen bg-[#07110f] text-white">
      <div className="mx-auto flex min-h-screen w-full max-w-7xl flex-col px-4 py-4 sm:px-6 sm:py-6 lg:px-8">
        <LoyaltyDeskHeader
          businessName={business?.name ?? "Loyalty checkout"}
          employeeName={employee?.full_name ?? "Employee"}
          locationName={location?.name ?? "Assigned location"}
          isLoading={isLoadingContext}
        />

        {contextError ? (
          <div className="mt-4 rounded-2xl border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-100">
            {contextError}
          </div>
        ) : null}

        <div className="mt-6 grid flex-1 items-start gap-6 lg:grid-cols-[1.25fr_0.75fr]">
          <LoyaltyScanner
            manualCardInput={manualCardInput}
            setManualCardInput={setManualCardInput}
            isScanning={isScanning}
            isWorkspaceUnavailable={isWorkspaceUnavailable}
            error={error}
            scanResult={scanResult}
            onScan={scanCard}
            onReset={reset}
          />

          <ActivityPanel
            recentActivity={recentActivity}
            isLoadingActivity={isLoadingActivity}
            onLoadActivity={loadRecentActivity}
          />
        </div>
      </div>
    </main>
  )
}