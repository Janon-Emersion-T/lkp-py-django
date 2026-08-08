export interface WebDevelopmentService {
  number: string;
  title: string;
  href: string;
  description: string;
  capabilities: string[];
}

export interface WebDevelopmentPrinciple {
  number: string;
  title: string;
  description: string;
}

export interface WebDevelopmentStage {
  number: string;
  title: string;
  description: string;
}

export const webDevelopmentServices: WebDevelopmentService[] = [
  {
    number: "01",
    title: "Business Websites",
    href: "/services/web-development/business-websites/",
    description:
      "Professional websites for businesses that need a credible, responsive and commercially useful online presence.",
    capabilities: [
      "Business presentation",
      "Lead generation",
      "Responsive design",
      "Search foundations",
    ],
  },
  {
    number: "02",
    title: "Corporate Websites",
    href: "/services/web-development/corporate-websites/",
    description:
      "Structured corporate websites for organisations that need to communicate scale, capability, governance and multiple areas of operation clearly.",
    capabilities: [
      "Corporate architecture",
      "Service structures",
      "Stakeholder content",
      "Scalable navigation",
    ],
  },
  {
    number: "03",
    title: "E-commerce Websites",
    href: "/services/web-development/ecommerce-websites/",
    description:
      "Online commerce experiences that connect products, customers, payments and operational workflows through a dependable web platform.",
    capabilities: [
      "Product catalogues",
      "Checkout",
      "Payments",
      "Order workflows",
    ],
  },
  {
    number: "04",
    title: "Landing Pages",
    href: "/services/web-development/landing-pages/",
    description:
      "Focused campaign and conversion pages designed around one audience, one offer and a clear next action.",
    capabilities: [
      "Campaign pages",
      "Lead capture",
      "Conversion paths",
      "Advertising support",
    ],
  },
  {
    number: "05",
    title: "Booking Websites",
    href: "/services/web-development/booking-websites/",
    description:
      "Websites that allow customers to discover availability, make bookings and interact with scheduling workflows online.",
    capabilities: [
      "Availability",
      "Bookings",
      "Customer flows",
      "Scheduling integration",
    ],
  },
  {
    number: "06",
    title: "Custom Web Applications",
    href: "/services/web-development/custom-web-applications/",
    description:
      "Browser-based software for workflows that need more than conventional website content and forms.",
    capabilities: [
      "Authenticated systems",
      "Business workflows",
      "Dashboards",
      "API integrations",
    ],
  },
  {
    number: "07",
    title: "Website Redesign",
    href: "/services/web-development/website-redesign/",
    description:
      "Rebuild outdated or underperforming websites while improving structure, usability, technical quality and commercial purpose.",
    capabilities: [
      "UX improvement",
      "Modernisation",
      "Content structure",
      "Performance improvement",
    ],
  },
  {
    number: "08",
    title: "Website Maintenance",
    href: "/services/web-development/website-maintenance/",
    description:
      "Ongoing technical support for websites that need updates, fixes, monitoring and controlled improvement after launch.",
    capabilities: [
      "Updates",
      "Bug fixes",
      "Technical support",
      "Ongoing improvements",
    ],
  },
];

export const webDevelopmentPrinciples: WebDevelopmentPrinciple[] = [
  {
    number: "01",
    title: "Build around the visitor's question",
    description:
      "Navigation, content and page structure should help people understand the business quickly instead of reflecting only the organisation's internal terminology.",
  },
  {
    number: "02",
    title: "Performance is part of design",
    description:
      "A visually sophisticated website that loads poorly or behaves inconsistently creates a weaker user experience.",
  },
  {
    number: "03",
    title: "Search begins with architecture",
    description:
      "SEO is easier when page structure, semantics, internal linking and technical foundations are considered during development rather than added afterwards.",
  },
  {
    number: "04",
    title: "Launch is not the end",
    description:
      "Websites need content updates, technical maintenance, measurement and improvement as the business and web ecosystem change.",
  },
];

export const webDevelopmentStages: WebDevelopmentStage[] = [
  {
    number: "01",
    title: "Discover",
    description:
      "Understand the business, audience, goals, existing assets and role the website needs to perform.",
  },
  {
    number: "02",
    title: "Structure",
    description:
      "Define information architecture, page hierarchy, user journeys and conversion paths.",
  },
  {
    number: "03",
    title: "Design",
    description:
      "Create a responsive visual system that supports clarity, credibility and the established brand.",
  },
  {
    number: "04",
    title: "Develop",
    description:
      "Build the website with maintainable components, semantic markup and appropriate backend integrations.",
  },
  {
    number: "05",
    title: "Validate",
    description:
      "Check responsive behaviour, accessibility, forms, metadata, performance and important user journeys.",
  },
  {
    number: "06",
    title: "Operate",
    description:
      "Launch, measure and maintain the website as content, search behaviour and business requirements evolve.",
  },
];
