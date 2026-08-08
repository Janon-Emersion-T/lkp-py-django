export interface MaintenanceService {
  number: string;
  title: string;
  href: string;
  description: string;
  includes: string[];
}

export interface MaintenanceCoverageItem {
  number: string;
  title: string;
  description: string;
}

export interface MaintenanceSupportModel {
  title: string;
  description: string;
  suitableFor: string;
}

export const maintenanceServices: MaintenanceService[] = [
  {
    number: "01",
    title: "Website Maintenance",
    href: "/services/maintenance-support/website-maintenance/",
    description:
      "Ongoing website care covering updates, issue resolution, monitoring, content changes, security and operational reliability.",
    includes: [
      "Platform and dependency updates",
      "Content and configuration changes",
      "Issue diagnosis and fixes",
      "Security and availability checks",
    ],
  },
  {
    number: "02",
    title: "Software Maintenance",
    href: "/services/maintenance-support/software-maintenance/",
    description:
      "Structured maintenance for business software, internal applications and custom systems after initial delivery.",
    includes: [
      "Bug resolution",
      "Compatibility maintenance",
      "Functional improvements",
      "Technical debt reduction",
    ],
  },
  {
    number: "03",
    title: "Performance Optimization",
    href: "/services/maintenance-support/performance-optimization/",
    description:
      "Technical review and improvement work focused on speed, efficiency, stability and resource use.",
    includes: [
      "Performance diagnosis",
      "Frontend and backend optimisation",
      "Database and query review",
      "Infrastructure efficiency",
    ],
  },
  {
    number: "04",
    title: "Technical Support",
    href: "/services/maintenance-support/technical-support/",
    description:
      "Practical technical assistance for incidents, configuration, troubleshooting and ongoing operational questions.",
    includes: [
      "Incident investigation",
      "Configuration support",
      "Technical guidance",
      "Escalation and resolution",
    ],
  },
];

export const maintenanceCoverage: MaintenanceCoverageItem[] = [
  {
    number: "01",
    title: "Prevent",
    description:
      "Routine maintenance reduces avoidable failures, outdated dependencies and operational surprises.",
  },
  {
    number: "02",
    title: "Monitor",
    description:
      "Availability, behaviour, performance and technical condition can be reviewed before users report a problem.",
  },
  {
    number: "03",
    title: "Respond",
    description:
      "When an issue does occur, responsibility and technical context matter more than starting the investigation from zero.",
  },
  {
    number: "04",
    title: "Improve",
    description:
      "Maintenance should also identify opportunities to improve performance, security, usability and maintainability.",
  },
];

export const supportModels: MaintenanceSupportModel[] = [
  {
    title: "Ongoing maintenance",
    description:
      "Recurring support for systems that require continuous technical ownership and routine maintenance.",
    suitableFor:
      "Business websites, software platforms and operational systems.",
  },
  {
    title: "Scheduled maintenance",
    description:
      "Planned maintenance performed at agreed intervals rather than through continuous support.",
    suitableFor:
      "Stable systems that need periodic technical review and upkeep.",
  },
  {
    title: "Ad-hoc technical support",
    description:
      "Support for specific incidents, changes or technical problems without a permanent maintenance arrangement.",
    suitableFor: "Businesses requiring occasional specialist assistance.",
  },
  {
    title: "Improvement projects",
    description:
      "Focused work when an existing system needs performance, security, architecture or maintainability improvements.",
    suitableFor:
      "Systems that work but have accumulated technical limitations.",
  },
];
