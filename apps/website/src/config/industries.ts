export interface Industry {
  number: string;
  title: string;
  href: string;
  description: string;
  areas: string[];
}

export interface IndustryCapability {
  number: string;
  title: string;
  description: string;
}

export interface IndustryApproach {
  number: string;
  title: string;
  description: string;
}

export interface IndustryServicePath {
  title: string;
  href: string;
  description: string;
}

export const industries: Industry[] = [
  {
    number: "01",
    title: "Small Business",
    href: "/industries/small-business/",
    description:
      "Practical websites, business systems, automation and digital growth infrastructure for organisations building stronger day-to-day operations.",
    areas: ["Websites", "CRM", "Automation", "Digital growth"],
  },
  {
    number: "02",
    title: "Enterprise",
    href: "/industries/enterprise/",
    description:
      "Structured software, integrations, data systems and technology services for larger organisations with complex workflows and responsibilities.",
    areas: ["Enterprise software", "Integration", "Data", "Infrastructure"],
  },
  {
    number: "03",
    title: "Healthcare",
    href: "/industries/healthcare/",
    description:
      "Digital systems for healthcare organisations requiring clearer administration, scheduling, records and operational workflows.",
    areas: ["Administration", "Scheduling", "Portals", "Reporting"],
  },
  {
    number: "04",
    title: "Education",
    href: "/industries/education/",
    description:
      "Technology for schools, institutes and education providers managing students, learning operations, administration and communication.",
    areas: ["Student systems", "Portals", "Administration", "Communication"],
  },
  {
    number: "05",
    title: "Hospitality",
    href: "/industries/hospitality/",
    description:
      "Web, booking, guest and operational technology for hotels, villas, accommodation providers and hospitality businesses.",
    areas: ["Booking", "Guest journeys", "Websites", "Operations"],
  },
  {
    number: "06",
    title: "Retail & E-commerce",
    href: "/industries/retail-ecommerce/",
    description:
      "Commerce, inventory, customer and digital-growth systems connecting the storefront with the wider retail operation.",
    areas: ["E-commerce", "POS", "Inventory", "CRM"],
  },
  {
    number: "07",
    title: "Manufacturing",
    href: "/industries/manufacturing/",
    description:
      "Operational software and data workflows supporting production, inventory, procurement and management visibility.",
    areas: ["Production", "Inventory", "ERP", "Analytics"],
  },
  {
    number: "08",
    title: "Construction",
    href: "/industries/construction/",
    description:
      "Digital systems for projects, quotations, documentation, teams, procurement and operational oversight across construction businesses.",
    areas: ["Projects", "Quotations", "Documents", "Reporting"],
  },
  {
    number: "09",
    title: "Logistics",
    href: "/industries/logistics/",
    description:
      "Software and integrations for movement, dispatch, tracking, records and operational coordination across logistics workflows.",
    areas: ["Dispatch", "Tracking", "Integration", "Operations"],
  },
  {
    number: "10",
    title: "Finance",
    href: "/industries/finance/",
    description:
      "Controlled financial and administrative workflows designed around access, approvals, traceability, integration and reporting.",
    areas: ["Approvals", "ERP", "Integration", "Analytics"],
  },
  {
    number: "11",
    title: "Government",
    href: "/industries/government/",
    description:
      "Public-service portals and administrative systems connecting accessible digital services with structured internal workflows.",
    areas: ["Public portals", "Administration", "Workflows", "Reporting"],
  },
  {
    number: "12",
    title: "Non-profit",
    href: "/industries/non-profit/",
    description:
      "Digital infrastructure for supporter relationships, programmes, volunteers, campaigns and mission-focused administration.",
    areas: ["Supporters", "Programmes", "Donations", "Reporting"],
  },
];

export const industryCapabilities: IndustryCapability[] = [
  {
    number: "01",
    title: "Customer & public experiences",
    description:
      "Websites, portals, applications and digital journeys shaped around the people who actually need to use them.",
  },
  {
    number: "02",
    title: "Internal operations",
    description:
      "Custom software, ERP, CRM and workflow systems designed around how information and responsibility move through the organisation.",
  },
  {
    number: "03",
    title: "System connectivity",
    description:
      "APIs and integrations that reduce repeated entry and connect suitable platforms without hiding operational ownership.",
  },
  {
    number: "04",
    title: "Automation",
    description:
      "Defined repetitive processes can be automated while keeping exceptions and important decisions visible to responsible people.",
  },
  {
    number: "05",
    title: "Data & reporting",
    description:
      "Operational information can be transformed into practical dashboards and reports when the underlying data is sufficiently reliable.",
  },
  {
    number: "06",
    title: "Infrastructure & continuity",
    description:
      "Hosting, cloud, cybersecurity and maintenance considerations support the systems that organisations depend on after launch.",
  },
];

export const industryApproach: IndustryApproach[] = [
  {
    number: "01",
    title: "Understand the operation before prescribing technology",
    description:
      "We begin with users, responsibilities, existing systems, information flows and the business problem rather than forcing every organisation into the same product.",
  },
  {
    number: "02",
    title: "Separate essential workflows from optional complexity",
    description:
      "A focused system solving the right operational problem is more valuable than a large feature list that teams do not need.",
  },
  {
    number: "03",
    title: "Design around real responsibilities",
    description:
      "Roles, permissions, approvals and visibility should reflect how the organisation is actually governed and operated.",
  },
  {
    number: "04",
    title: "Connect where integration creates value",
    description:
      "Existing platforms do not automatically need replacement. Where suitable interfaces exist, integration can preserve useful systems while reducing duplication.",
  },
  {
    number: "05",
    title: "Plan beyond launch",
    description:
      "Maintainability, documentation, security, infrastructure and future change are considered as part of the system rather than postponed until something breaks.",
  },
];

export const industryServicePaths: IndustryServicePath[] = [
  {
    title: "Web Development",
    href: "/services/web-development/",
    description:
      "Corporate websites, business websites, e-commerce, portals and custom web applications.",
  },
  {
    title: "Software Development",
    href: "/services/software-development/",
    description:
      "Custom software, ERP, CRM and operational systems designed around business workflows.",
  },
  {
    title: "Mobile App Development",
    href: "/services/mobile-app-development/",
    description:
      "Mobile applications for customers, staff, field teams and organisation-specific workflows.",
  },
  {
    title: "AI Solutions",
    href: "/services/ai-solutions/",
    description:
      "Practical AI capabilities applied where they can support defined business and information workflows.",
  },
  {
    title: "API Integration",
    href: "/services/api-integration/",
    description:
      "Connect supported platforms, services and internal systems through controlled integrations.",
  },
  {
    title: "Business Automation",
    href: "/services/business-automation/",
    description:
      "Reduce repetitive administration through defined workflow and process automation.",
  },
  {
    title: "Data & Analytics",
    href: "/services/data-analytics/",
    description:
      "Reporting, dashboards and operational insight built around available organisational data.",
  },
  {
    title: "Cybersecurity",
    href: "/services/cybersecurity/",
    description:
      "Security reviews, hardening, access considerations and risk-reduction measures for digital systems.",
  },
  {
    title: "Cloud & Hosting",
    href: "/services/cloud-hosting/",
    description:
      "Infrastructure, hosting, monitoring and operational foundations for business applications.",
  },
  {
    title: "Maintenance & Support",
    href: "/services/maintenance-support/",
    description:
      "Ongoing technical support, maintenance and improvement after systems enter production.",
  },
];
