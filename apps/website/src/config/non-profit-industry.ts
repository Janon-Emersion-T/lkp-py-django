export interface NonProfitChallenge {
  number: string;
  title: string;
  description: string;
}

export interface NonProfitCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface NonProfitPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface NonProfitFlow {
  number: string;
  title: string;
  description: string;
}

export const nonProfitChallenges: NonProfitChallenge[] = [
  {
    number: "01",
    title: "Supporter information is often fragmented",
    description:
      "Donors, volunteers, partners, beneficiaries and campaign contacts can end up spread across spreadsheets, email accounts and disconnected platforms.",
  },
  {
    number: "02",
    title: "Programme reporting consumes operational time",
    description:
      "Teams may spend significant effort gathering activity, budget and outcome information from separate sources before they can report on programmes or grants.",
  },
  {
    number: "03",
    title: "Communication needs different audiences",
    description:
      "Donors, volunteers, beneficiaries, partners and internal staff often require different messages, permissions and engagement workflows.",
  },
  {
    number: "04",
    title: "Limited budgets make poor technology decisions expensive",
    description:
      "Non-profits need systems that solve real operational problems without creating unnecessary licensing, maintenance or implementation costs.",
  },
];

export const nonProfitCapabilities: NonProfitCapability[] = [
  {
    number: "01",
    title: "Non-profit Websites",
    href: "/services/web-development/business-websites/",
    description:
      "Build clear, credible websites for organisations that need to communicate mission, programmes, impact, opportunities and ways to support the work.",
    outcomes: [
      "Mission visibility",
      "Programme information",
      "Supporter engagement",
      "Responsive access",
    ],
  },
  {
    number: "02",
    title: "Donation & Campaign Workflows",
    href: "/services/web-development/ecommerce-websites/",
    description:
      "Support approved online donation, campaign and contribution journeys through suitable payment and transaction workflows.",
    outcomes: [
      "Online donations",
      "Campaign support",
      "Payment workflows",
      "Donor convenience",
    ],
  },
  {
    number: "03",
    title: "Donor & Supporter CRM",
    href: "/services/software-development/crm-development/",
    description:
      "Centralise supporter records, interactions, campaigns and relationship history where generic spreadsheets no longer provide enough structure.",
    outcomes: [
      "Supporter records",
      "Interaction history",
      "Campaign visibility",
      "Relationship management",
    ],
  },
  {
    number: "04",
    title: "Volunteer Management",
    href: "/services/software-development/custom-software/",
    description:
      "Develop workflows for volunteer registration, availability, assignments, records and communication where the organisation needs more operational control.",
    outcomes: [
      "Volunteer records",
      "Assignments",
      "Availability",
      "Communication",
    ],
  },
  {
    number: "05",
    title: "Programme & Grant Administration",
    href: "/services/software-development/custom-software/",
    description:
      "Structure programme, project, grant, milestone, document and reporting workflows around the organisation's actual operating model.",
    outcomes: [
      "Programme tracking",
      "Grant visibility",
      "Milestones",
      "Structured reporting",
    ],
  },
  {
    number: "06",
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Automate predictable notifications, acknowledgements, approvals, reminders and recurring administrative activities.",
    outcomes: [
      "Acknowledgements",
      "Notifications",
      "Reminder workflows",
      "Less manual administration",
    ],
  },
  {
    number: "07",
    title: "Data & Impact Reporting",
    href: "/services/data-analytics/",
    description:
      "Create dashboards and reports around programmes, campaigns, donations, volunteers and other available operational data.",
    outcomes: [
      "Programme visibility",
      "Campaign reporting",
      "Operational insight",
      "Management dashboards",
    ],
  },
  {
    number: "08",
    title: "API & Platform Integration",
    href: "/services/api-integration/",
    description:
      "Connect supported donation, CRM, accounting, communication and operational platforms where appropriate integration methods are available.",
    outcomes: [
      "Connected systems",
      "Reduced duplication",
      "Data exchange",
      "Workflow continuity",
    ],
  },
];

export const nonProfitPrinciples: NonProfitPrinciple[] = [
  {
    number: "01",
    title: "Spend technology budget on real operational value",
    description:
      "Systems should reduce administrative burden, improve visibility or strengthen supporter engagement rather than adding software simply because it exists.",
  },
  {
    number: "02",
    title: "Treat supporter data responsibly",
    description:
      "Collect and retain information for clear organisational purposes, with access limited according to responsibility.",
  },
  {
    number: "03",
    title: "Keep reporting connected to source activity",
    description:
      "Impact and programme reporting becomes more reliable when operational information is captured consistently rather than reconstructed after the fact.",
  },
  {
    number: "04",
    title: "Preserve organisational ownership",
    description:
      "Important domains, accounts, data and digital assets should remain under appropriate organisational control rather than becoming permanently dependent on one vendor.",
  },
];

export const nonProfitFlow: NonProfitFlow[] = [
  {
    number: "01",
    title: "Reach",
    description:
      "People discover the organisation, its mission, programmes and opportunities to contribute or participate.",
  },
  {
    number: "02",
    title: "Engage",
    description:
      "Supporters, volunteers, partners or beneficiaries enter the appropriate communication or participation workflow.",
  },
  {
    number: "03",
    title: "Coordinate",
    description:
      "Teams organise activities, programmes, volunteers, contributions and internal responsibilities.",
  },
  {
    number: "04",
    title: "Deliver",
    description:
      "Programmes and services move forward with operational information recorded in a structured way.",
  },
  {
    number: "05",
    title: "Report",
    description:
      "Programme, campaign and operational information supports management, donor and stakeholder reporting.",
  },
  {
    number: "06",
    title: "Sustain",
    description:
      "Supporter relationships, organisational knowledge and digital systems continue beyond one campaign or funding cycle.",
  },
];
