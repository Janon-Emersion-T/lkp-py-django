import { z } from "zod";

import { enquiryPriorities, enquirySources, enquiryStatuses } from "./types";

const nullableDecimalSchema = z
  .union([z.string(), z.number()])
  .nullable()
  .transform((value) => (value === null ? null : String(value)));

export const enquiryNoteSchema = z.object({
  id: z.string(),
  author_id: z.string().nullable(),
  author_name: z.string().nullable(),
  note: z.string(),
  is_private: z.boolean(),
  created_at: z.string(),
});

const baseEnquiryFields = {
  id: z.string(),
  reference_code: z.string(),
  name: z.string(),
  email: z.string(),
  phone: z.string(),
  company_name: z.string(),
  source: z.enum(enquirySources),
  source_url: z.string(),
  status: z.enum(enquiryStatuses),
  priority: z.enum(enquiryPriorities),
  assigned_to_id: z.string().nullable(),
  assigned_to_name: z.string().nullable(),
  client_id: z.string().nullable(),
  lead_id: z.string().nullable(),
  submitted_at: z.string(),
  first_contacted_at: z.string().nullable(),
  resolved_at: z.string().nullable(),
  last_follow_up_at: z.string().nullable(),
  next_follow_up_at: z.string().nullable(),
  internal_summary: z.string(),
  loss_reason: z.string(),
  metadata: z.record(z.string(), z.unknown()),
  notes: z.array(enquiryNoteSchema),
  created_at: z.string(),
  updated_at: z.string(),
};

export const contactEnquirySchema = z.object({
  ...baseEnquiryFields,
  subject: z.string(),
  message: z.string(),
});

export const quoteEnquiryServiceSchema = z.object({
  id: z.string(),
  service_id: z.string(),
  service_title: z.string(),
  notes: z.string(),
  sort_order: z.number(),
});

export const quoteEnquirySchema = z.object({
  ...baseEnquiryFields,
  country: z.string(),
  website_url: z.string(),
  project_title: z.string(),
  project_description: z.string(),
  preferred_package_id: z.string().nullable(),
  budget_min: nullableDecimalSchema,
  budget_max: nullableDecimalSchema,
  budget_currency: z.string(),
  desired_start_date: z.string().nullable(),
  desired_completion_date: z.string().nullable(),
  quotation_id: z.string().nullable(),
  services: z.array(quoteEnquiryServiceSchema),
});

export const enquiryDashboardSchema = z.object({
  total_contact_enquiries: z.number(),
  total_quote_enquiries: z.number(),
  new_contact_enquiries: z.number(),
  new_quote_enquiries: z.number(),
  active_contact_enquiries: z.number(),
  active_quote_enquiries: z.number(),
  won_contact_enquiries: z.number(),
  won_quote_enquiries: z.number(),
  lost_contact_enquiries: z.number(),
  lost_quote_enquiries: z.number(),
  urgent_contact_enquiries: z.number(),
  urgent_quote_enquiries: z.number(),
  overdue_contact_follow_ups: z.number(),
  overdue_quote_follow_ups: z.number(),
  contact_enquiries_by_status: z.record(z.string(), z.number()),
  quote_enquiries_by_status: z.record(z.string(), z.number()),
  contact_enquiries_by_source: z.record(z.string(), z.number()),
  quote_enquiries_by_source: z.record(z.string(), z.number()),
});
