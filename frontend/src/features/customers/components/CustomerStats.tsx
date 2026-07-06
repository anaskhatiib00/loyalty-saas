import { Users, WalletCards, UserCheck, CalendarPlus } from "lucide-react"

type CustomerStatsProps = {
  total: number
}

export function CustomerStats({ total }: CustomerStatsProps) {
  const cards = [
    {
      title: "Customers",
      value: total,
      icon: Users,
    },
    {
      title: "Active",
      value: total,
      icon: UserCheck,
    },
    {
      title: "Wallets",
      value: "—",
      icon: WalletCards,
    },
    {
      title: "New This Month",
      value: "—",
      icon: CalendarPlus,
    },
  ]

  return (
    <div className="grid grid-cols-2 gap-3 md:gap-4 xl:grid-cols-4">
      {cards.map((card) => {
        const Icon = card.icon

        return (
          <div
            key={card.title}
            className="rounded-3xl border border-white/10 bg-white/[0.03] p-4 md:p-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-white/50">
                  {card.title}
                </p>

                <p className="mt-2 text-3xl font-semibold">
                  {card.value}
                </p>
              </div>

              <div className="rounded-2xl bg-white/5 p-3">
                <Icon className="h-5 w-5 text-white/70" />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}