export const testimonialStatuses = [
  "draft",
  "review",
  "scheduled",
  "published",
  "archived",
] as const;

export type TestimonialStatus = (typeof testimonialStatuses)[number];

export const testimonialSources = [
  "direct",
  "google",
  "facebook",
  "linkedin",
  "whatsapp",
  "email",
  "other",
] as const;

export type TestimonialSource = (typeof testimonialSources)[number];

export interface Testimonial {
  id: string;
  client_id: string | null;
  client_name: string | null;
  project_id: string | null;
  project_title: string | null;
  author_name: string;
  author_position: string;
  company_name: string;
  content: string;
  short_content: string;
  rating: number;
  source: TestimonialSource;
  source_url: string;
  author_image_id: string | null;
  company_logo_id: string | null;
  status: TestimonialStatus;
  published_at: string | null;
  scheduled_for: string | null;
  is_featured: boolean;
  is_verified: boolean;
  is_active: boolean;
  is_publicly_available: boolean;
  sort_order: number;
  internal_notes: string;
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedTestimonials {
  items: Testimonial[];
  pagination: PaginationMeta;
}

export interface TestimonialFilters {
  page: number;
  pageSize: number;
  search: string;
  status: TestimonialStatus | "";
  source: TestimonialSource | "";
  rating: number | "";
  featuredState: "all" | "featured" | "standard";
  verifiedState: "all" | "verified" | "unverified";
  activeState: "all" | "active" | "inactive";
  clientId: string;
  projectId: string;
  ordering: string;
}

export interface TestimonialSchedulePayload {
  scheduled_for: string;
}
