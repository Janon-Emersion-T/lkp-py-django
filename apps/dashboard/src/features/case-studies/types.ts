export const caseStudyStatuses = [
  "draft",
  "review",
  "scheduled",
  "published",
  "archived",
] as const;

export type CaseStudyStatus = (typeof caseStudyStatuses)[number];

export interface CaseStudyServiceLink {
  id: string;
  service_id: string;
  service_title: string;
  description: string;
  sort_order: number;
}

export interface CaseStudyTechnology {
  id: string;
  name: string;
  description: string;
  logo_id: string | null;
  sort_order: number;
}

export interface CaseStudyMedia {
  id: string;
  asset_id: string;
  asset_title: string;
  title: string;
  caption: string;
  media_role: string;
  sort_order: number;
}

export interface CaseStudyMetric {
  id: string;
  label: string;
  value: string;
  description: string;
  icon: string;
  sort_order: number;
}

export interface CaseStudyMilestone {
  id: string;
  title: string;
  description: string;
  milestone_date: string | null;
  sort_order: number;
}

export interface CaseStudySeo {
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

export interface CaseStudyRevision {
  id: string;
  revision_number: number;
  snapshot: Record<string, unknown>;
  change_summary: string;
  created_at: string;
}

export interface CaseStudy {
  id: string;
  title: string;
  slug: string;

  client_id: string | null;
  client_name: string;
  linked_client_name: string | null;

  project_id: string | null;
  project_name: string | null;

  industry_id: string | null;
  industry_name: string | null;

  location: string;
  website_url: string;
  short_description: string;

  overview: Record<string, unknown>;
  challenge: Record<string, unknown>;
  solution: Record<string, unknown>;
  implementation: Record<string, unknown>;
  results: Record<string, unknown>;

  testimonial: string;
  testimonial_author: string;
  testimonial_position: string;

  featured_image_id: string | null;

  status: CaseStudyStatus;
  published_at: string | null;
  scheduled_for: string | null;

  project_start_date: string | null;
  project_completion_date: string | null;
  project_duration: string;

  is_featured: boolean;
  is_active: boolean;
  is_publicly_available: boolean;

  sort_order: number;
  view_count: number;
  current_revision_number: number;

  services: CaseStudyServiceLink[];
  technologies: CaseStudyTechnology[];
  media_items: CaseStudyMedia[];
  metrics: CaseStudyMetric[];
  milestones: CaseStudyMilestone[];

  seo: CaseStudySeo | null;
  revisions: CaseStudyRevision[];

  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedCaseStudies {
  items: CaseStudy[];
  pagination: PaginationMeta;
}

export interface CaseStudyFilters {
  page: number;
  pageSize: number;
  search: string;
  status: CaseStudyStatus | "";
  clientId: string;
  projectId: string;
  industryId: string;
  serviceId: string;
  featuredState: "all" | "featured" | "standard";
  activeState: "all" | "active" | "inactive";
  ordering: string;
}

export interface CaseStudySchedulePayload {
  scheduled_for: string;
}
