export interface WhyChooseReason {
  number: string;
  title: string;
  description: string;
}

export interface WhyChooseProofPoint {
  label: string;
  value: string;
  note: string;
}

export const whyChooseReasons: WhyChooseReason[] = [
  {
    number: "01",
    title: "Business-first thinking",
    description:
      "Technology is only useful when it supports a real business objective. We begin with the problem, the users, the operating context and the result you need.",
  },
  {
    number: "02",
    title: "Broad technical capability",
    description:
      "Web, software, mobile, automation, infrastructure, SEO and digital growth can be considered together instead of being treated as disconnected problems.",
  },
  {
    number: "03",
    title: "Direct accountability",
    description:
      "Clients should know who is responsible for the work, the decisions and the outcome. We value ownership over unnecessary layers.",
  },
  {
    number: "04",
    title: "Modular engineering",
    description:
      "We prefer maintainable systems, clear boundaries and reusable components rather than fragile implementations that become difficult to extend.",
  },
  {
    number: "05",
    title: "Long-term perspective",
    description:
      "We look beyond launch day. Maintainability, support, performance, security and future changes are considered as part of delivery.",
  },
  {
    number: "06",
    title: "Practical communication",
    description:
      "Clients should understand what is happening, what has changed, what requires a decision and what comes next.",
  },
];

export const proofPoints: WhyChooseProofPoint[] = [
  {
    label: "History",
    value: "Since 2013",
    note: "Technology delivery experience developed over more than a decade.",
  },
  {
    label: "Base",
    value: "Jaffna, Sri Lanka",
    note: "A Sri Lankan technology company working with clients beyond local borders.",
  },
  {
    label: "Scope",
    value: "Multi-disciplinary",
    note: "Engineering, digital growth, infrastructure and business technology under one operating model.",
  },
  {
    label: "Approach",
    value: "Accountable",
    note: "Clear ownership, structured delivery and practical communication.",
  },
];
