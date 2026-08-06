import { z } from "zod";

import { industryStatuses } from "./types";

const industryServiceLinkSchema = z.object({
  id: z.string(),
  service_id: z.string(),
  service_title: z.string(),
  description: z.string(),
  sort_order: z.number(),
  is_featured: z.boolean(),
});

const industryFaqSchema = z.object({
  id: z.string(),
  question: z.string(),
  answer: z.string(),
  sort_order: z.number(),
});

const industrySeoSchema = z.object({
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
  structured_data: z.record(z.string(), z.unknown()),
});

const industryRevisionSchema = z.object({
  id: z.string(),
  revision_number: z.number(),
  snapshot: z.record(z.string(), z.unknown()),
  change_summary: z.string(),
  created_at: z.string(),
});

export const catalogIndustrySchema = z.object({
  id: z.string(),
  name: z.string(),
  slug: z.string(),
  short_description: z.string(),
  description: z.record(z.string(), z.unknown()),
  hero_title: z.string(),
  hero_description: z.string(),
  hero_image_id: z.string().nullable(),
  icon: z.string(),
  status: z.enum(industryStatuses),
  published_at: z.string().nullable(),
  scheduled_for: z.string().nullable(),
  is_featured: z.boolean(),
  is_active: z.boolean(),
  is_publicly_available: z.boolean(),
  sort_order: z.number(),
  challenges: z.array(z.unknown()),
  solutions: z.array(z.unknown()),
  benefits: z.array(z.unknown()),
  cta_title: z.string(),
  cta_text: z.string(),
  cta_label: z.string(),
  cta_url: z.string(),
  current_revision_number: z.number(),
  services: z.array(industryServiceLinkSchema),
  faqs: z.array(industryFaqSchema),
  seo: industrySeoSchema.nullable(),
  revisions: z.array(industryRevisionSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedIndustriesSchema = z.object({
  items: z.array(catalogIndustrySchema),
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
