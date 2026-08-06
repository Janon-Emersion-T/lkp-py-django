export interface FooterLinkedPage {
  title: string;
  path: string;
  eyebrow: string;
  description: string;
  parentPath?: string;
  noindex?: boolean;
}

export const footerLinkedPages: FooterLinkedPage[] = [
  {
    title: "Web Development",
    path: "services/web-development",
    eyebrow: "Services",
    description:
      "Professional websites and web platforms designed around business goals, usability, performance and long-term maintainability.",
    parentPath: "services",
  },
  {
    title: "Software Development",
    path: "services/software-development",
    eyebrow: "Services",
    description:
      "Custom software systems built to improve business operations, control information and support measurable growth.",
    parentPath: "services",
  },
  {
    title: "Mobile App Development",
    path: "services/mobile-app-development",
    eyebrow: "Services",
    description:
      "Reliable mobile applications for organisations that need practical, secure and maintainable digital products.",
    parentPath: "services",
  },
  {
    title: "AI Solutions",
    path: "services/ai-solutions",
    eyebrow: "Services",
    description:
      "Applied AI solutions focused on automation, customer service, internal productivity and better business decisions.",
    parentPath: "services",
  },
  {
    title: "Digital Marketing",
    path: "services/digital-marketing",
    eyebrow: "Services",
    description:
      "Search, advertising, content and digital growth services connected to clear commercial objectives.",
    parentPath: "services",
  },
  {
    title: "Branding & Design",
    path: "services/branding-design",
    eyebrow: "Services",
    description:
      "Corporate identity, interface and visual design services that communicate clearly and support business credibility.",
    parentPath: "services",
  },
  {
    title: "Cloud & Hosting",
    path: "services/cloud-hosting",
    eyebrow: "Services",
    description:
      "Hosting, domain, email, SSL and cloud infrastructure services managed with reliability and accountability.",
    parentPath: "services",
  },
  {
    title: "IT Consultancy",
    path: "services/it-consultancy",
    eyebrow: "Services",
    description:
      "Practical technology advice for organisations planning systems, integrations and digital transformation.",
    parentPath: "services",
  },
  {
    title: "Cybersecurity",
    path: "services/cybersecurity",
    eyebrow: "Services",
    description:
      "Security assessment, protection, backup and hardening services for websites and business systems.",
    parentPath: "services",
  },
  {
    title: "API & Integration",
    path: "services/api-integration",
    eyebrow: "Services",
    description:
      "Reliable integrations connecting payment, messaging, CRM, ERP and other business platforms.",
    parentPath: "services",
  },
  {
    title: "Business Automation",
    path: "services/business-automation",
    eyebrow: "Services",
    description:
      "Workflow and process automation designed to reduce repetitive work and improve operational control.",
    parentPath: "services",
  },
  {
    title: "Data & Analytics",
    path: "services/data-analytics",
    eyebrow: "Services",
    description:
      "Dashboards, reports and business intelligence systems that turn operational data into practical information.",
    parentPath: "services",
  },
  {
    title: "Maintenance & Support",
    path: "services/maintenance-support",
    eyebrow: "Services",
    description:
      "Dependable technical maintenance, optimisation and support for websites, software and digital infrastructure.",
    parentPath: "services",
  },

  {
    title: "About Us",
    path: "about",
    eyebrow: "Company",
    description:
      "Learn about LKProfessionals, our history, principles, working methods and commitment to reliable technology delivery.",
  },
  {
    title: "Industries",
    path: "industries",
    eyebrow: "Industry Experience",
    description:
      "Technology and digital services adapted to the operational requirements of different industries.",
  },
  {
    title: "Case Studies",
    path: "case-studies",
    eyebrow: "Our Work",
    description:
      "Selected examples of business challenges, technical decisions and results delivered by LKProfessionals.",
  },
  {
    title: "Portfolio",
    path: "portfolio",
    eyebrow: "Portfolio",
    description:
      "Explore selected website, software, mobile, branding and digital marketing work.",
  },
  {
    title: "Insights",
    path: "insights",
    eyebrow: "Knowledge",
    description:
      "Practical articles and updates covering technology, software, websites, digital growth and business operations.",
  },
  {
    title: "Pricing",
    path: "pricing",
    eyebrow: "Pricing",
    description:
      "Review structured service options or request a quotation based on your specific requirements.",
  },
  {
    title: "Testimonials",
    path: "testimonials",
    eyebrow: "Client Experience",
    description:
      "Feedback from organisations and clients who have worked with LKProfessionals.",
  },
  {
    title: "Careers",
    path: "about/careers",
    eyebrow: "Company",
    description:
      "Explore current opportunities to work and grow with LKProfessionals.",
    parentPath: "about",
  },
  {
    title: "Contact Us",
    path: "contact",
    eyebrow: "Contact",
    description:
      "Contact LKProfessionals for sales, general enquiries, project discussions and support.",
  },
  {
    title: "Get a Quote",
    path: "get-a-quote",
    eyebrow: "Start a Project",
    description:
      "Tell us about your requirements and receive a practical quotation from LKProfessionals.",
  },

  {
    title: "Terms & Conditions",
    path: "legal/terms-conditions",
    eyebrow: "Legal",
    description:
      "Terms governing the use of LKProfessionals websites, services and commercial engagements.",
    parentPath: "legal",
  },
  {
    title: "Privacy Policy",
    path: "legal/privacy-policy",
    eyebrow: "Legal",
    description:
      "Information about how LKProfessionals collects, uses and protects personal information.",
    parentPath: "legal",
  },
  {
    title: "Cookie Policy",
    path: "legal/cookie-policy",
    eyebrow: "Legal",
    description:
      "Information about cookies and similar technologies used by the LKProfessionals website.",
    parentPath: "legal",
  },
  {
    title: "Refund Policy",
    path: "legal/refund-policy",
    eyebrow: "Legal",
    description:
      "The LKProfessionals policy governing cancellations, refunds and completed service work.",
    parentPath: "legal",
  },
];

export const footerLinkedPageByPath = new Map(
  footerLinkedPages.map((page) => [page.path, page]),
);
