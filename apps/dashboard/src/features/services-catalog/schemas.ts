import {
  z,
} from "zod";

import {
  serviceStatuses,
} from "./types";

const jsonObjectSchema =
  z.record(
    z.string(),
    z.unknown(),
  );

export const serviceFeatureSchema =
  z.object({
    id: z.string().uuid(),
    title: z.string(),
    description: z.string(),
    icon: z.string(),
    sort_order:
      z.number().int().nonnegative(),
  });

export const serviceProcessStepSchema =
  z.object({
    id: z.string().uuid(),
    title: z.string(),
    description: z.string(),
    step_number:
      z.number().int().positive(),
    sort_order:
      z.number().int().nonnegative(),
  });

export const serviceTechnologySchema =
  z.object({
    id: z.string().uuid(),
    name: z.string(),
    description: z.string(),
    logo_id:
      z.string().uuid().nullable(),
    sort_order:
      z.number().int().nonnegative(),
  });

export const serviceFaqSchema =
  z.object({
    id: z.string().uuid(),
    question: z.string(),
    answer: z.string(),
    sort_order:
      z.number().int().nonnegative(),
  });

export const serviceSeoSchema =
  z.object({
    id: z.string().uuid(),
    meta_title: z.string(),
    meta_description: z.string(),
    canonical_url: z.string(),
    robots_index: z.boolean(),
    robots_follow: z.boolean(),
    open_graph_title: z.string(),
    open_graph_description:
      z.string(),
    open_graph_image_id:
      z.string().uuid().nullable(),
    twitter_title: z.string(),
    twitter_description: z.string(),
    structured_data:
      jsonObjectSchema,
  });

export const serviceRevisionSchema =
  z.object({
    id: z.string().uuid(),
    revision_number:
      z.number().int().positive(),
    snapshot: jsonObjectSchema,
    change_summary: z.string(),
    created_at: z.string(),
  });

export const catalogServiceSchema =
  z.object({
    id: z.string().uuid(),
    title: z.string(),
    slug: z.string(),
    short_description: z.string(),
    description: jsonObjectSchema,
    hero_title: z.string(),
    hero_description: z.string(),
    hero_image_id:
      z.string().uuid().nullable(),
    status: z.enum(serviceStatuses),
    published_at:
      z.string().nullable(),
    scheduled_for:
      z.string().nullable(),
    icon: z.string(),
    sort_order:
      z.number().int().nonnegative(),
    is_featured: z.boolean(),
    is_active: z.boolean(),
    is_publicly_available:
      z.boolean(),
    cta_title: z.string(),
    cta_text: z.string(),
    cta_label: z.string(),
    cta_url: z.string(),
    current_revision_number:
      z.number().int().positive(),
    features:
      z.array(serviceFeatureSchema),
    process_steps:
      z.array(
        serviceProcessStepSchema,
      ),
    technologies:
      z.array(
        serviceTechnologySchema,
      ),
    faqs:
      z.array(serviceFaqSchema),
    seo:
      serviceSeoSchema.nullable(),
    revisions:
      z.array(serviceRevisionSchema),
    created_at: z.string(),
    updated_at: z.string(),
  });

export const paginatedServicesSchema =
  z.object({
    items:
      z.array(catalogServiceSchema),
    pagination: z.object({
      page:
        z.number().int().positive(),
      page_size:
        z.number().int().positive(),
      total_items:
        z.number().int().nonnegative(),
      total_pages:
        z.number().int().nonnegative(),
    }),
  });

export const messageSchema =
  z.object({
    status: z.string(),
    message: z.string(),
  });
