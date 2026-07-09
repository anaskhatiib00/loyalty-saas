import {
  BadgePlus,
  CircleDollarSign,
  MinusCircle,
  Plus,
  ScanLine,
} from "lucide-react"

export type CustomerOperationType =
  | "visit"
  | "stamp"
  | "points"
  | "spend"
  | "correction"

export const CUSTOMER_OPERATIONS: Array<{
  type: CustomerOperationType
  title: string
  description: string
  programType: string | null
  icon: typeof Plus
}> = [
  {
    type: "visit",
    title: "Add Visit",
    description: "Record one customer visit.",
    programType: "visits",
    icon: ScanLine,
  },
  {
    type: "stamp",
    title: "Add Stamp",
    description: "Add one stamp to the card.",
    programType: "stamps",
    icon: BadgePlus,
  },
  {
    type: "points",
    title: "Add Points",
    description: "Manually add loyalty points.",
    programType: "points",
    icon: Plus,
  },
  {
    type: "spend",
    title: "Record Spend",
    description: "Record spend-based progress.",
    programType: "spend",
    icon: CircleDollarSign,
  },
  {
    type: "correction",
    title: "Correction",
    description: "Fix mistakes with a required reason.",
    programType: null,
    icon: MinusCircle,
  },
]

export function getRecommendedCustomerOperation(programType?: string | null) {
  return (
    CUSTOMER_OPERATIONS.find((operation) => operation.programType === programType) ??
    null
  )
}