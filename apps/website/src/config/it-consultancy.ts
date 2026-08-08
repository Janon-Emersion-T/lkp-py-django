export interface ConsultancyService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface ConsultancyPrinciple {
  number: string;
  title: string;
  description: string;
}

export const consultancyServices: ConsultancyService[] = [
  {
    number: "01",
    title: "Digital Transformation",
    href: "/services/it-consultancy/digital-transformation/",
    description:
      "Review how technology supports the organisation and identify practical opportunities to improve operations, customer experience and internal capability.",
    capabilities: [
      "Current-state assessment",
      "Process improvement",
      "Technology roadmap",
      "Transformation planning",
    ],
  },
  {
    number: "02",
    title: "Technology Consulting",
    href: "/services/it-consultancy/technology-consulting/",
    description:
      "Independent technical guidance for technology choices, architecture, platforms, infrastructure and implementation decisions.",
    capabilities: [
      "Technology selection",
      "Architecture guidance",
      "Platform evaluation",
      "Technical strategy",
    ],
  },
  {
    number: "03",
    title: "System Integration",
    href: "/services/it-consultancy/system-integration/",
    description:
      "Plan how business systems, data and operational workflows should connect before implementation begins.",
    capabilities: [
      "Integration planning",
      "System boundaries",
      "Data ownership",
      "Operational design",
    ],
  },
  {
    number: "04",
    title: "Project Consulting",
    href: "/services/it-consultancy/project-consulting/",
    description:
      "Provide technical and delivery guidance for technology projects that need clearer requirements, stronger oversight or independent review.",
    capabilities: [
      "Requirements review",
      "Project planning",
      "Technical oversight",
      "Delivery review",
    ],
  },
];

export const consultancyPrinciples: ConsultancyPrinciple[] = [
  {
    number: "01",
    title: "Start with the business problem",
    description:
      "The technology decision should follow the operational or commercial need rather than starting with a preferred product.",
  },
  {
    number: "02",
    title: "Challenge unnecessary complexity",
    description:
      "More systems, features and integrations are not automatically better. Complexity needs a business reason.",
  },
  {
    number: "03",
    title: "Consider the operating reality",
    description:
      "A solution must fit the organisation's people, skills, processes, budget and ability to maintain it.",
  },
  {
    number: "04",
    title: "Think beyond implementation",
    description:
      "Architecture, ownership, support, security and future change matter after the initial project is completed.",
  },
];
