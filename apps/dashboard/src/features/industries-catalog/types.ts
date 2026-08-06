export const industryStatuses = [
  "draft",
  "scheduled",
  "published",
  "archived",
] as const;

export type IndustryStatus = (typeof industryStatuses)[number];

export interface IndustryServiceLink {
  id: string;
  service_id: string;
  service_title: string;
  description: string;
  sort_order: number;
  is_featured: boolean;
}

export interface IndustryFaq {
  id: string;
  question: string;
  answer: string;
  sort_order: number;
}

export interface IndustrySeo {
  id: string;
  meta_title: string;
  meta_description: string;
  canonical_url: string;
  robots_index: boolean;
  robots_follow: boolean;
  open_graph_title: string;
  open_graph_description: string;
  open_graph_image_id: string | null;
  twitter_title: string;
  twitter_description: string;
  structured_data: Record<string, unknown>;
}

export interface IndustryRevision {
  id: string;
  revision_number: number;
  snapshot: Record<string, unknown>;
  change_summary: string;
  created_at: string;
}

export interface CatalogIndustry {
  id: string;
  name: string;
  slug: string;
  short_description: string;
  description: Record<string, unknown>;
  hero_title: string;
  hero_description: string;
  hero_image_id: string | null;
  icon: string;
  status: IndustryStatus;
  published_at: string | null;
  scheduled_for: string | null;
  is_featured: boolean;
  is_active: boolean;
  is_publicly_available: boolean;
  sort_order: number;
  challenges: unknown[];
  solutions: unknown[];
  benefits: unknown[];
  cta_title: string;
  cta_text: string;
  cta_label: string;
  cta_url: string;
  current_revision_number: number;
  services: IndustryServiceLink[];
  faqs: IndustryFaq[];
  seo: IndustrySeo | null;
  revisions: IndustryRevision[];
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedIndustries {
  items: CatalogIndustry[];
  pagination: PaginationMeta;
}

export interface IndustryFilters {
  page: number;
  pageSize: number;
  search: string;
  status: IndustryStatus | "";
  featuredState: "all" | "featured" | "standard";
  activeState: "all" | "active" | "inactive";
  ordering: string;
}

export interface IndustrySchedulePayload {
  scheduled_for: string;
}
