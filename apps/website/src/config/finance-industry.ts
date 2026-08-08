export interface FinanceChallenge {
  number: string;
  title: string;
  description: string;
}

export interface FinanceCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface FinancePrinciple {
  number: string;
  title: string;
  description: string;
}

export interface FinanceFlow {
  number: string;
  title: string;
  description: string;
}

export const financeChallenges: FinanceChallenge[] = [
  {
    number: "01",
    title: "Access must reflect responsibility",
    description:
      "Financial and commercially sensitive information should not be broadly available. Systems need deliberate roles, permissions and administrative boundaries.",
  },
  {
    number: "02",
    title: "Approvals need traceable context",
    description:
      "Payments, adjustments, quotations, expenses and other important financial actions often require clear approval states and a record of who acted and when.",
  },
  {
    number: "03",
    title: "Disconnected records make reconciliation harder",
    description:
      "Transactions, customer records, invoices, payments and operational systems become difficult to reconcile when the same information is repeatedly entered across separate platforms.",
  },
  {
    number: "04",
    title: "Management reporting depends on reliable source data",
    description:
      "Dashboards and financial reports are useful only when the underlying records, definitions and data flows are maintained consistently.",
  },
];

export const financeCapabilities: FinanceCapability[] = [
  {
    number: "01",
    title: "Finance & Operational Software",
    href: "/services/software-development/custom-software/",
    description:
      "Develop tailored systems around financial administration, transactions, approvals, records and organisation-specific operating workflows.",
    outcomes: [
      "Structured workflows",
      "Controlled access",
      "Approval states",
      "Operational records",
    ],
  },
  {
    number: "02",
    title: "ERP Development",
    href: "/services/software-development/erp-development/",
    description:
      "Connect finance-related information with customers, projects, purchasing, inventory and wider operational processes through structured ERP workflows.",
    outcomes: [
      "Unified operations",
      "Financial visibility",
      "Cross-team workflows",
      "Structured records",
    ],
  },
  {
    number: "03",
    title: "CRM Development",
    href: "/services/software-development/crm-development/",
    description:
      "Manage customer, lead and commercial information through controlled workflows that can connect with quotation, invoicing or service processes.",
    outcomes: [
      "Customer records",
      "Pipeline visibility",
      "Commercial history",
      "Structured follow-up",
    ],
  },
  {
    number: "04",
    title: "API & Financial System Integration",
    href: "/services/api-integration/",
    description:
      "Connect supported accounting, payment, ERP, CRM and operational platforms where appropriate APIs or integration mechanisms are available.",
    outcomes: [
      "Connected systems",
      "Reduced re-entry",
      "Data exchange",
      "Workflow continuity",
    ],
  },
  {
    number: "05",
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Automate predictable administrative steps such as approval routing, notifications, document generation and recurring workflow actions.",
    outcomes: [
      "Approval routing",
      "Notifications",
      "Document workflows",
      "Less manual administration",
    ],
  },
  {
    number: "06",
    title: "Data & Analytics",
    href: "/services/data-analytics/",
    description:
      "Create dashboards and reports around revenue, expenditure, receivables, project finance and other available business information.",
    outcomes: [
      "Financial reporting",
      "KPI visibility",
      "Management dashboards",
      "Decision support",
    ],
  },
  {
    number: "07",
    title: "Cybersecurity",
    href: "/services/cybersecurity/",
    description:
      "Strengthen financial and business systems through security reviews, access controls, hardening, monitoring considerations and recovery planning.",
    outcomes: [
      "Risk reduction",
      "Access protection",
      "System hardening",
      "Recovery planning",
    ],
  },
  {
    number: "08",
    title: "Cloud & Infrastructure",
    href: "/services/cloud-hosting/",
    description:
      "Support approved finance and operational applications with infrastructure designed around reliability, monitoring, backups and controlled administration.",
    outcomes: [
      "Reliable hosting",
      "Monitoring",
      "Backups",
      "Operational resilience",
    ],
  },
];

export const financePrinciples: FinancePrinciple[] = [
  {
    number: "01",
    title: "Separate duties where the workflow requires it",
    description:
      "Creating, approving and administering important financial actions should not automatically belong to the same user when stronger controls are appropriate.",
  },
  {
    number: "02",
    title: "Preserve important audit history",
    description:
      "Sensitive changes and approvals should retain enough information to understand what changed, who performed the action and when it occurred.",
  },
  {
    number: "03",
    title: "Do not automate ambiguity",
    description:
      "Financial automation should execute defined rules. Exceptions and unclear conditions should remain visible to responsible staff rather than being silently guessed by software.",
  },
  {
    number: "04",
    title: "Protect source data before polishing dashboards",
    description:
      "Reporting quality depends on accurate records, consistent definitions and reliable integrations more than visual complexity.",
  },
];

export const financeFlow: FinanceFlow[] = [
  {
    number: "01",
    title: "Capture",
    description:
      "A transaction, request, document or financial event enters the system with the required supporting information.",
  },
  {
    number: "02",
    title: "Validate",
    description:
      "Required fields, business rules and available source information are checked before the workflow moves forward.",
  },
  {
    number: "03",
    title: "Approve",
    description:
      "Authorised users review actions that require control before commitment or processing.",
  },
  {
    number: "04",
    title: "Process",
    description:
      "The approved event moves through the defined financial or operational workflow.",
  },
  {
    number: "05",
    title: "Reconcile",
    description:
      "Related records and system information can be reviewed for consistency and unresolved differences.",
  },
  {
    number: "06",
    title: "Report",
    description:
      "Structured data supports financial and management visibility appropriate to the organisation.",
  },
];
