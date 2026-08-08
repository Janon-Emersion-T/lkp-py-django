export interface AutomationService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface AutomationPrinciple {
  number: string;
  title: string;
  description: string;
}

export const automationServices: AutomationService[] = [
  {
    number: "01",
    title: "Workflow Automation",
    href: "/services/business-automation/workflow-automation/",
    description:
      "Replace repetitive manual steps with structured workflows that move information, tasks and approvals through the business more consistently.",
    capabilities: [
      "Task routing",
      "Approval workflows",
      "Process triggers",
      "System coordination",
    ],
  },
  {
    number: "02",
    title: "CRM Automation",
    href: "/services/business-automation/crm-automation/",
    description:
      "Automate customer and sales processes so leads, follow-ups, records and internal actions move through the CRM with less manual intervention.",
    capabilities: [
      "Lead routing",
      "Follow-up automation",
      "Pipeline actions",
      "Customer notifications",
    ],
  },
  {
    number: "03",
    title: "HR Automation",
    href: "/services/business-automation/hr-automation/",
    description:
      "Streamline recurring HR administration across employee records, onboarding, approvals, attendance, documentation and internal requests.",
    capabilities: [
      "Employee onboarding",
      "Approval processes",
      "HR notifications",
      "Record workflows",
    ],
  },
  {
    number: "04",
    title: "Document Automation",
    href: "/services/business-automation/document-automation/",
    description:
      "Generate, route, process and manage business documents using structured data and repeatable rules instead of manual preparation.",
    capabilities: [
      "Document generation",
      "Template automation",
      "Approval routing",
      "Data-driven documents",
    ],
  },
];

export const automationPrinciples: AutomationPrinciple[] = [
  {
    number: "01",
    title: "Automate a defined process",
    description:
      "Automation works best when the underlying process is understood first. Automating confusion simply makes confusion move faster.",
  },
  {
    number: "02",
    title: "Keep human decisions where they matter",
    description:
      "Not every step should be automated. Judgement, exceptions and approvals still need appropriate human control.",
  },
  {
    number: "03",
    title: "Connect existing systems",
    description:
      "Useful automation often comes from coordinating tools the business already uses rather than replacing everything.",
  },
  {
    number: "04",
    title: "Make exceptions visible",
    description:
      "Good automation handles routine work while clearly surfacing cases that require attention.",
  },
];
