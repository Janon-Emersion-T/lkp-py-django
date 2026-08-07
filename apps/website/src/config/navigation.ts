export interface HeaderLink {
  label: string;
  href: string;
  description?: string;
}

export interface HeaderNavigationGroup {
  label: string;
  href: string;
  layout?: "single" | "two-column" | "mega";
  children?: HeaderLink[];
}

export const aboutNavigation: HeaderLink[] = [
  {
    label: "About Us",
    href: "/about",
  },
  {
    label: "Our Story",
    href: "/about/our-story",
  },
  {
    label: "Mission & Vision",
    href: "/about/mission-vision",
  },
  {
    label: "Why Choose LKP",
    href: "/about/why-choose-lkp",
  },
  {
    label: "Our Process",
    href: "/about/our-process",
  },
  {
    label: "Our Team",
    href: "/about/our-team",
  },
  {
    label: "Careers",
    href: "/about/careers",
  },
];

export const serviceNavigation: HeaderLink[] = [
  {
    label: "Web Development",
    href: "/services/web-development",
    description: "Websites, commerce and custom web applications.",
  },
  {
    label: "Software Development",
    href: "/services/software-development",
    description: "ERP, CRM, POS and operational software.",
  },
  {
    label: "Mobile App Development",
    href: "/services/mobile-app-development",
    description: "Android, iOS and cross-platform applications.",
  },
  {
    label: "AI Solutions",
    href: "/services/ai-solutions",
    description: "AI assistants, automation and integration.",
  },
  {
    label: "Digital Marketing",
    href: "/services/digital-marketing",
    description: "SEO, advertising and digital acquisition.",
  },
  {
    label: "Branding & Design",
    href: "/services/branding-design",
    description: "Identity, UI/UX and visual communication.",
  },
  {
    label: "Cloud & Hosting",
    href: "/services/cloud-hosting",
    description: "Hosting, domains, email and infrastructure.",
  },
  {
    label: "IT Consultancy",
    href: "/services/it-consultancy",
    description: "Technology planning and transformation.",
  },
  {
    label: "Cybersecurity",
    href: "/services/cybersecurity",
    description: "Audit, protection, backup and hardening.",
  },
  {
    label: "API & Integration",
    href: "/services/api-integration",
    description: "Payments, messaging, CRM and ERP integration.",
  },
  {
    label: "Business Automation",
    href: "/services/business-automation",
    description: "Workflow and operational automation.",
  },
  {
    label: "Data & Analytics",
    href: "/services/data-analytics",
    description: "Dashboards, intelligence and KPI reporting.",
  },
  {
    label: "Maintenance & Support",
    href: "/services/maintenance-support",
    description: "Ongoing maintenance and technical support.",
  },
];

export const caseStudiesNavigation: HeaderLink[] = [
  {
    label: "All Case Studies",
    href: "/case-studies",
  },
  {
    label: "Web Development",
    href: "/case-studies/web-development",
  },
  {
    label: "Software Development",
    href: "/case-studies/software-development",
  },
  {
    label: "SEO",
    href: "/case-studies/seo",
  },
  {
    label: "Digital Marketing",
    href: "/case-studies/digital-marketing",
  },
  {
    label: "Mobile Apps",
    href: "/case-studies/mobile-apps",
  },
];

export const industryNavigation: HeaderLink[] = [
  {
    label: "Small Business",
    href: "/industries/small-business",
  },
  {
    label: "Enterprise",
    href: "/industries/enterprise",
  },
  {
    label: "Healthcare",
    href: "/industries/healthcare",
  },
  {
    label: "Education",
    href: "/industries/education",
  },
  {
    label: "Hospitality",
    href: "/industries/hospitality",
  },
  {
    label: "Retail & E-commerce",
    href: "/industries/retail-ecommerce",
  },
  {
    label: "Manufacturing",
    href: "/industries/manufacturing",
  },
  {
    label: "Construction",
    href: "/industries/construction",
  },
  {
    label: "Logistics",
    href: "/industries/logistics",
  },
  {
    label: "Finance",
    href: "/industries/finance",
  },
  {
    label: "Government",
    href: "/industries/government",
  },
  {
    label: "Non-profit",
    href: "/industries/non-profit",
  },
];

export const insightNavigation: HeaderLink[] = [
  {
    label: "All Insights",
    href: "/insights",
  },
  {
    label: "Blog",
    href: "/insights/blog",
  },
  {
    label: "News",
    href: "/insights/news",
  },
  {
    label: "SEO Tips",
    href: "/insights/seo-tips",
  },
  {
    label: "AI",
    href: "/insights/ai",
  },
  {
    label: "Web Development",
    href: "/insights/web-development",
  },
  {
    label: "Software Development",
    href: "/insights/software-development",
  },
  {
    label: "Digital Marketing",
    href: "/insights/digital-marketing",
  },
  {
    label: "Business Growth",
    href: "/insights/business-growth",
  },
  {
    label: "Tutorials",
    href: "/insights/tutorials",
  },
];

export const headerNavigation: HeaderNavigationGroup[] = [
  {
    label: "Home",
    href: "/",
  },
  {
    label: "About Us",
    href: "/about",
    layout: "single",
    children: aboutNavigation,
  },
  {
    label: "Services",
    href: "/services",
    layout: "mega",
    children: serviceNavigation,
  },
  {
    label: "Case Studies",
    href: "/case-studies",
    layout: "single",
    children: caseStudiesNavigation,
  },
  {
    label: "Industries",
    href: "/industries",
    layout: "two-column",
    children: industryNavigation,
  },
  {
    label: "Insights",
    href: "/insights",
    layout: "two-column",
    children: insightNavigation,
  },
  {
    label: "Contact Us",
    href: "/contact",
  },
];
