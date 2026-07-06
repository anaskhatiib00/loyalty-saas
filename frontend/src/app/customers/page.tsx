"use client"

import { Plus } from "lucide-react"

import { DashboardShell } from "@/components/layout/DashboardShell"
import {
  CreateCustomerDialog,
  CustomerBulkActions,
  CustomerEmptyState,
  CustomerLoadingSkeleton,
  CustomerMobileCards,
  CustomerPagination,
  CustomerSearch,
  CustomerSort,
  CustomerStats,
  CustomerTable,
  useCustomers,
} from "@/features/customers"

export default function CustomersPage() {
  const {
    search,
    setSearch,
    sort,
    setSort,
    currentPage,
    setCurrentPage,
    loading,
    error,
    totalPages,
    totalCustomers,
    paginatedCustomers,
    selectedCustomerIds,
    allPageSelected,
    toggleCustomerSelection,
    togglePageSelection,
    clearSelection,
    refreshCustomers,
  } = useCustomers()

  return (
    <DashboardShell>
      <div className="space-y-6 text-white">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-sm text-white/50">Business</p>

            <h1 className="mt-1 text-4xl font-semibold tracking-tight">
              Customers
            </h1>

            <p className="mt-2 text-sm text-white/50">
              Search, manage and issue wallet passes for your loyalty customers.
            </p>
          </div>

          <CreateCustomerDialog
            onCustomerCreated={refreshCustomers}
            trigger={
              <button className="inline-flex items-center justify-center gap-2 rounded-full bg-white px-5 py-2.5 text-sm font-medium text-black transition hover:bg-white/90">
                <Plus className="h-4 w-4" />
                New Customer
              </button>
            }
          />
        </div>

        <CustomerStats total={totalCustomers} />

        <div className="grid gap-3 md:grid-cols-[1fr_auto]">
          <CustomerSearch value={search} onChange={setSearch} />
          <CustomerSort value={sort} onChange={setSort} />
        </div>

        <CustomerBulkActions
          selectedCount={selectedCustomerIds.length}
          onClearSelection={clearSelection}
        />

        {loading && <CustomerLoadingSkeleton />}

        {!loading && error && (
          <div className="rounded-3xl border border-red-500/20 bg-red-500/10 p-5 text-sm text-red-300">
            {error}
          </div>
        )}

        {!loading &&
          !error &&
          (totalCustomers > 0 ? (
            <>
              <div className="hidden md:block">
                <CustomerTable
                  customers={paginatedCustomers}
                  selectedCustomerIds={selectedCustomerIds}
                  allPageSelected={allPageSelected}
                  onToggleCustomer={toggleCustomerSelection}
                  onTogglePageSelection={togglePageSelection}
                  onCustomerDeleted={refreshCustomers}
                />
              </div>

              <CustomerMobileCards
                customers={paginatedCustomers}
                selectedCustomerIds={selectedCustomerIds}
                onToggleCustomer={toggleCustomerSelection}
                onCustomerDeleted={refreshCustomers}
              />

              <CustomerPagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
              />
            </>
          ) : (
            <CustomerEmptyState />
          ))}
      </div>
    </DashboardShell>
  )
}