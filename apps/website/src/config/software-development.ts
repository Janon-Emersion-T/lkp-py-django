export interface SoftwareDevelopmentService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface SoftwarePrinciple {
  number: string;
  title: string;
  description: string;
}

export interface SoftwareStage {
  number: string;
  title: string;
  description: string;
}

export const softwareDevelopmentServices: SoftwareDevelopmentService[] = [
  {
    number: "01",
    title: "Custom Software",
    href: "/services/software-development/custom-software/",
    description:
      "Purpose-built applications designed around business workflows, users, permissions, data and operational requirements.",
    capabilities: [
      "Business applications",
      "Custom workflows",
      "Internal systems",
      "API-driven software",
    ],
  },
  {
    number: "02",
    title: "ERP Development",
    href: "/services/software-development/erp-development/",
    description:
      "Integrated operational systems that bring core business processes, data and management visibility into a structured platform.",
    capabilities: [
      "Operations management",
      "Finance workflows",
      "Inventory",
      "Business reporting",
    ],
  },
  {
    number: "03",
    title: "CRM Development",
    href: "/services/software-development/crm-development/",
    description:
      "Customer relationship systems built around how the organisation captures leads, manages opportunities and serves customers.",
    capabilities: [
      "Lead management",
      "Sales pipelines",
      "Customer records",
      "Follow-up workflows",
    ],
  },
  {
    number: "04",
    title: "POS Systems",
    href: "/services/software-development/pos-systems/",
    description:
      "Point-of-sale systems designed to support real transactional workflows, products, payments, staff and reporting requirements.",
    capabilities: [
      "Sales processing",
      "Products",
      "Receipts",
      "Transaction reporting",
    ],
  },
  {
    number: "05",
    title: "Inventory Systems",
    href: "/services/software-development/inventory-systems/",
    description:
      "Inventory management software that gives businesses clearer control over stock movement, availability and operational records.",
    capabilities: [
      "Stock tracking",
      "Movements",
      "Reorder visibility",
      "Inventory reporting",
    ],
  },
  {
    number: "06",
    title: "HRM Systems",
    href: "/services/software-development/hrm-systems/",
    description:
      "Human resource systems for employee records, attendance, leave, onboarding and recurring administrative workflows.",
    capabilities: [
      "Employee records",
      "Attendance",
      "Leave workflows",
      "HR administration",
    ],
  },
  {
    number: "07",
    title: "Accounting Systems",
    href: "/services/software-development/accounting-systems/",
    description:
      "Business accounting applications designed around transactions, financial records, reporting and operational integration.",
    capabilities: [
      "Income & expenses",
      "Ledgers",
      "Financial reports",
      "Operational integration",
    ],
  },
  {
    number: "08",
    title: "SaaS Development",
    href: "/services/software-development/saas-development/",
    description:
      "Multi-user software products designed for recurring online delivery, account management and long-term product operation.",
    capabilities: [
      "Multi-tenant systems",
      "Subscriptions",
      "Account management",
      "Product platforms",
    ],
  },
];

export const softwarePrinciples: SoftwarePrinciple[] = [
  {
    number: "01",
    title: "Model the business before the database",
    description:
      "Software structure should follow how the organisation actually operates rather than forcing business processes into arbitrary technical models.",
  },
  {
    number: "02",
    title: "Keep responsibilities separated",
    description:
      "Modular boundaries make software easier to understand, test, maintain and extend as requirements change.",
  },
  {
    number: "03",
    title: "Protect data integrity",
    description:
      "Permissions, validation, transactions and auditability matter because business software becomes part of the organisation's operational record.",
  },
  {
    number: "04",
    title: "Build for change",
    description:
      "Requirements evolve. Good architecture should allow deliberate change without turning every new feature into a risky rewrite.",
  },
];

export const softwareStages: SoftwareStage[] = [
  {
    number: "01",
    title: "Understand",
    description:
      "Study the business problem, users, workflows, existing systems and operational constraints.",
  },
  {
    number: "02",
    title: "Define",
    description:
      "Translate the requirement into roles, processes, data structures, integrations and acceptance criteria.",
  },
  {
    number: "03",
    title: "Architect",
    description:
      "Choose technical boundaries and an implementation approach appropriate for the system's real responsibilities.",
  },
  {
    number: "04",
    title: "Develop",
    description:
      "Build the software incrementally with clear modules, interfaces and testable behaviour.",
  },
  {
    number: "05",
    title: "Validate",
    description:
      "Test workflows, permissions, edge cases, integrations and business rules against realistic scenarios.",
  },
  {
    number: "06",
    title: "Operate",
    description:
      "Deploy, monitor and maintain the system as users, data and business requirements evolve.",
  },
];
