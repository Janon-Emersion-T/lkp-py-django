export const dashboardPeriodPresets = [
  "today",
  "this_week",
  "this_month",
  "this_quarter",
  "this_year",
  "last_7_days",
  "last_30_days",
  "last_90_days",
  "custom",
] as const;

export type DashboardPeriodPreset =
  (typeof dashboardPeriodPresets)[number];

export interface DashboardQuery {
  preset: DashboardPeriodPreset;
  dateFrom?: string;
  dateTo?: string;
  environment?: string;
}

export interface DashboardPeriod {
  preset: DashboardPeriodPreset;
  date_from: string;
  date_to: string;
  datetime_from: string;
  datetime_to: string;
}

export interface CurrencyAmount {
  currency: string;
  amount: string | number;
}

export interface AccountBalance {
  id: string | number;
  name: string;
  currency: string;
  current_balance: string | number;
}

export interface ExecutiveSummary {
  total_clients: number;
  active_clients: number;
  total_leads: number;
  qualified_leads: number;
  won_leads: number;
  lost_leads: number;
  lead_conversion_rate: number;
  open_enquiries: number;
  overdue_follow_ups: number;
}

export interface ClientMetrics {
  total_clients: number;
  active_clients: number;
  new_clients: number;
}

export interface CrmMetrics {
  total_leads: number;
  qualified_leads: number;
  won_leads: number;
  lost_leads: number;
  overdue_follow_ups: number;
  period_leads: number;
  lead_conversion_rate: number;
}

export interface SalesMetrics {
  total_quotations: number;
  accepted_quotations: number;
  period_quotations: number;
  quotation_value_by_currency: CurrencyAmount[];
  accepted_quotation_value_by_currency: CurrencyAmount[];
}

export interface ProjectMetrics {
  active_projects: number;
  completed_projects: number;
  overdue_projects: number;
  completed_in_period: number;
}

export interface TaskMetrics {
  open_tasks: number;
  overdue_tasks: number;
  completed_tasks: number;
  completed_in_period: number;
}

export interface FinanceMetrics {
  outstanding_invoices: number;
  overdue_invoices: number;
  outstanding_value_by_currency: CurrencyAmount[];
  overdue_value_by_currency: CurrencyAmount[];
  revenue_by_currency: CurrencyAmount[];
  cash_and_bank_balances: AccountBalance[];
}

export interface EnquiryBreakdown {
  open_count: number;
  overdue_follow_ups: number;
  submitted_in_period: number;
}

export interface EnquiryMetrics {
  open_enquiries: number;
  overdue_follow_ups: number;
  submitted_in_period: number;
  contact_enquiries: EnquiryBreakdown;
  quote_enquiries: EnquiryBreakdown;
}

export interface WorkforceMetrics {
  active_team_members: number;
  open_job_positions: number;
  open_job_listings: number;
  newsletter_subscribers: number;
}

export interface ExecutiveDashboardData {
  clients: ClientMetrics;
  crm: CrmMetrics;
  sales: SalesMetrics;
  projects: ProjectMetrics;
  tasks: TaskMetrics;
  finance: FinanceMetrics;
  enquiries: EnquiryMetrics;
  workforce: WorkforceMetrics;
  summary: ExecutiveSummary;
}

export interface DashboardReportMetadata {
  foundation: boolean;
  aggregation_status: string;
}

export interface ExecutiveDashboardReport {
  report_type: "executive";
  environment: string;
  period: DashboardPeriod;
  generated_at: string;
  timezone: string;
  schema_version: number;
  data: ExecutiveDashboardData;
  metadata: DashboardReportMetadata;
}
