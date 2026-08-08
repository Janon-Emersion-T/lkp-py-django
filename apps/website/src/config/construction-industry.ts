export interface ConstructionChallenge {
  number: string;
  title: string;
  description: string;
}

export interface ConstructionCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface ConstructionPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface ConstructionFlow {
  number: string;
  title: string;
  description: string;
}

export const constructionChallenges: ConstructionChallenge[] = [
  {
    number: "01",
    title: "Project information changes constantly",
    description:
      "Drawings, quotations, approvals, material requirements, site updates and client decisions can change throughout a project, making version control and communication difficult.",
  },
  {
    number: "02",
    title: "Site and office information can drift apart",
    description:
      "Project managers, site teams, finance staff, subcontractors and management may each work from different records unless the workflow is structured.",
  },
  {
    number: "03",
    title: "Procurement delays affect the programme",
    description:
      "Materials, supplier quotations, purchase approvals and deliveries need visibility because one late item can disrupt multiple downstream activities.",
  },
  {
    number: "04",
    title: "Progress is difficult to assess from memory",
    description:
      "Reliable project oversight needs recorded milestones, status updates, costs, issues and decisions rather than informal verbal reporting.",
  },
];

export const constructionCapabilities: ConstructionCapability[] = [
  {
    number: "01",
    title: "Construction Management Software",
    href: "/services/software-development/custom-software/",
    description:
      "Custom systems for projects, phases, site updates, approvals, documents, subcontractors, materials and management reporting.",
    outcomes: [
      "Project visibility",
      "Site coordination",
      "Structured records",
      "Management reporting",
    ],
  },
  {
    number: "02",
    title: "Quotation & Estimation Workflows",
    href: "/services/software-development/custom-software/",
    description:
      "Digitise quotation, estimation and approval workflows where project pricing currently depends on spreadsheets and manual handovers.",
    outcomes: [
      "Quotation tracking",
      "Estimate control",
      "Approval workflow",
      "Version visibility",
    ],
  },
  {
    number: "03",
    title: "BOQ & Cost Tracking",
    href: "/services/data-analytics/",
    description:
      "Structure cost information around quantities, budgets, committed costs, actual spending and project-level financial visibility.",
    outcomes: [
      "Budget visibility",
      "Cost tracking",
      "Variance awareness",
      "Project reporting",
    ],
  },
  {
    number: "04",
    title: "Procurement & Materials",
    href: "/services/software-development/inventory-systems/",
    description:
      "Track material requirements, purchase requests, supplier decisions, deliveries and stock movements across projects or stores.",
    outcomes: [
      "Material visibility",
      "Purchase tracking",
      "Delivery status",
      "Inventory control",
    ],
  },
  {
    number: "05",
    title: "Document & Approval Workflows",
    href: "/services/business-automation/",
    description:
      "Create structured workflows for documents, drawings, submissions, approvals and recurring project administration.",
    outcomes: [
      "Approval tracking",
      "Document control",
      "Status visibility",
      "Reduced follow-up",
    ],
  },
  {
    number: "06",
    title: "Mobile Site Workflows",
    href: "/services/mobile-app-development/",
    description:
      "Provide mobile-friendly access for site updates, inspections, photographs, task status and approved field workflows.",
    outcomes: [
      "Site updates",
      "Mobile access",
      "Photo records",
      "Field visibility",
    ],
  },
  {
    number: "07",
    title: "API & System Integration",
    href: "/services/api-integration/",
    description:
      "Connect supported accounting, ERP, CRM, document, procurement or communication platforms where suitable integration methods are available.",
    outcomes: [
      "Connected systems",
      "Reduced re-entry",
      "Data exchange",
      "Workflow continuity",
    ],
  },
  {
    number: "08",
    title: "Project Dashboards & Analytics",
    href: "/services/data-analytics/",
    description:
      "Create management dashboards around project progress, costs, procurement, issues, milestones and other available operational data.",
    outcomes: [
      "Progress reporting",
      "Cost visibility",
      "Project KPIs",
      "Management insight",
    ],
  },
];

export const constructionPrinciples: ConstructionPrinciple[] = [
  {
    number: "01",
    title: "Keep one project record",
    description:
      "Important project information should have a clear authoritative source rather than living in separate spreadsheets, chat threads and individual devices.",
  },
  {
    number: "02",
    title: "Record decisions, not just outcomes",
    description:
      "Approvals, changes and exceptions need enough context to understand who decided what and when.",
  },
  {
    number: "03",
    title: "Make site workflows practical",
    description:
      "Field systems must work on the devices, connectivity and time constraints that site teams actually have.",
  },
  {
    number: "04",
    title: "Expose delays early",
    description:
      "The value of project software is not merely recording history; it should help surface overdue approvals, procurement risk and stalled work before they become larger problems.",
  },
];

export const constructionFlow: ConstructionFlow[] = [
  {
    number: "01",
    title: "Estimate",
    description:
      "Scope, quantities, rates and commercial assumptions are assembled into a controlled estimate or quotation.",
  },
  {
    number: "02",
    title: "Plan",
    description:
      "Project stages, responsibilities, material needs and key milestones are defined before execution.",
  },
  {
    number: "03",
    title: "Procure",
    description:
      "Materials, suppliers, approvals and delivery expectations are tracked against project requirements.",
  },
  {
    number: "04",
    title: "Build",
    description:
      "Site activities, tasks, updates and issues are recorded as the work progresses.",
  },
  {
    number: "05",
    title: "Review",
    description:
      "Progress, quality, cost, approvals and exceptions are reviewed against the project plan.",
  },
  {
    number: "06",
    title: "Close",
    description:
      "Completion records, outstanding items, documentation and project information are brought into a controlled closeout process.",
  },
];
