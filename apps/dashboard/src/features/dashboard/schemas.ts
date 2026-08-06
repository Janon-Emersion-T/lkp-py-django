import {
  z,
} from "zod";

import {
  dashboardPeriodPresets,
} from "./types";

const countSchema = z.number().int().nonnegative();

const decimalValueSchema = z.union([
  z.number(),
  z.string(),
]);

const currencyAmountSchema = z.object({
  currency: z.string(),
  amount: decimalValueSchema,
});

const accountBalanceSchema = z.object({
  id: z.union([
    z.string(),
    z.number(),
  ]),
  name: z.string(),
  currency: z.string(),
  current_balance: decimalValueSchema,
});

const dashboardPeriodSchema = z.object({
  preset: z.enum(dashboardPeriodPresets),
  date_from: z.string(),
  date_to: z.string(),
  datetime_from: z.string(),
  datetime_to: z.string(),
});

const executiveSummarySchema = z.object({
  total_clients: countSchema,
  active_clients: countSchema,
  total_leads: countSchema,
  qualified_leads: countSchema,
  won_leads: countSchema,
  lost_leads: countSchema,
  lead_conversion_rate: z.number(),
  open_enquiries: countSchema,
  overdue_follow_ups: countSchema,
});

const clientMetricsSchema = z.object({
  total_clients: countSchema,
  active_clients: countSchema,
  new_clients: countSchema,
});

const crmMetricsSchema = z.object({
  total_leads: countSchema,
  qualified_leads: countSchema,
  won_leads: countSchema,
  lost_leads: countSchema,
  overdue_follow_ups: countSchema,
  period_leads: countSchema,
  lead_conversion_rate: z.number(),
});

const salesMetricsSchema = z.object({
  total_quotations: countSchema,
  accepted_quotations: countSchema,
  period_quotations: countSchema,
  quotation_value_by_currency: z.array(
    currencyAmountSchema,
  ),
  accepted_quotation_value_by_currency: z.array(
    currencyAmountSchema,
  ),
});

const projectMetricsSchema = z.object({
  active_projects: countSchema,
  completed_projects: countSchema,
  overdue_projects: countSchema,
  completed_in_period: countSchema,
});

const taskMetricsSchema = z.object({
  open_tasks: countSchema,
  overdue_tasks: countSchema,
  completed_tasks: countSchema,
  completed_in_period: countSchema,
});

const financeMetricsSchema = z.object({
  outstanding_invoices: countSchema,
  overdue_invoices: countSchema,
  outstanding_value_by_currency: z.array(
    currencyAmountSchema,
  ),
  overdue_value_by_currency: z.array(
    currencyAmountSchema,
  ),
  revenue_by_currency: z.array(
    currencyAmountSchema,
  ),
  cash_and_bank_balances: z.array(
    accountBalanceSchema,
  ),
});

const enquiryBreakdownSchema = z.object({
  open_count: countSchema,
  overdue_follow_ups: countSchema,
  submitted_in_period: countSchema,
});

const enquiryMetricsSchema = z.object({
  open_enquiries: countSchema,
  overdue_follow_ups: countSchema,
  submitted_in_period: countSchema,
  contact_enquiries: enquiryBreakdownSchema,
  quote_enquiries: enquiryBreakdownSchema,
});

const workforceMetricsSchema = z.object({
  active_team_members: countSchema,
  open_job_positions: countSchema,
  open_job_listings: countSchema,
  newsletter_subscribers: countSchema,
});

export const executiveDashboardReportSchema = z.object({
  report_type: z.literal("executive"),
  environment: z.string(),
  period: dashboardPeriodSchema,
  generated_at: z.string(),
  timezone: z.string(),
  schema_version: z.number().int().positive(),
  data: z.object({
    clients: clientMetricsSchema,
    crm: crmMetricsSchema,
    sales: salesMetricsSchema,
    projects: projectMetricsSchema,
    tasks: taskMetricsSchema,
    finance: financeMetricsSchema,
    enquiries: enquiryMetricsSchema,
    workforce: workforceMetricsSchema,
    summary: executiveSummarySchema,
  }),
  metadata: z.object({
    foundation: z.boolean(),
    aggregation_status: z.string(),
  }),
});
