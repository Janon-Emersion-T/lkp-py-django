export interface GovernmentChallenge {
  number: string;
  title: string;
  description: string;
}

export interface GovernmentCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface GovernmentPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface GovernmentFlow {
  number: string;
  title: string;
  description: string;
}

export const governmentChallenges: GovernmentChallenge[] = [
  {
    number: "01",
    title: "Administrative workflows cross multiple responsibilities",
    description:
      "Requests, documents and approvals may move between officers, departments and management levels. Without structured workflows, status and ownership can become difficult to determine.",
  },
  {
    number: "02",
    title: "Public services must remain understandable",
    description:
      "Digital services should make it clear what information is required, what happens next and how users can complete a process without unnecessary complexity.",
  },
  {
    number: "03",
    title: "Legacy and disconnected systems create duplication",
    description:
      "Departments may rely on separate databases, spreadsheets, paper records and specialist applications, increasing repeated entry and making organisation-wide visibility difficult.",
  },
  {
    number: "04",
    title: "Long-term maintainability matters",
    description:
      "Public-sector systems may remain operational for years. Documentation, architecture, access control and maintainable implementation therefore matter beyond the initial launch.",
  },
];

export const governmentCapabilities: GovernmentCapability[] = [
  {
    number: "01",
    title: "Public Service Portals",
    href: "/services/web-development/custom-web-applications/",
    description:
      "Develop web-based portals for appropriate applications, requests, information, submissions and public-service workflows.",
    outcomes: [
      "Digital services",
      "Online submissions",
      "Status visibility",
      "Responsive access",
    ],
  },
  {
    number: "02",
    title: "Administrative Management Systems",
    href: "/services/software-development/custom-software/",
    description:
      "Build internal systems around cases, records, requests, approvals, departments and organisation-specific administrative processes.",
    outcomes: [
      "Case management",
      "Structured records",
      "Workflow visibility",
      "Administrative control",
    ],
  },
  {
    number: "03",
    title: "Document & Approval Workflows",
    href: "/services/business-automation/",
    description:
      "Digitise predictable document routing, review, approval, notification and administrative workflows.",
    outcomes: [
      "Approval routing",
      "Document status",
      "Notifications",
      "Reduced manual follow-up",
    ],
  },
  {
    number: "04",
    title: "Mobile Applications",
    href: "/services/mobile-app-development/",
    description:
      "Develop mobile experiences for appropriate public, staff or field workflows where mobile access materially improves service delivery.",
    outcomes: [
      "Mobile access",
      "Field workflows",
      "Service availability",
      "Responsive interaction",
    ],
  },
  {
    number: "05",
    title: "API & System Integration",
    href: "/services/api-integration/",
    description:
      "Connect supported departmental, administrative and third-party systems where approved interfaces and suitable integration mechanisms are available.",
    outcomes: [
      "Connected systems",
      "Reduced duplication",
      "Controlled data exchange",
      "Workflow continuity",
    ],
  },
  {
    number: "06",
    title: "Data & Reporting",
    href: "/services/data-analytics/",
    description:
      "Create operational dashboards and reports around available service, case, programme and administrative data.",
    outcomes: [
      "Operational reporting",
      "Programme visibility",
      "Service metrics",
      "Management insight",
    ],
  },
  {
    number: "07",
    title: "Cybersecurity",
    href: "/services/cybersecurity/",
    description:
      "Assess and strengthen approved systems through security reviews, access-control considerations, hardening, monitoring and recovery planning.",
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
      "Plan and support suitable application infrastructure around availability, monitoring, backups, administration and operational requirements.",
    outcomes: [
      "Reliable infrastructure",
      "Monitoring",
      "Backup planning",
      "Operational resilience",
    ],
  },
];

export const governmentPrinciples: GovernmentPrinciple[] = [
  {
    number: "01",
    title: "Design around the service, not the department chart",
    description:
      "A digital workflow should follow the actual journey of the request or service while preserving the responsibilities and approvals required internally.",
  },
  {
    number: "02",
    title: "Make status and ownership visible",
    description:
      "Authorised staff should be able to determine where a request sits, who is responsible for the next action and what has already occurred.",
  },
  {
    number: "03",
    title: "Keep public interfaces straightforward",
    description:
      "Public-facing services should use clear language, responsive layouts and practical interaction patterns rather than exposing internal administrative complexity.",
  },
  {
    number: "04",
    title: "Build for maintainability",
    description:
      "Documentation, modular architecture and controlled change matter when systems are expected to remain useful beyond the initial project team.",
  },
];

export const governmentFlow: GovernmentFlow[] = [
  {
    number: "01",
    title: "Submit",
    description:
      "A citizen, organisation or authorised staff member provides the information required to begin the service or administrative process.",
  },
  {
    number: "02",
    title: "Validate",
    description:
      "Required information and defined business rules are checked before the request proceeds.",
  },
  {
    number: "03",
    title: "Route",
    description:
      "The request moves to the appropriate department, officer or workflow stage according to defined responsibilities.",
  },
  {
    number: "04",
    title: "Review",
    description:
      "Authorised personnel assess the request, documentation or case and record the required action.",
  },
  {
    number: "05",
    title: "Resolve",
    description:
      "The approved outcome, service action or administrative decision is recorded and progressed.",
  },
  {
    number: "06",
    title: "Record",
    description:
      "Relevant workflow history and outcome information remain available according to the system's authorised record-management requirements.",
  },
];
