export const insightStatuses = [
  "draft",
  "review",
  "scheduled",
  "published",
  "archived",
] as const;

export type InsightStatus = (typeof insightStatuses)[number];

export interface InsightCategory {
  id: string;
  name: string;
  slug: string;
  description: string;
  parent_id: string | null;
  is_active: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export interface InsightTag {
  id: string;
  name: string;
  slug: string;
  description: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface InsightArticleTag {
  id: string;
  name: string;
  slug: string;
}

export interface RelatedInsightArticle {
  id: string;
  title: string;
  slug: string;
}

export interface InsightInternalLink {
  id: string;
  target_article_id: string;
  target_article_title: string;
  anchor_text: string;
  context: string;
  is_active: boolean;
}

export interface InsightSeo {
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
  article_schema: Record<string, unknown>;
  faq_schema: Array<Record<string, unknown>>;
}

export interface InsightRevision {
  id: string;
  revision_number: number;
  snapshot: Record<string, unknown>;
  change_summary: string;
  created_at: string;
}

export interface InsightPublishingEvent {
  id: string;
  event_type: string;
  description: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface InsightArticle {
  id: string;
  title: string;
  slug: string;
  excerpt: string;
  content: Record<string, unknown>;
  category_id: string | null;
  category_name: string | null;
  author_id: number | null;
  author_email: string | null;
  featured_image_id: string | null;
  status: InsightStatus;
  published_at: string | null;
  scheduled_for: string | null;
  reading_time_minutes: number;
  word_count: number;
  view_count: number;
  is_featured: boolean;
  is_active: boolean;
  allow_comments: boolean;
  is_publicly_available: boolean;
  current_revision_number: number;
  tags: InsightArticleTag[];
  related_articles: RelatedInsightArticle[];
  internal_links: InsightInternalLink[];
  seo: InsightSeo | null;
  revisions: InsightRevision[];
  publishing_events: InsightPublishingEvent[];
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedInsights {
  items: InsightArticle[];
  pagination: PaginationMeta;
}

export interface InsightFilters {
  page: number;
  pageSize: number;
  search: string;
  status: InsightStatus | "";
  categoryId: string;
  tagId: string;
  featuredState: "all" | "featured" | "standard";
  activeState: "all" | "active" | "inactive";
  ordering: string;
}

export interface InsightSchedulePayload {
  scheduled_for: string;
}
