export const leadStatuses = [
  "new",
  "contacted",
  "follow_up",
  "proposal_sent",
  "negotiation",
  "won",
  "lost",
  "spam",
] as const;

export type LeadStatus =
  (typeof leadStatuses)[number];

export const leadSources = [
  "google",
  "organic_search",
  "facebook",
  "instagram",
  "linkedin",
  "tiktok",
  "referral",
  "whatsapp",
  "email",
  "manual",
  "other",
] as const;

export type LeadSource =
  (typeof leadSources)[number];

export const leadPriorities = [
  "low",
  "normal",
  "high",
  "urgent",
] as const;

export type LeadPriority =
  (typeof leadPriorities)[number];

export const leadOrderingOptions = [
  "-created_at",
  "created_at",
  "-updated_at",
  "updated_at",
  "name",
  "-name",
  "company",
  "-company",
  "-lead_score",
  "lead_score",
  "-estimated_value",
  "estimated_value",
  "next_follow_up_at",
  "-next_follow_up_at",
] as const;

export type LeadOrdering =
  (typeof leadOrderingOptions)[number];

export interface UserSummary {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

export interface Lead {
  id: string;
  name: string;
  company: string;
  email: string;
  phone: string;
  whatsapp: string;
  country: string;
  website: string;
  source: LeadSource;
  status: LeadStatus;
  priority: LeadPriority;
  assigned_to: UserSummary | null;
  lead_score: number;
  estimated_value: string | null;
  currency: string;
  notes: string;
  tags: string[];
  next_follow_up_at: string | null;
  last_contacted_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedLeads {
  items: Lead[];
  pagination: PaginationMeta;
}

export interface LeadFilters {
  page: number;
  pageSize: number;
  search: string;
  status: LeadStatus | "";
  source: LeadSource | "";
  country: string;
  ordering: LeadOrdering;
}

export interface CrmReportPeriod {
  preset: string;
  date_from: string;
  date_to: string;
  datetime_from: string;
  datetime_to: string;
}

export interface CrmReportSummary {
  total_leads: number;
  new_leads: number;
  contacted_leads: number;
  follow_up_leads: number;
  proposal_sent_leads: number;
  negotiation_leads: number;
  won_leads: number;
  lost_leads: number;
  spam_leads: number;
  overdue_follow_ups: number;
  unassigned_leads: number;
  conversion_rate: number;
  all_time_total_leads: number;
  all_time_won_leads: number;
  all_time_lost_leads: number;
}

export interface CrmReport {
  report_type: "crm";
  environment: string;
  period: CrmReportPeriod;
  generated_at: string;
  timezone: string;
  schema_version: number;
  data: {
    summary: CrmReportSummary;
    leads_by_status: unknown[];
    leads_by_source: unknown[];
    leads_by_owner: unknown[];
    conversion_funnel: unknown[];
    monthly_lead_trend: unknown[];
    won_lost_trend: unknown[];
    estimated_value_by_currency: unknown[];
    metadata: Record<string, unknown>;
  };
  metadata: {
    foundation: boolean;
    aggregation_status: string;
  };
}
