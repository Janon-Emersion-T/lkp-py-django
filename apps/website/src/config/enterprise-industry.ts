export interface EnterpriseChallenge {
  number: string;
  title: string;
  description: string;
}

export interface EnterpriseCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface EnterprisePrinciple {
  number: string;
  title: string;
  description: string;
}

export interface EnterpriseStage {
  number: string;
  title: string;
  description: string;
}

export const enterpriseChallenges: EnterpriseChallenge[] = [
  {
    number: "01",
    title: "Legacy systems and fragmented ownership",
    description:
      "Enterprise environments often contain years of accumulated platforms, integrations, manual bridges and overlapping responsibilities that make change risky.",
  },
  {
    number: "02",
    title: "Complex stakeholder requirements",
    description:
      "Technology decisions must work for operations, management, finance, security, compliance and end users rather than satisfying one isolated team.",
  },
  {
    number: "03",
    title: "Scale magnifies weak architecture",
    description:
      "Small inefficiencies become serious operational problems when transaction volume, data, users and integrations increase.",
  },
  {
    number: "04",
    title: "Change must be controlled",
    description:
      "Enterprise transformation cannot rely on ad-hoc deployment. Rollout, testing, permissions, migration, rollback and continuity need deliberate planning.",
  },
];

export const enterpriseCapabilities: EnterpriseCapability[] = [
  {
    number: "01",
    title: "Enterprise Software Development",
    href: "/services/software-development/",
    description:
      "Design and develop operational platforms around complex workflows, permissions, business rules and organisational structures.",
    outcomes: [
      "Integrated workflows",
      "Role-based access",
      "Operational control",
      "Structured data",
    ],
  },
  {
    number: "02",
    title: "ERP & CRM Systems",
    href: "/services/software-development/erp-development/",
    description:
      "Create or extend systems that centralise operational and customer information across teams and business functions.",
    outcomes: [
      "Unified records",
      "Cross-team visibility",
      "Process control",
      "Reporting",
    ],
  },
  {
    number: "03",
    title: "API & System Integration",
    href: "/services/api-integration/",
    description:
      "Connect existing systems safely so information can move between platforms without relying on repeated manual transfer.",
    outcomes: [
      "Connected platforms",
      "Reduced duplication",
      "Data exchange",
      "Automation readiness",
    ],
  },
  {
    number: "04",
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Automate recurring operational processes where business rules are stable enough to support controlled execution.",
    outcomes: [
      "Process efficiency",
      "Fewer manual steps",
      "Consistent execution",
      "Faster turnaround",
    ],
  },
  {
    number: "05",
    title: "Cybersecurity",
    href: "/services/cybersecurity/",
    description:
      "Strengthen systems through security reviews, hardening, recovery planning and risk-focused technical controls.",
    outcomes: [
      "Risk reduction",
      "Hardening",
      "Recovery planning",
      "Security visibility",
    ],
  },
  {
    number: "06",
    title: "Cloud & Infrastructure",
    href: "/services/cloud-hosting/",
    description:
      "Support production systems with infrastructure designed around reliability, performance, security and operational ownership.",
    outcomes: [
      "Reliable hosting",
      "Scalable resources",
      "Monitoring",
      "Operational resilience",
    ],
  },
  {
    number: "07",
    title: "Data & Analytics",
    href: "/services/data-analytics/",
    description:
      "Turn operational data into structured dashboards, reports and decision-support information across departments.",
    outcomes: [
      "Management visibility",
      "KPI tracking",
      "Reporting",
      "Decision support",
    ],
  },
  {
    number: "08",
    title: "IT Consultancy",
    href: "/services/it-consultancy/",
    description:
      "Support architecture, transformation, integration and project decisions before significant technical commitments are made.",
    outcomes: [
      "Architecture guidance",
      "Transformation planning",
      "Risk assessment",
      "Technology governance",
    ],
  },
];

export const enterprisePrinciples: EnterprisePrinciple[] = [
  {
    number: "01",
    title: "Integrate before replacing unnecessarily",
    description:
      "Existing systems may still carry critical business value. Replacement should be based on operational need rather than assuming every legacy platform must disappear.",
  },
  {
    number: "02",
    title: "Design for ownership",
    description:
      "Infrastructure, code, data, accounts and operational responsibilities should remain understandable to the organisation that depends on them.",
  },
  {
    number: "03",
    title: "Control change deliberately",
    description:
      "Testing, migration, permissions, release management and rollback planning are part of delivery rather than last-minute deployment concerns.",
  },
  {
    number: "04",
    title: "Measure operational impact",
    description:
      "Enterprise technology should improve control, efficiency, reliability, visibility or capacity in ways that can be evaluated after implementation.",
  },
];

export const enterpriseStages: EnterpriseStage[] = [
  {
    number: "01",
    title: "Assess",
    description:
      "Understand the current systems, dependencies, business processes, risks and stakeholder requirements.",
  },
  {
    number: "02",
    title: "Prioritise",
    description:
      "Separate urgent operational constraints from improvements that can wait for later phases.",
  },
  {
    number: "03",
    title: "Architect",
    description:
      "Define system boundaries, integrations, data ownership, security and deployment strategy.",
  },
  {
    number: "04",
    title: "Deliver",
    description:
      "Implement in controlled phases with testing, review and measurable acceptance criteria.",
  },
  {
    number: "05",
    title: "Migrate",
    description:
      "Move users, data and workflows with clear validation, fallback and continuity planning.",
  },
  {
    number: "06",
    title: "Operate",
    description:
      "Monitor, support and improve the environment after systems become part of daily operations.",
  },
];
