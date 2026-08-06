export const cmsContentTypes = [
  "pages",
  "services",
  "packages",
  "industries",
  "insights",
  "case-studies",
  "testimonials",
] as const;

export type CmsContentType =
  (typeof cmsContentTypes)[number];

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface CmsBaseRecord {
  id: string;
  status: string;
  is_active: boolean;
  is_featured?: boolean;
  is_publicly_available?: boolean;
  published_at: string | null;
  scheduled_for: string | null;
  created_at: string;
  updated_at: string;
}

export interface CmsPage
  extends CmsBaseRecord {
  title: string;
  slug: string;
  page_type: string;
  excerpt: string;
  content: Record<string, unknown>;
  featured_image_id: string | null;
  is_indexable: boolean;
  is_visible_in_navigation: boolean;
  navigation_label: string;
  navigation_order: number;
  current_revision_number: number;
  seo: Record<string, unknown> | null;
  revisions: Array<Record<string, unknown>>;
}

export interface CmsService
  extends CmsBaseRecord {
  title: string;
  slug: string;
  short_description: string;
  description: Record<string, unknown>;
  icon: string;
  hero_title: string;
  hero_description: string;
  hero_image_id: string | null;
  sort_order: number;
  view_count: number;
  current_revision_number: number;
  features: Array<Record<string, unknown>>;
  technologies: Array<Record<string, unknown>>;
  process_steps: Array<Record<string, unknown>>;
  faqs: Array<Record<string, unknown>>;
  seo: Record<string, unknown> | null;
  revisions: Array<Record<string, unknown>>;
}

export interface CmsPackage
  extends CmsBaseRecord {
  name: string;
  slug: string;
  category: string;
  service_id: string | null;
  service_title: string | null;
  short_description: string;
  description: Record<string, unknown>;
  pricing_type: string;
  price: string;
  compare_at_price: string | null;
  currency: string;
  billing_cycle: string;
  delivery_time: string;
  revisions_included: number;
  support_period_days: number;
  is_popular: boolean;
  sort_order: number;
  badge_text: string;
  cta_label: string;
  cta_url: string;
  current_revision_number: number;
  features: Array<Record<string, unknown>>;
  addons: Array<Record<string, unknown>>;
  target_audiences: Array<Record<string, unknown>>;
  faqs: Array<Record<string, unknown>>;
  seo: Record<string, unknown> | null;
  revisions: Array<Record<string, unknown>>;
}

export interface CmsIndustry
  extends CmsBaseRecord {
  name: string;
  slug: string;
  short_description: string;
  description: Record<string, unknown>;
  hero_title: string;
  hero_description: string;
  hero_image_id: string | null;
  icon: string;
  sort_order: number;
  challenges: unknown[];
  solutions: unknown[];
  benefits: unknown[];
  cta_title: string;
  cta_text: string;
  cta_label: string;
  cta_url: string;
  current_revision_number: number;
  services: Array<Record<string, unknown>>;
  faqs: Array<Record<string, unknown>>;
  seo: Record<string, unknown> | null;
  revisions: Array<Record<string, unknown>>;
}

export interface CmsInsight
  extends CmsBaseRecord {
  title: string;
  slug: string;
  excerpt: string;
  content: Record<string, unknown>;
  category_id: string | null;
  category_name: string | null;
  author_id: number | null;
  author_email: string | null;
  featured_image_id: string | null;
  reading_time_minutes: number;
  word_count: number;
  view_count: number;
  allow_comments: boolean;
  current_revision_number: number;
  tags: Array<Record<string, unknown>>;
  related_articles: Array<Record<string, unknown>>;
  internal_links: Array<Record<string, unknown>>;
  seo: Record<string, unknown> | null;
  revisions: Array<Record<string, unknown>>;
  publishing_events: Array<Record<string, unknown>>;
}

export interface CmsCaseStudy
  extends CmsBaseRecord {
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
  project_start_date: string | null;
  project_completion_date: string | null;
  project_duration: string;
  sort_order: number;
  view_count: number;
  current_revision_number: number;
  services: Array<Record<string, unknown>>;
  technologies: Array<Record<string, unknown>>;
  media_items: Array<Record<string, unknown>>;
  metrics: Array<Record<string, unknown>>;
  milestones: Array<Record<string, unknown>>;
  seo: Record<string, unknown> | null;
  revisions: Array<Record<string, unknown>>;
}

export interface CmsTestimonial
  extends CmsBaseRecord {
  title?: string;
  author_name: string;
  author_position: string;
  company_name: string;
  content: string;
  rating: number;
  source: string;
  client_id: string | null;
  project_id: string | null;
  is_verified: boolean;
  sort_order: number;
}

export type CmsRecord =
  | CmsPage
  | CmsService
  | CmsPackage
  | CmsIndustry
  | CmsInsight
  | CmsCaseStudy
  | CmsTestimonial;

export interface PaginatedCmsRecords {
  items: CmsRecord[];
  pagination: PaginationMeta;
}

export interface CmsFilters {
  page: number;
  pageSize: number;
  search: string;
  status: string;
  featured: boolean | null;
  active: boolean | null;
  ordering: string;
}

export interface CmsDetailSelection {
  type: CmsContentType;
  id: string;
}
