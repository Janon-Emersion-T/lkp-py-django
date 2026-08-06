import { z } from "zod";

import { insightStatuses } from "./types";

export const insightCategorySchema = z.object({
  id: z.string(),
  name: z.string(),
  slug: z.string(),
  description: z.string(),
  parent_id: z.string().nullable(),
  is_active: z.boolean(),
  sort_order: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const insightTagSchema = z.object({
  id: z.string(),
  name: z.string(),
  slug: z.string(),
  description: z.string(),
  is_active: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
});

const insightArticleTagSchema = z.object({
  id: z.string(),
  name: z.string(),
  slug: z.string(),
});

const relatedInsightArticleSchema = z.object({
  id: z.string(),
  title: z.string(),
  slug: z.string(),
});

const insightInternalLinkSchema = z.object({
  id: z.string(),
  target_article_id: z.string(),
  target_article_title: z.string(),
  anchor_text: z.string(),
  context: z.string(),
  is_active: z.boolean(),
});

const insightSeoSchema = z.object({
  id: z.string(),
  meta_title: z.string(),
  meta_description: z.string(),
  canonical_url: z.string(),
  robots_index: z.boolean(),
  robots_follow: z.boolean(),
  open_graph_title: z.string(),
  open_graph_description: z.string(),
  open_graph_image_id: z.string().nullable(),
  twitter_title: z.string(),
  twitter_description: z.string(),
  article_schema: z.record(z.string(), z.unknown()),
  faq_schema: z.array(z.record(z.string(), z.unknown())),
});

const insightRevisionSchema = z.object({
  id: z.string(),
  revision_number: z.number(),
  snapshot: z.record(z.string(), z.unknown()),
  change_summary: z.string(),
  created_at: z.string(),
});

const insightPublishingEventSchema = z.object({
  id: z.string(),
  event_type: z.string(),
  description: z.string(),
  metadata: z.record(z.string(), z.unknown()),
  created_at: z.string(),
});

export const insightArticleSchema = z.object({
  id: z.string(),
  title: z.string(),
  slug: z.string(),
  excerpt: z.string(),
  content: z.record(z.string(), z.unknown()),
  category_id: z.string().nullable(),
  category_name: z.string().nullable(),
  author_id: z.number().nullable(),
  author_email: z.string().nullable(),
  featured_image_id: z.string().nullable(),
  status: z.enum(insightStatuses),
  published_at: z.string().nullable(),
  scheduled_for: z.string().nullable(),
  reading_time_minutes: z.number(),
  word_count: z.number(),
  view_count: z.number(),
  is_featured: z.boolean(),
  is_active: z.boolean(),
  allow_comments: z.boolean(),
  is_publicly_available: z.boolean(),
  current_revision_number: z.number(),
  tags: z.array(insightArticleTagSchema),
  related_articles: z.array(relatedInsightArticleSchema),
  internal_links: z.array(insightInternalLinkSchema),
  seo: insightSeoSchema.nullable(),
  revisions: z.array(insightRevisionSchema),
  publishing_events: z.array(insightPublishingEventSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedInsightsSchema = z.object({
  items: z.array(insightArticleSchema),
  pagination: z.object({
    page: z.number(),
    page_size: z.number(),
    total_items: z.number(),
    total_pages: z.number(),
  }),
});

export const messageSchema = z.object({
  status: z.string(),
  message: z.string(),
});
