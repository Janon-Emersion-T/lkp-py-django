export interface InsightCategoryConfig {
  slug: string;
  label: string;
  title: string;
  description: string;
  note: string;
  metaTitle: string;
  metaDescription: string;
}

export const insightCategoryConfigs: Record<
  string,
  InsightCategoryConfig
> = {
  news: {
    slug: "news",
    label: "News",
    title: "Technology and company news.",
    description:
      "Relevant developments from LKProfessionals and the wider technology landscape, presented with the context businesses need.",
    note:
      "Updates worth understanding, without turning every software release into breaking news.",
    metaTitle: "Technology News",
    metaDescription:
      "Technology and company news from LKProfessionals, covering relevant digital, software and business technology developments.",
  },

  "seo-tips": {
    slug: "seo-tips",
    label: "SEO Tips",
    title: "Search guidance that stays practical.",
    description:
      "Practical guidance on technical SEO, content, indexing, search visibility and the fundamentals behind sustainable organic growth.",
    note:
      "Focused on useful improvements rather than shortcuts, tricks or keyword theatre.",
    metaTitle: "SEO Tips & Guidance",
    metaDescription:
      "Practical SEO tips from LKProfessionals covering technical SEO, content, indexing and sustainable search visibility.",
  },

  ai: {
    slug: "ai",
    label: "AI",
    title: "AI without the theatre.",
    description:
      "Practical thinking on artificial intelligence, automation, assistants and where these technologies genuinely improve business operations.",
    note:
      "Useful applications first. Hype can wait outside.",
    metaTitle: "AI Insights & Automation",
    metaDescription:
      "Practical AI insights from LKProfessionals covering automation, assistants, integrations and real business applications.",
  },

  "web-development": {
    slug: "web-development",
    label: "Web Development",
    title: "Building for the web properly.",
    description:
      "Planning, engineering, maintaining and improving websites and web applications around genuine business requirements.",
    note:
      "Architecture, performance, usability and maintainability matter long after launch day.",
    metaTitle: "Web Development Insights",
    metaDescription:
      "Web development insights from LKProfessionals covering websites, web applications, architecture, performance and implementation.",
  },

  "software-development": {
    slug: "software-development",
    label: "Software Development",
    title: "Software built around operations.",
    description:
      "Engineering decisions, architecture, business systems and lessons from building software that organisations actually depend on.",
    note:
      "The objective is reliable software that fits the operation—not complexity for its own sake.",
    metaTitle: "Software Development Insights",
    metaDescription:
      "Software development insights from LKProfessionals covering architecture, business systems, engineering and implementation.",
  },

  "digital-marketing": {
    slug: "digital-marketing",
    label: "Digital Marketing",
    title: "Marketing measured by outcomes.",
    description:
      "Search, paid media, content and digital acquisition considered through measurable business results rather than vanity metrics.",
    note:
      "Reach is useful. Revenue, enquiries and qualified demand are more useful.",
    metaTitle: "Digital Marketing Insights",
    metaDescription:
      "Digital marketing insights from LKProfessionals covering SEO, advertising, content, acquisition and measurable growth.",
  },

  "business-growth": {
    slug: "business-growth",
    label: "Business Growth",
    title: "Technology as part of growth.",
    description:
      "How websites, software, automation, data and digital strategy fit into the wider operation and growth of an organisation.",
    note:
      "Technology works best when it supports a clear commercial or operational objective.",
    metaTitle: "Business Growth & Technology",
    metaDescription:
      "Business growth insights from LKProfessionals covering technology, digital strategy, systems and operational improvement.",
  },
};

export const validInsightCategorySlugs =
  Object.keys(insightCategoryConfigs);
