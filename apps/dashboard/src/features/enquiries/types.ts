export const enquiryStatuses = [
  "new",
  "assigned",
  "contacted",
  "qualified",
  "proposal_sent",
  "won",
  "lost",
  "spam",
  "archived",
] as const;

export type EnquiryStatus = (typeof enquiryStatuses)[number];

export const enquiryPriorities = ["low", "normal", "high", "urgent"] as const;

export type EnquiryPriority = (typeof enquiryPriorities)[number];

export const enquirySources = [
  "website",
  "google",
  "facebook",
  "instagram",
  "linkedin",
  "tiktok",
  "whatsapp",
  "referral",
  "email",
  "phone",
  "manual",
  "other",
] as const;

export type EnquirySource = (typeof enquirySources)[number];

export type EnquiryKind = "contact" | "quote";

export interface EnquiryNote {
  id: string;
  author_id: string | null;
  author_name: string | null;
  note: string;
  is_private: boolean;
  created_at: string;
}

export interface BaseEnquiry {
  id: string;
  reference_code: string;
  name: string;
  email: string;
  phone: string;
  company_name: string;
  source: EnquirySource;
  source_url: string;
  status: EnquiryStatus;
  priority: EnquiryPriority;
  assigned_to_id: string | null;
  assigned_to_name: string | null;
  client_id: string | null;
  lead_id: string | null;
  submitted_at: string;
  first_contacted_at: string | null;
  resolved_at: string | null;
  last_follow_up_at: string | null;
  next_follow_up_at: string | null;
  internal_summary: string;
  loss_reason: string;
  metadata: Record<string, unknown>;
  notes: EnquiryNote[];
  created_at: string;
  updated_at: string;
}

export interface ContactEnquiry extends BaseEnquiry {
  subject: string;
  message: string;
}

export interface QuoteEnquiryService {
  id: string;
  service_id: string;
  service_title: string;
  notes: string;
  sort_order: number;
}

export interface QuoteEnquiry extends BaseEnquiry {
  country: string;
  website_url: string;
  project_title: string;
  project_description: string;
  preferred_package_id: string | null;
  budget_min: string | null;
  budget_max: string | null;
  budget_currency: string;
  desired_start_date: string | null;
  desired_completion_date: string | null;
  quotation_id: string | null;
  services: QuoteEnquiryService[];
}

export interface EnquiryDashboard {
  total_contact_enquiries: number;
  total_quote_enquiries: number;
  new_contact_enquiries: number;
  new_quote_enquiries: number;
  active_contact_enquiries: number;
  active_quote_enquiries: number;
  won_contact_enquiries: number;
  won_quote_enquiries: number;
  lost_contact_enquiries: number;
  lost_quote_enquiries: number;
  urgent_contact_enquiries: number;
  urgent_quote_enquiries: number;
  overdue_contact_follow_ups: number;
  overdue_quote_follow_ups: number;
  contact_enquiries_by_status: Record<string, number>;
  quote_enquiries_by_status: Record<string, number>;
  contact_enquiries_by_source: Record<string, number>;
  quote_enquiries_by_source: Record<string, number>;
}

export interface ContactEnquiryFilters {
  search: string;
  status: EnquiryStatus | "";
  priority: EnquiryPriority | "";
  source: EnquirySource | "";
  assignedToId: string;
  ordering: string;
}

export interface QuoteEnquiryFilters extends ContactEnquiryFilters {
  country: string;
  serviceId: string;
}

export interface EnquiryStatusPayload {
  status: EnquiryStatus;
  loss_reason: string;
}

export interface EnquiryAssignmentPayload {
  assigned_to_id: string | null;
  priority: EnquiryPriority;
  internal_summary: string;
  next_follow_up_at: string | null;
}

export interface EnquiryFollowUpPayload {
  next_follow_up_at: string | null;
}

export interface EnquiryNotePayload {
  note: string;
  is_private: boolean;
}
