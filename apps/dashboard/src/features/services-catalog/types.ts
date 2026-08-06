export const serviceStatuses = [
  "draft",
  "scheduled",
  "published",
  "archived",
] as const;

export type ServiceStatus =
  (typeof serviceStatuses)[number];

export interface ServiceFeature {
  id: string;
  title: string;
  description: string;
  icon: string;
  sort_order: number;
}

export interface ServiceProcessStep {
  id: string;
  title: string;
  description: string;
  step_number: number;
  sort_order: number;
}

export interface ServiceTechnology {
  id: string;
  name: string;
  description: string;
  logo_id: string | null;
  sort_order: number;
}

export interface ServiceFaq {
  id: string;
  question: string;
  answer: string;
  sort_order: number;
}

export interface ServiceSeo {
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

export interface ServiceRevision {
  id: string;
  revision_number: number;
  snapshot: Record<string, unknown>;
  change_summary: string;
  created_at: string;
}

export interface CatalogService {
  id: string;
  title: string;
  slug: string;
  short_description: string;
  description: Record<string, unknown>;
  hero_title: string;
  hero_description: string;
  hero_image_id: string | null;
  status: ServiceStatus;
  published_at: string | null;
  scheduled_for: string | null;
  icon: string;
  sort_order: number;
  is_featured: boolean;
  is_active: boolean;
  is_publicly_available: boolean;
  cta_title: string;
  cta_text: string;
  cta_label: string;
  cta_url: string;
  current_revision_number: number;
  features: ServiceFeature[];
  process_steps: ServiceProcessStep[];
  technologies: ServiceTechnology[];
  faqs: ServiceFaq[];
  seo: ServiceSeo | null;
  revisions: ServiceRevision[];
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedServices {
  items: CatalogService[];
  pagination: PaginationMeta;
}

export interface ServiceFilters {
  page: number;
  pageSize: number;
  search: string;
  status: ServiceStatus | "";
  featuredState:
    | "all"
    | "featured"
    | "standard";
  activeState:
    | "all"
    | "active"
    | "inactive";
  ordering: string;
}

export interface ServiceSchedulePayload {
  scheduled_for: string;
}
