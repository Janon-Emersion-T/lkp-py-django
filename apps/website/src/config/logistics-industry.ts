export interface LogisticsChallenge {
  number: string;
  title: string;
  description: string;
}

export interface LogisticsCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface LogisticsPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface LogisticsFlow {
  number: string;
  title: string;
  description: string;
}

export const logisticsChallenges: LogisticsChallenge[] = [
  {
    number: "01",
    title: "Every handover can create an information gap",
    description:
      "Orders move between customers, operations teams, warehouses, drivers, carriers and recipients. Without structured status information, each handover becomes another place for uncertainty.",
  },
  {
    number: "02",
    title: "Dispatch decisions depend on current information",
    description:
      "Assignments, priorities, delivery windows and exceptions become harder to manage when operational data is delayed or spread across calls, messages and spreadsheets.",
  },
  {
    number: "03",
    title: "Warehouse and delivery records need to agree",
    description:
      "Inventory, picking, dispatch and delivery information should remain connected so teams can understand what left, what arrived and what still requires action.",
  },
  {
    number: "04",
    title: "Customers expect visibility without repeated calls",
    description:
      "Clear status information and appropriate notifications can reduce manual enquiries while giving customers better visibility into their orders or deliveries.",
  },
];

export const logisticsCapabilities: LogisticsCapability[] = [
  {
    number: "01",
    title: "Logistics Management Software",
    href: "/services/software-development/custom-software/",
    description:
      "Develop tailored systems for orders, shipments, dispatch, assignments, delivery status, exceptions and operational administration.",
    outcomes: [
      "Shipment visibility",
      "Dispatch control",
      "Status tracking",
      "Operational records",
    ],
  },
  {
    number: "02",
    title: "Warehouse & Inventory Systems",
    href: "/services/software-development/inventory-systems/",
    description:
      "Structure stock receipts, storage, movements, picking and dispatch information around the logistics workflows that depend on it.",
    outcomes: [
      "Stock visibility",
      "Movement history",
      "Dispatch accuracy",
      "Warehouse control",
    ],
  },
  {
    number: "03",
    title: "Mobile Delivery Workflows",
    href: "/services/mobile-app-development/",
    description:
      "Provide mobile-friendly workflows for assignments, delivery updates, proof records, photographs and other approved field activities.",
    outcomes: [
      "Driver workflows",
      "Delivery updates",
      "Proof records",
      "Mobile access",
    ],
  },
  {
    number: "04",
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Automate predictable status changes, notifications, assignments, alerts and recurring administrative actions.",
    outcomes: [
      "Status automation",
      "Customer notifications",
      "Operational alerts",
      "Less manual follow-up",
    ],
  },
  {
    number: "05",
    title: "API & Platform Integration",
    href: "/services/api-integration/",
    description:
      "Connect supported ecommerce, ERP, CRM, accounting, carrier, mapping or other operational platforms where suitable APIs are available.",
    outcomes: [
      "Connected platforms",
      "Data exchange",
      "Reduced re-entry",
      "Workflow continuity",
    ],
  },
  {
    number: "06",
    title: "Customer Portals",
    href: "/services/web-development/custom-web-applications/",
    description:
      "Create secure web experiences for appropriate shipment, order, document or service information without exposing internal operational systems.",
    outcomes: [
      "Self-service visibility",
      "Order information",
      "Document access",
      "Reduced enquiries",
    ],
  },
  {
    number: "07",
    title: "Logistics Analytics",
    href: "/services/data-analytics/",
    description:
      "Build dashboards around delivery performance, order volumes, exceptions, warehouse activity and other available operational data.",
    outcomes: [
      "Delivery reporting",
      "Exception visibility",
      "Operational KPIs",
      "Management insight",
    ],
  },
  {
    number: "08",
    title: "Cloud & Infrastructure",
    href: "/services/cloud-hosting/",
    description:
      "Support logistics applications with appropriate hosting, monitoring, backups and infrastructure planning.",
    outcomes: [
      "System availability",
      "Monitoring",
      "Backups",
      "Operational resilience",
    ],
  },
];

export const logisticsPrinciples: LogisticsPrinciple[] = [
  {
    number: "01",
    title: "Give every shipment a clear operational state",
    description:
      "Teams should be able to understand where an order or shipment sits in the workflow without reconstructing its history from calls and messages.",
  },
  {
    number: "02",
    title: "Record important handovers",
    description:
      "Transfers between warehouse, dispatch, driver, carrier and recipient should preserve enough information to support accountability and investigation.",
  },
  {
    number: "03",
    title: "Design field workflows for the field",
    description:
      "Mobile logistics workflows should minimise unnecessary typing and remain practical for staff working away from a desk.",
  },
  {
    number: "04",
    title: "Treat exceptions as first-class information",
    description:
      "Delayed, failed, damaged, incomplete or otherwise exceptional deliveries should be visible rather than disappearing inside normal workflow data.",
  },
];

export const logisticsFlow: LogisticsFlow[] = [
  {
    number: "01",
    title: "Receive",
    description:
      "The order or shipment request enters the operation with the information required for processing.",
  },
  {
    number: "02",
    title: "Prepare",
    description:
      "Goods, documents, inventory and fulfilment requirements are prepared for the next operational stage.",
  },
  {
    number: "03",
    title: "Dispatch",
    description:
      "Assignments, schedules and shipment information move into the delivery or transport workflow.",
  },
  {
    number: "04",
    title: "Track",
    description:
      "Operational status changes provide visibility while the shipment moves through its journey.",
  },
  {
    number: "05",
    title: "Deliver",
    description:
      "Delivery status and appropriate proof information close the physical movement of the shipment.",
  },
  {
    number: "06",
    title: "Review",
    description:
      "Exceptions, performance and completed operational records become available for service and management review.",
  },
];
