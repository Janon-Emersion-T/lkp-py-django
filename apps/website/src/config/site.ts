import type {
  NavigationItem,
  ProcessStep,
  ProofPoint,
  ServiceSummary,
} from "../types/landing";

export const site = {
  name: "LKProfessionals",
  shortName: "LKP",
  legalName: "LKProfessionals (Pvt) Ltd",
  url: "https://lkprofessionals.com",
  description:
    "LKProfessionals designs and develops dependable websites, business software, digital platforms and search-led growth systems.",
  email: "info@lkprofessionals.com",
  location: "Jaffna, Sri Lanka",
  foundingYear: 2013,
  tagline: "Empowering Businesses Through Reliable IT Solutions.",
} as const;

export const primaryNavigation: NavigationItem[] = [
  {
    label: "Services",
    href: "/services",
  },
  {
    label: "Industries",
    href: "/industries",
  },
  {
    label: "Work",
    href: "/case-studies",
  },
  {
    label: "Insights",
    href: "/insights",
  },
  {
    label: "About",
    href: "/about",
  },
];

export const footerNavigation = {
  company: [
    {
      label: "About us",
      href: "/about",
    },
    {
      label: "Case studies",
      href: "/case-studies",
    },
    {
      label: "Careers",
      href: "/careers",
    },
    {
      label: "Contact",
      href: "/contact",
    },
  ],
  services: [
    {
      label: "Web development",
      href: "/services/web-development",
    },
    {
      label: "Custom software",
      href: "/services/custom-software-development",
    },
    {
      label: "E-commerce",
      href: "/services/ecommerce-development",
    },
    {
      label: "SEO",
      href: "/services/search-engine-optimisation",
    },
  ],
  resources: [
    {
      label: "Insights",
      href: "/insights",
    },
    {
      label: "Request a quote",
      href: "/request-quote",
    },
    {
      label: "Privacy",
      href: "/privacy-policy",
    },
    {
      label: "Terms",
      href: "/terms-and-conditions",
    },
  ],
} satisfies Record<string, NavigationItem[]>;

export const services: ServiceSummary[] = [
  {
    number: "01",
    title: "Web platforms",
    description:
      "Fast, maintainable websites and web applications built around business goals, search visibility and measurable conversion.",
    href: "/services/web-development",
    capabilities: [
      "Business websites",
      "Landing pages",
      "E-commerce",
      "Web applications",
    ],
  },
  {
    number: "02",
    title: "Business software",
    description:
      "Purpose-built operational systems that replace fragmented spreadsheets, manual processes and disconnected tools.",
    href: "/services/custom-software-development",
    capabilities: [
      "ERP and CRM",
      "Booking systems",
      "Inventory software",
      "Internal portals",
    ],
  },
  {
    number: "03",
    title: "Search and growth",
    description:
      "Practical SEO and digital acquisition programmes grounded in technical quality, useful content and commercial intent.",
    href: "/services/search-engine-optimisation",
    capabilities: [
      "Technical SEO",
      "Local SEO",
      "Content strategy",
      "Google Ads",
    ],
  },
  {
    number: "04",
    title: "Technology partnership",
    description:
      "Ongoing technical support for organisations that need a dependable team without building every capability in-house.",
    href: "/services/it-consulting",
    capabilities: [
      "Technical consulting",
      "Maintenance",
      "Hosting",
      "Digital operations",
    ],
  },
];

export const processSteps: ProcessStep[] = [
  {
    number: "01",
    title: "Understand the operation",
    description:
      "We begin with the business model, users, constraints and commercial objective—not a predetermined template.",
  },
  {
    number: "02",
    title: "Define the right system",
    description:
      "Scope, information architecture, technical approach and delivery priorities are agreed before production begins.",
  },
  {
    number: "03",
    title: "Build with accountability",
    description:
      "Work is delivered through visible milestones, practical reviews and direct communication with the people responsible.",
  },
  {
    number: "04",
    title: "Improve after launch",
    description:
      "Performance, usability, search visibility and operational value are monitored and strengthened over time.",
  },
];

export const proofPoints: ProofPoint[] = [
  {
    value: "2013",
    label: "Established",
    note: "More than a decade of practical delivery experience.",
  },
  {
    value: "Full-stack",
    label: "Capability",
    note: "Strategy, design, development, infrastructure and growth.",
  },
  {
    value: "Direct",
    label: "Accountability",
    note: "Clear communication with the team doing the work.",
  },
  {
    value: "Global",
    label: "Delivery",
    note: "Built in Sri Lanka for organisations operating worldwide.",
  },
];
