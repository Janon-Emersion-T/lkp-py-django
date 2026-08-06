import { z } from "zod";

import { testimonialSources, testimonialStatuses } from "./types";

export const testimonialSchema = z.object({
  id: z.string(),
  client_id: z.string().nullable(),
  client_name: z.string().nullable(),
  project_id: z.string().nullable(),
  project_title: z.string().nullable(),
  author_name: z.string(),
  author_position: z.string(),
  company_name: z.string(),
  content: z.string(),
  short_content: z.string(),
  rating: z.number(),
  source: z.enum(testimonialSources),
  source_url: z.string(),
  author_image_id: z.string().nullable(),
  company_logo_id: z.string().nullable(),
  status: z.enum(testimonialStatuses),
  published_at: z.string().nullable(),
  scheduled_for: z.string().nullable(),
  is_featured: z.boolean(),
  is_verified: z.boolean(),
  is_active: z.boolean(),
  is_publicly_available: z.boolean(),
  sort_order: z.number(),
  internal_notes: z.string(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedTestimonialsSchema = z.object({
  items: z.array(testimonialSchema),
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
