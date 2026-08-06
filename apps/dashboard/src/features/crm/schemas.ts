import {
  z,
} from "zod";

import {
  leadPriorities,
  leadSources,
  leadStatuses,
} from "./types";

const nonNegativeCount = z.number().int().nonnegative();

const userSummarySchema = z.object({
  id: z.number().int(),
  email: z.string(),
  first_name: z.string(),
  last_name: z.string(),
});

export const leadSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  company: z.string(),
  email: z.string(),
  phone: z.string(),
  whatsapp: z.string(),
  country: z.string(),
  website: z.string(),
  source: z.enum(leadSources),
  status: z.enum(leadStatuses),
  priority: z.enum(leadPriorities),
  assigned_to: userSummarySchema.nullable(),
  lead_score: z.number().int().min(0).max(100),
  estimated_value: z.string().nullable(),
  currency: z.string(),
  notes: z.string(),
  tags: z.array(z.string()),
  next_follow_up_at: z.string().nullable(),
  last_contacted_at: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedLeadsSchema = z.object({
  items: z.array(leadSchema),
  pagination: z.object({
    page: z.number().int().positive(),
    page_size: z.number().int().positive(),
    total_items: nonNegativeCount,
    total_pages: nonNegativeCount,
  }),
});

const crmSummarySchema = z.object({
  total_leads: nonNegativeCount,
  new_leads: nonNegativeCount,
  contacted_leads: nonNegativeCount,
  follow_up_leads: nonNegativeCount,
  proposal_sent_leads: nonNegativeCount,
  negotiation_leads: nonNegativeCount,
  won_leads: nonNegativeCount,
  lost_leads: nonNegativeCount,
  spam_leads: nonNegativeCount,
  overdue_follow_ups: nonNegativeCount,
  unassigned_leads: nonNegativeCount,
  conversion_rate: z.number(),
  all_time_total_leads: nonNegativeCount,
  all_time_won_leads: nonNegativeCount,
  all_time_lost_leads: nonNegativeCount,
});

export const crmReportSchema = z.object({
  report_type: z.literal("crm"),
  environment: z.string(),
  period: z.object({
    preset: z.string(),
    date_from: z.string(),
    date_to: z.string(),
    datetime_from: z.string(),
    datetime_to: z.string(),
  }),
  generated_at: z.string(),
  timezone: z.string(),
  schema_version: z.number().int().positive(),
  data: z.object({
    summary: crmSummarySchema,
    leads_by_status: z.array(z.unknown()),
    leads_by_source: z.array(z.unknown()),
    leads_by_owner: z.array(z.unknown()),
    conversion_funnel: z.array(z.unknown()),
    monthly_lead_trend: z.array(z.unknown()),
    won_lost_trend: z.array(z.unknown()),
    estimated_value_by_currency: z.array(z.unknown()),
    metadata: z.record(
      z.string(),
      z.unknown(),
    ),
  }),
  metadata: z.object({
    foundation: z.boolean(),
    aggregation_status: z.string(),
  }),
});
