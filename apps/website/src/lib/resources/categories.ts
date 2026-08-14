import type {
  ResourceType,
} from "./types";

export interface ResourceCategoryConfig {
  slug: string;
  resourceType: ResourceType;
  label: string;
  title: string;
  description: string;
  metaTitle: string;
  metaDescription: string;
}

export const resourceCategories: Record<
  string,
  ResourceCategoryConfig
> = {
  downloads: {
    slug: "downloads",
    resourceType: "download",
    label: "Downloads",
    title: "Useful files without the clutter.",
    description:
      "Practical downloadable resources prepared for businesses, teams and technology projects.",
    metaTitle: "Downloads",
    metaDescription:
      "Download practical business and technology resources from LKProfessionals.",
  },

  guides: {
    slug: "guides",
    resourceType: "guide",
    label: "Guides",
    title: "Guidance designed to be used.",
    description:
      "Detailed practical guides covering technology, websites, software, digital operations and business decisions.",
    metaTitle: "Business & Technology Guides",
    metaDescription:
      "Practical business and technology guides from LKProfessionals.",
  },

  checklists: {
    slug: "checklists",
    resourceType: "checklist",
    label: "Checklists",
    title: "A clearer way to check the details.",
    description:
      "Structured checklists for planning, reviewing and delivering digital and technology work.",
    metaTitle: "Technology Checklists",
    metaDescription:
      "Practical website, software and digital project checklists from LKProfessionals.",
  },

  templates: {
    slug: "templates",
    resourceType: "template",
    label: "Templates",
    title: "Useful starting points.",
    description:
      "Reusable templates designed to reduce repetitive work and make common business processes more consistent.",
    metaTitle: "Business & Technology Templates",
    metaDescription:
      "Reusable business and technology templates from LKProfessionals.",
  },
};
