export const quotationStatuses = [
  "draft",
  "sent",
  "viewed",
  "accepted",
  "rejected",
  "expired",
  "cancelled",
] as const;

export type QuotationStatus =
  (typeof quotationStatuses)[number];

export const quotationOrderingOptions = [
  "-created_at",
  "created_at",
  "quotation_number",
  "-quotation_number",
  "issue_date",
  "-issue_date",
  "expiry_date",
  "-expiry_date",
  "total_amount",
  "-total_amount",
  "status",
  "-status",
  "updated_at",
  "-updated_at",
] as const;

export type QuotationOrdering =
  (typeof quotationOrderingOptions)[number];

export interface QuotationItem {
  id: string;
  title: string;
  description: string;
  quantity: string;
  unit_price: string;
  discount_amount: string;
  tax_rate: string;
  subtotal: string;
  tax_amount: string;
  total_amount: string;
  sort_order: number;
}

export interface QuotationRecipient {
  id: string;
  name: string;
  email: string;
  is_primary: boolean;
  received_at: string | null;
  viewed_at: string | null;
}

export interface QuotationEvent {
  id: string;
  event_type: string;
  description: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface Quotation {
  id: string;
  quotation_number: string;
  client_id: string;
  client_name: string;
  lead_id: string | null;
  title: string;
  subject: string;
  description: string;
  status: QuotationStatus;
  issue_date: string;
  expiry_date: string | null;
  currency: string;
  subtotal: string;
  discount_amount: string;
  tax_amount: string;
  total_amount: string;
  terms: string;
  notes: string;
  accepted_at: string | null;
  accepted_by_name: string;
  accepted_by_email: string;
  sent_at: string | null;
  duplicated_from_id: string | null;
  is_expired: boolean;
  items: QuotationItem[];
  recipients: QuotationRecipient[];
  events: QuotationEvent[];
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedQuotations {
  items: Quotation[];
  pagination: PaginationMeta;
}

export interface QuotationFilters {
  page: number;
  pageSize: number;
  search: string;
  status: QuotationStatus | "";
  clientId: string;
  currency: string;
  ordering: QuotationOrdering;
}
