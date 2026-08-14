export interface PortfolioCategory {
  slug: string;
  label: string;
  serviceSlug: string;
  title: string;
  description: string;
  metaTitle: string;
  metaDescription: string;
}

export const portfolioCategories: Record<
  string,
  PortfolioCategory
> = {
  websites: {
    slug: "websites",
    label: "Websites",
    serviceSlug: "web-development",
    title: "Web work built for real businesses.",
    description:
      "Selected websites and web platforms delivered around commercial, operational and customer requirements.",
    metaTitle: "Website Portfolio",
    metaDescription:
      "Selected website and web development work by LKProfessionals.",
  },

  software: {
    slug: "software",
    label: "Software",
    serviceSlug: "software-development",
    title: "Software shaped around operations.",
    description:
      "Custom systems, business applications and operational software designed around the way organisations actually work.",
    metaTitle: "Software Portfolio",
    metaDescription:
      "Selected software development projects by LKProfessionals.",
  },

  "mobile-apps": {
    slug: "mobile-apps",
    label: "Mobile Apps",
    serviceSlug: "mobile-app-development",
    title: "Mobile products with a job to do.",
    description:
      "Mobile applications created for business workflows, services and customer experiences.",
    metaTitle: "Mobile App Portfolio",
    metaDescription:
      "Selected mobile application projects by LKProfessionals.",
  },

  branding: {
    slug: "branding",
    label: "Branding",
    serviceSlug: "branding-design",
    title: "Identity systems with practical purpose.",
    description:
      "Selected branding, visual identity and digital design work developed around clear business positioning.",
    metaTitle: "Branding Portfolio",
    metaDescription:
      "Selected branding and design work by LKProfessionals.",
  },

  marketing: {
    slug: "marketing",
    label: "Marketing",
    serviceSlug: "digital-marketing",
    title: "Digital work measured beyond impressions.",
    description:
      "Selected SEO, paid media and digital marketing engagements focused on measurable commercial outcomes.",
    metaTitle: "Digital Marketing Portfolio",
    metaDescription:
      "Selected digital marketing work by LKProfessionals.",
  },
};
