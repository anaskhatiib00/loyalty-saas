import {
  Activity,
  BadgePercent,
  Building2,
  Gift,
  Home,
  MapPin,
  Settings,
  Users,
  WalletCards,
} from "lucide-react"

export const navigationSections = [
  {
    title: "Overview",
    items: [{ title: "Dashboard", href: "/", icon: Home }],
  },
  {
    title: "Business",
    items: [
      { title: "Customers", href: "/customers", icon: Users },
      { title: "Employees", href: "/employees", icon: BadgePercent },
      { title: "Locations", href: "/locations", icon: MapPin },
    ],
  },
  {
    title: "Loyalty",
    items: [
      { title: "Programs", href: "/programs", icon: Building2 },
      { title: "Rewards", href: "/rewards", icon: Gift },
      { title: "Activities", href: "/activities", icon: Activity },
      { title: "Wallets", href: "/wallets", icon: WalletCards },
    ],
  },
  {
    title: "System",
    items: [{ title: "Settings", href: "/settings", icon: Settings }],
  },
]