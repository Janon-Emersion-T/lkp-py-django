export interface SmallBusinessChallenge {
  number: string;
  title: string;
  description: string;
}

export interface SmallBusinessCapability {
  number: string;
  title: string;
  href: string;
  description: string;
  outcomes: string[];
}

export interface SmallBusinessPrinciple {
  number: string;
  title: string;
  description: string;
}

export const smallBusinessChallenges: SmallBusinessChallenge[] = [
  {
    number: "01",
    title: "Too many disconnected tools",
    description:
      "Customer records, spreadsheets, accounting, messaging and website enquiries often live in separate places, creating duplicate work and weak visibility.",
  },
  {
    number: "02",
    title: "Limited internal IT capacity",
    description:
      "Smaller teams rarely have dedicated specialists for every technology area, so systems need to be understandable, supportable and appropriately scoped.",
  },
  {
    number: "03",
    title: "Every investment needs a reason",
    description:
      "Technology budgets need to produce operational value or revenue impact rather than becoming expensive infrastructure with no clear business purpose.",
  },
  {
    number: "04",
    title: "Growth exposes weak processes",
    description:
      "Processes that work with ten customers can become fragile at one hundred. Software and automation should remove those limits before they become bottlenecks.",
  },
];

export const smallBusinessCapabilities: SmallBusinessCapability[] = [
  {
    number: "01",
    title: "Business Websites",
    href: "/services/web-development/business-websites/",
    description:
      "Create a credible digital presence that explains the business clearly and gives potential customers an obvious path to enquire.",
    outcomes: [
      "Professional presence",
      "Lead generation",
      "Mobile usability",
      "Search foundations",
    ],
  },
  {
    number: "02",
    title: "E-commerce",
    href: "/services/web-development/ecommerce-websites/",
    description:
      "Sell products and services online through a structured commerce experience connected to payments and operational workflows.",
    outcomes: [
      "Online sales",
      "Product management",
      "Payments",
      "Order workflows",
    ],
  },
  {
    number: "03",
    title: "Custom Business Software",
    href: "/services/software-development/custom-software/",
    description:
      "Replace spreadsheets and repetitive workarounds when the business reaches the point where generic tools no longer fit.",
    outcomes: [
      "Structured workflows",
      "Centralised records",
      "Permissions",
      "Operational visibility",
    ],
  },
  {
    number: "04",
    title: "SEO & Digital Marketing",
    href: "/services/digital-marketing/",
    description:
      "Improve discoverability and customer acquisition through search, advertising, content and measurable digital marketing activity.",
    outcomes: [
      "Search visibility",
      "Lead acquisition",
      "Campaign tracking",
      "Customer growth",
    ],
  },
  {
    number: "05",
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Remove repetitive administrative steps where predictable processes can be handled safely by connected systems.",
    outcomes: [
      "Less manual work",
      "Faster follow-up",
      "Consistent processes",
      "Connected tools",
    ],
  },
  {
    number: "06",
    title: "IT Consultancy",
    href: "/services/it-consultancy/",
    description:
      "Make technology decisions with a clearer understanding of cost, risk, scalability and what the business actually needs.",
    outcomes: [
      "Technology planning",
      "Vendor decisions",
      "Architecture guidance",
      "Reduced waste",
    ],
  },
];

export const smallBusinessPrinciples: SmallBusinessPrinciple[] = [
  {
    number: "01",
    title: "Do not over-engineer",
    description:
      "A five-person business rarely needs the same infrastructure as a multinational. Architecture should fit the current requirement while leaving sensible room to grow.",
  },
  {
    number: "02",
    title: "Keep recurring costs visible",
    description:
      "Hosting, software subscriptions, third-party services and maintenance should be understood before the solution becomes operationally dependent on them.",
  },
  {
    number: "03",
    title: "Automate stable work first",
    description:
      "The best early automation opportunities are usually recurring tasks with clear inputs, predictable rules and a measurable cost in staff time.",
  },
  {
    number: "04",
    title: "Own the important assets",
    description:
      "Businesses should retain appropriate control of domains, accounts, data and other digital assets instead of being permanently dependent on a vendor.",
  },
];
