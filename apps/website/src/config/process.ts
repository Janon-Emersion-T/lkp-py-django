export interface ProcessStage {
  number: string;
  title: string;
  shortTitle: string;
  description: string;
  outputs: string[];
}

export interface ProcessPrinciple {
  number: string;
  title: string;
  description: string;
}

export const processPrinciples: ProcessPrinciple[] = [
  {
    number: "01",
    title: "Understand before building",
    description:
      "We begin with the business problem, operating context, users and expected outcome rather than jumping straight into implementation.",
  },
  {
    number: "02",
    title: "Make the scope visible",
    description:
      "Requirements, responsibilities, assumptions and priorities are made clear so the project does not depend on guesswork.",
  },
  {
    number: "03",
    title: "Communicate throughout",
    description:
      "Progress, decisions, risks and changes should remain visible throughout delivery instead of appearing only at the end.",
  },
  {
    number: "04",
    title: "Validate before release",
    description:
      "Quality assurance, review and practical validation are part of delivery, not an optional final-minute activity.",
  },
];

export const processStages: ProcessStage[] = [
  {
    number: "01",
    shortTitle: "Understand",
    title: "Discovery & context",
    description:
      "We establish what needs to change, why it matters, who it affects and what a successful outcome should look like.",
    outputs: [
      "Business context",
      "Objectives",
      "User requirements",
      "Constraints",
    ],
  },
  {
    number: "02",
    shortTitle: "Define",
    title: "Scope & planning",
    description:
      "The work is translated into a practical scope, priorities, responsibilities and delivery plan before execution begins.",
    outputs: ["Project scope", "Requirements", "Priorities", "Delivery plan"],
  },
  {
    number: "03",
    shortTitle: "Architect",
    title: "Solution design",
    description:
      "We determine the appropriate structure, technology, user experience and implementation approach for the problem.",
    outputs: [
      "Architecture",
      "Technical approach",
      "UX direction",
      "Integration plan",
    ],
  },
  {
    number: "04",
    shortTitle: "Build",
    title: "Execution & integration",
    description:
      "The approved solution is implemented in controlled stages, with integration and technical decisions handled as part of the build.",
    outputs: [
      "Implementation",
      "Integrations",
      "Working increments",
      "Progress reviews",
    ],
  },
  {
    number: "05",
    shortTitle: "Validate",
    title: "Testing & refinement",
    description:
      "We review functionality, quality, performance and practical usability, correcting issues before final delivery.",
    outputs: [
      "Quality assurance",
      "Testing",
      "Refinement",
      "Acceptance review",
    ],
  },
  {
    number: "06",
    shortTitle: "Deliver",
    title: "Launch & handover",
    description:
      "The completed work is prepared for real use with deployment, access, documentation and necessary handover activities.",
    outputs: [
      "Deployment",
      "Documentation",
      "Access handover",
      "Operational readiness",
    ],
  },
  {
    number: "07",
    shortTitle: "Improve",
    title: "Support & evolution",
    description:
      "Delivery is not treated as the end of the relationship. Where required, we support, maintain, measure and improve what has been built.",
    outputs: ["Support", "Maintenance", "Optimisation", "Future roadmap"],
  },
];
