export interface ManufacturingChallenge {
  number: string;
  title: string;
  description: string;
}

export interface ManufacturingCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface ManufacturingPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface ManufacturingFlow {
  number: string;
  title: string;
  description: string;
}

export const manufacturingChallenges: ManufacturingChallenge[] = [
  {
    number: "01",
    title: "Production information is often fragmented",
    description:
      "Orders, materials, work-in-progress, schedules and production records can end up spread across spreadsheets, paper records and disconnected software.",
  },
  {
    number: "02",
    title: "Inventory errors affect the production plan",
    description:
      "Poor visibility of raw materials, components and finished goods can create shortages, over-ordering or avoidable delays.",
  },
  {
    number: "03",
    title: "Manual handovers reduce traceability",
    description:
      "When production stages depend on verbal updates or manual records, it becomes harder to understand who changed what, when and why.",
  },
  {
    number: "04",
    title: "Management needs operational visibility",
    description:
      "Production, stock, purchasing, quality and order information should support decisions without requiring managers to reconstruct the operation manually.",
  },
];

export const manufacturingCapabilities: ManufacturingCapability[] = [
  {
    number: "01",
    title: "Manufacturing & ERP Systems",
    href: "/services/software-development/erp-development/",
    description:
      "Develop or extend systems around production orders, materials, inventory, purchasing, work stages and operational reporting.",
    outcomes: [
      "Production visibility",
      "Inventory control",
      "Procurement workflows",
      "Operational reporting",
    ],
  },
  {
    number: "02",
    title: "Inventory Management",
    href: "/services/software-development/inventory-systems/",
    description:
      "Track raw materials, components, finished goods and stock movements through structured inventory workflows.",
    outcomes: [
      "Stock visibility",
      "Movement history",
      "Reorder awareness",
      "Reduced duplication",
    ],
  },
  {
    number: "03",
    title: "Production Workflow Software",
    href: "/services/software-development/custom-software/",
    description:
      "Create tailored systems for work orders, production stages, approvals, status changes and manufacturing-specific operational rules.",
    outcomes: [
      "Work orders",
      "Stage tracking",
      "Status visibility",
      "Process control",
    ],
  },
  {
    number: "04",
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Automate predictable manufacturing administration such as alerts, approvals, stock triggers and recurring workflow events.",
    outcomes: [
      "Workflow alerts",
      "Approval automation",
      "Stock triggers",
      "Less manual administration",
    ],
  },
  {
    number: "05",
    title: "API & System Integration",
    href: "/services/api-integration/",
    description:
      "Connect supported ERP, inventory, accounting, CRM, ecommerce or operational systems where reliable integration methods are available.",
    outcomes: [
      "Connected systems",
      "Reduced re-entry",
      "Data exchange",
      "Process continuity",
    ],
  },
  {
    number: "06",
    title: "Data & Analytics",
    href: "/services/data-analytics/",
    description:
      "Build dashboards and reports around production, stock, purchasing, order status and other available operational data.",
    outcomes: [
      "Production reporting",
      "Inventory insight",
      "KPI visibility",
      "Management dashboards",
    ],
  },
  {
    number: "07",
    title: "Cloud & Infrastructure",
    href: "/services/cloud-hosting/",
    description:
      "Support manufacturing software and connected operational systems with reliable infrastructure, monitoring and backup planning.",
    outcomes: [
      "Reliable hosting",
      "Monitoring",
      "Backups",
      "Operational resilience",
    ],
  },
  {
    number: "08",
    title: "IT Consultancy",
    href: "/services/it-consultancy/",
    description:
      "Assess operational systems, integration requirements and transformation priorities before committing to significant software changes.",
    outcomes: [
      "System assessment",
      "Architecture guidance",
      "Integration planning",
      "Technology roadmap",
    ],
  },
];

export const manufacturingPrinciples: ManufacturingPrinciple[] = [
  {
    number: "01",
    title: "Model the real production process",
    description:
      "Software should reflect how materials, work orders, production stages and approvals actually move through the organisation.",
  },
  {
    number: "02",
    title: "Keep stock movements traceable",
    description:
      "Inventory adjustments, transfers, receipts and consumption should have enough context to support operational review.",
  },
  {
    number: "03",
    title: "Automate stable rules, not exceptions",
    description:
      "Predictable manufacturing processes are good automation candidates, while exceptional cases should remain visible to responsible staff.",
  },
  {
    number: "04",
    title: "Measure throughput and constraints",
    description:
      "Operational reporting should help identify delays, shortages, bottlenecks and capacity issues rather than simply generating more dashboards.",
  },
];

export const manufacturingFlow: ManufacturingFlow[] = [
  {
    number: "01",
    title: "Plan",
    description:
      "Orders, demand, materials and capacity inform what needs to be produced and when.",
  },
  {
    number: "02",
    title: "Procure",
    description:
      "Required materials and components are identified, purchased and received into controlled stock.",
  },
  {
    number: "03",
    title: "Produce",
    description:
      "Work orders and production stages move through the defined manufacturing workflow.",
  },
  {
    number: "04",
    title: "Inspect",
    description:
      "Quality or approval steps record whether output is ready to proceed or requires corrective action.",
  },
  {
    number: "05",
    title: "Store",
    description:
      "Finished goods and remaining materials are reflected accurately in inventory records.",
  },
  {
    number: "06",
    title: "Deliver",
    description:
      "Orders move into dispatch, fulfilment or subsequent operational workflows with clear status visibility.",
  },
];
