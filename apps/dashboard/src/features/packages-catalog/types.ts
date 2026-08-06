export const packageCategories = [
  "website",
  "seo",
  "marketing",
  "software",
  "mobile_app",
  "hosting",
  "maintenance",
  "consulting",
  "other",
] as const;

export type PackageCategory = (typeof packageCategories)[number];

export const packageStatuses = [
  "draft",
  "scheduled",
  "published",
  "archived",
] as const;

export type PackageStatus = (typeof packageStatuses)[number];

export const pricingTypes = [
  "fixed",
  "starting_from",
  "custom_quote",
  "free",
] as const;

export type PricingType = (typeof pricingTypes)[number];

export const billingCycles = [
  "one_time",
  "monthly",
  "quarterly",
  "half_yearly",
  "yearly",
] as const;

export type BillingCycle = (typeof billingCycles)[number];

export interface PackageFeature {
  id: string;
  title: string;
  description: string;
  is_included: boolean;
  value: string;
  icon: string;
  sort_order: number;
}

export interface PackageAddon {
  id: string;
  name: string;
  description: string;
  price: string;
  currency: string;
  billing_cycle: BillingCycle;
  is_active: boolean;
  sort_order: number;
}

export interface PackageTargetAudience {
  id: string;
  title: string;
  description: string;
  sort_order: number;
}

export interface PackageFaq {
  id: string;
  question: string;
  answer: string;
  sort_order: number;
}

export interface PackageSeo {
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

export interface PackageRevision {
  id: string;
  revision_number: number;
  snapshot: Record<string, unknown>;
  change_summary: string;
  created_at: string;
}

export interface CatalogPackage {
  id: string;
  name: string;
  slug: string;
  category: PackageCategory;
  service_id: string | null;
  service_title: string | null;
  short_description: string;
  description: Record<string, unknown>;
  pricing_type: PricingType;
  price: string;
  compare_at_price: string | null;
  currency: string;
  billing_cycle: BillingCycle;
  delivery_time: string;
  revisions_included: number;
  support_period_days: number;
  status: PackageStatus;
  published_at: string | null;
  scheduled_for: string | null;
  is_featured: boolean;
  is_popular: boolean;
  is_active: boolean;
  is_publicly_available: boolean;
  sort_order: number;
  badge_text: string;
  cta_label: string;
  cta_url: string;
  current_revision_number: number;
  features: PackageFeature[];
  addons: PackageAddon[];
  target_audiences: PackageTargetAudience[];
  faqs: PackageFaq[];
  seo: PackageSeo | null;
  revisions: PackageRevision[];
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedPackages {
  items: CatalogPackage[];
  pagination: PaginationMeta;
}

export interface PackageFilters {
  page: number;
  pageSize: number;
  search: string;
  category: PackageCategory | "";
  status: PackageStatus | "";
  currency: string;
  billingCycle: BillingCycle | "";
  featuredState: "all" | "featured" | "standard";
  popularState: "all" | "popular" | "standard";
  activeState: "all" | "active" | "inactive";
  ordering: string;
}

export interface PackageSchedulePayload {
  scheduled_for: string;
}
