import { z } from "zod";

import { caseStudyStatuses } from "./types";

const caseStudyServiceSchema = z.object({
  id: z.string(),
  service_id: z.string(),
  service_title: z.string(),
  description: z.string(),
  sort_order: z.number(),
});

const caseStudyTechnologySchema = z.object({
  id: z.string(),
  name: z.string(),
  description: z.string(),
  logo_id: z.string().nullable(),
  sort_order: z.number(),
});

const caseStudyMediaSchema = z.object({
  id: z.string(),
  asset_id: z.string(),
  asset_title: z.string(),
  title: z.string(),
  caption: z.string(),
  media_role: z.string(),
  sort_order: z.number(),
});

const caseStudyMetricSchema = z.object({
  id: z.string(),
  label: z.string(),
  value: z.string(),
  description: z.string(),
  icon: z.string(),
  sort_order: z.number(),
});

const caseStudyMilestoneSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string(),
  milestone_date: z.string().nullable(),
  sort_order: z.number(),
});

const caseStudySeoSchema = z.object({
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

const caseStudyRevisionSchema = z.object({
  id: z.string(),
  revision_number: z.number(),
  snapshot: z.record(z.string(), z.unknown()),
  change_summary: z.string(),
  created_at: z.string(),
});

export const caseStudySchema = z.object({
  id: z.string(),
  title: z.string(),
  slug: z.string(),

  client_id: z.string().nullable(),
  client_name: z.string(),
  linked_client_name: z.string().nullable(),

  project_id: z.string().nullable(),
  project_name: z.string().nullable(),

  industry_id: z.string().nullable(),
  industry_name: z.string().nullable(),

  location: z.string(),
  website_url: z.string(),
  short_description: z.string(),

  overview: z.record(z.string(), z.unknown()),
  challenge: z.record(z.string(), z.unknown()),
  solution: z.record(z.string(), z.unknown()),
  implementation: z.record(z.string(), z.unknown()),
  results: z.record(z.string(), z.unknown()),

  testimonial: z.string(),
  testimonial_author: z.string(),
  testimonial_position: z.string(),

  featured_image_id: z.string().nullable(),

  status: z.enum(caseStudyStatuses),
  published_at: z.string().nullable(),
  scheduled_for: z.string().nullable(),

  project_start_date: z.string().nullable(),
  project_completion_date: z.string().nullable(),
  project_duration: z.string(),

  is_featured: z.boolean(),
  is_active: z.boolean(),
  is_publicly_available: z.boolean(),

  sort_order: z.number(),
  view_count: z.number(),
  current_revision_number: z.number(),

  services: z.array(caseStudyServiceSchema),
  technologies: z.array(caseStudyTechnologySchema),
  media_items: z.array(caseStudyMediaSchema),
  metrics: z.array(caseStudyMetricSchema),
  milestones: z.array(caseStudyMilestoneSchema),

  seo: caseStudySeoSchema.nullable(),
  revisions: z.array(caseStudyRevisionSchema),

  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedCaseStudiesSchema = z.object({
  items: z.array(caseStudySchema),
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
