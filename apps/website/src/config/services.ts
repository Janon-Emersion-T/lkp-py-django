export interface ServiceFamily {
  number: string;
  title: string;
  href: string;
  description: string;
  focus: string[];
  group: "Build" | "Grow" | "Operate" | "Advise";
}

export interface ServiceGroup {
  name: string;
  statement: string;
  description: string;
}

export interface ServicePrinciple {
  number: string;
  title: string;
  description: string;
}

export const serviceFamilies: ServiceFamily[] = [
  {
    number: "01",
    title: "Web Development",
    href: "/services/web-development/",
    description:
      "Business websites, ecommerce, booking platforms, landing pages and custom web applications built around business purpose.",
    focus: ["Websites", "E-commerce", "Web applications", "Maintenance"],
    group: "Build",
  },
  {
    number: "02",
    title: "Software Development",
    href: "/services/software-development/",
    description:
      "Custom operational software including ERP, CRM, POS, inventory, HRM, accounting and SaaS platforms.",
    focus: ["Custom software", "ERP & CRM", "Business systems", "SaaS"],
    group: "Build",
  },
  {
    number: "03",
    title: "Mobile App Development",
    href: "/services/mobile-app-development/",
    description:
      "Android, iOS and cross-platform applications connected to the systems and workflows behind the mobile experience.",
    focus: ["Android", "iOS", "Cross-platform", "Business apps"],
    group: "Build",
  },
  {
    number: "04",
    title: "AI Solutions",
    href: "/services/ai-solutions/",
    description:
      "Practical AI capabilities for assistants, chatbots, intelligent workflows, integrations and purpose-built applications.",
    focus: ["AI assistants", "Chatbots", "AI automation", "AI integration"],
    group: "Build",
  },
  {
    number: "05",
    title: "Digital Marketing",
    href: "/services/digital-marketing/",
    description:
      "Search, paid acquisition, content, social media, email and marketing automation focused on measurable demand generation.",
    focus: ["SEO", "Google Ads", "Content", "Marketing automation"],
    group: "Grow",
  },
  {
    number: "06",
    title: "Branding & Design",
    href: "/services/branding-design/",
    description:
      "Visual identity, UI/UX and communication design that keeps the business recognisable across customer touchpoints.",
    focus: ["Brand identity", "Logo design", "UI/UX", "Graphic design"],
    group: "Grow",
  },
  {
    number: "07",
    title: "Cloud & Hosting",
    href: "/services/cloud-hosting/",
    description:
      "Hosting, VPS infrastructure, domains, business email and SSL services supporting reliable digital operations.",
    focus: ["Web hosting", "VPS", "Domains", "Business email"],
    group: "Operate",
  },
  {
    number: "08",
    title: "IT Consultancy",
    href: "/services/it-consultancy/",
    description:
      "Technology guidance for transformation, architecture, integrations and projects before expensive decisions become permanent.",
    focus: [
      "Technology strategy",
      "Transformation",
      "Integration planning",
      "Project consulting",
    ],
    group: "Advise",
  },
  {
    number: "09",
    title: "Cybersecurity",
    href: "/services/cybersecurity/",
    description:
      "Security review, hardening, website protection and recovery planning focused on practical risk reduction.",
    focus: ["Security audits", "Hardening", "Website security", "Recovery"],
    group: "Operate",
  },
  {
    number: "10",
    title: "API & Integration",
    href: "/services/api-integration/",
    description:
      "Reliable connections between payments, messaging, CRM, ERP and the systems involved in business workflows.",
    focus: ["APIs", "Payments", "Messaging", "System integration"],
    group: "Build",
  },
  {
    number: "11",
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Reduce repetitive operational work by connecting processes, systems, triggers and business rules.",
    focus: [
      "Workflow automation",
      "Process automation",
      "Notifications",
      "System workflows",
    ],
    group: "Operate",
  },
  {
    number: "12",
    title: "Data & Analytics",
    href: "/services/data-analytics/",
    description:
      "Turn operational data into structured reporting, dashboards and decision-support information.",
    focus: ["Dashboards", "Reporting", "Analytics", "Data visibility"],
    group: "Advise",
  },
  {
    number: "13",
    title: "Maintenance & Support",
    href: "/services/maintenance-support/",
    description:
      "Ongoing technical maintenance, monitoring, support and improvement for systems already in production.",
    focus: ["Maintenance", "Monitoring", "Technical support", "Improvements"],
    group: "Operate",
  },
];

export const serviceGroups: ServiceGroup[] = [
  {
    name: "Build",
    statement: "Create the digital systems.",
    description:
      "Websites, software, mobile products, AI capabilities and integrations built around actual business responsibilities.",
  },
  {
    name: "Grow",
    statement: "Strengthen how the market sees you.",
    description:
      "Brand, search, advertising and communication that help the right audiences discover and understand the business.",
  },
  {
    name: "Operate",
    statement: "Keep technology dependable.",
    description:
      "Infrastructure, security, automation and maintenance that support systems after they become part of daily operations.",
  },
  {
    name: "Advise",
    statement: "Make better technology decisions.",
    description:
      "Consulting and analytics that improve visibility, planning and confidence before significant commitments are made.",
  },
];

export const servicePrinciples: ServicePrinciple[] = [
  {
    number: "01",
    title: "Start with the business requirement",
    description:
      "Technology should be selected after the problem, users, workflow and constraints are understood.",
  },
  {
    number: "02",
    title: "Keep ownership clear",
    description:
      "Domains, software, infrastructure, data and accounts should not disappear into unexplained vendor dependencies.",
  },
  {
    number: "03",
    title: "Build systems that can be maintained",
    description:
      "Modularity, documentation and controlled architecture matter long after the first release.",
  },
  {
    number: "04",
    title: "Measure the operational outcome",
    description:
      "The real question is not whether technology was delivered, but whether it improves how the business operates or grows.",
  },
];
