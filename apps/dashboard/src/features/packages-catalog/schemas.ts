import { z } from "zod";

import {
  billingCycles,
  packageCategories,
  packageStatuses,
  pricingTypes,
} from "./types";

const packageFeatureSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  is_included: z.boolean(),
  value: z.string(),
  icon: z.string(),
  sort_order: z.number(),
});

const packageAddonSchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  price: z.string(),
  currency: z.string(),
  billing_cycle: z.enum(billingCycles),
  is_active: z.boolean(),
  sort_order: z.number(),
});

const packageTargetAudienceSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  sort_order: z.number(),
});

const packageFaqSchema = z.object({
  id: z.string(),
  question: z.string(),
  answer: z.string(),
  sort_order: z.number(),
});

const packageSeoSchema = z.object({
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

const packageRevisionSchema = z.object({
  id: z.string(),
  revision_number: z.number(),
  snapshot: z.record(z.string(), z.unknown()),
  change_summary: z.string(),
  created_at: z.string(),
});

export const catalogPackageSchema = z.object({
  id: z.string(),
  name: z.string(),
  slug: z.string(),
  category: z.enum(packageCategories),
  service_id: z.string().nullable(),
  service_title: z.string().nullable(),
  short_description: z.string(),
  description: z.record(z.string(), z.unknown()),
  pricing_type: z.enum(pricingTypes),
  price: z.string(),
  compare_at_price: z.string().nullable(),
  currency: z.string(),
  billing_cycle: z.enum(billingCycles),
  delivery_time: z.string(),
  revisions_included: z.number(),
  support_period_days: z.number(),
  status: z.enum(packageStatuses),
  published_at: z.string().nullable(),
  scheduled_for: z.string().nullable(),
  is_featured: z.boolean(),
  is_popular: z.boolean(),
  is_active: z.boolean(),
  is_publicly_available: z.boolean(),
  sort_order: z.number(),
  badge_text: z.string(),
  cta_label: z.string(),
  cta_url: z.string(),
  current_revision_number: z.number(),
  features: z.array(packageFeatureSchema),
  addons: z.array(packageAddonSchema),
  target_audiences: z.array(packageTargetAudienceSchema),
  faqs: z.array(packageFaqSchema),
  seo: packageSeoSchema.nullable(),
  revisions: z.array(packageRevisionSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedPackagesSchema = z.object({
  items: z.array(catalogPackageSchema),
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
