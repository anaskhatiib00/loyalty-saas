type CustomerPaginationProps = {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
}

export function CustomerPagination({
  currentPage,
  totalPages,
  onPageChange,
}: CustomerPaginationProps) {
  if (totalPages <= 1) {
    return null
  }

  return (
    <div className="flex flex-col gap-3 rounded-3xl border border-white/10 bg-white/[0.03] px-5 py-4 text-sm text-white/60 sm:flex-row sm:items-center sm:justify-between">
      <p>
        Page <span className="text-white">{currentPage}</span> of{" "}
        <span className="text-white">{totalPages}</span>
      </p>

      <div className="flex items-center gap-2">
        <button
          disabled={currentPage === 1}
          onClick={() => onPageChange(currentPage - 1)}
          className="rounded-full border border-white/10 px-4 py-2 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Previous
        </button>

        <button
          disabled={currentPage === totalPages}
          onClick={() => onPageChange(currentPage + 1)}
          className="rounded-full border border-white/10 px-4 py-2 transition hover:bg-white/10 disabled:cursor-not-allowed disabled:opacity-40"
        >
          Next
        </button>
      </div>
    </div>
  )
}