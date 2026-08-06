export const clientStatuses = [
  "prospect",
  "active",
  "inactive",
  "suspended",
  "archived",
] as const;

export type ClientStatus =
  (typeof clientStatuses)[number];

export const clientTypes = [
  "company",
  "individual",
  "non_profit",
  "government",
] as const;

export type ClientType =
  (typeof clientTypes)[number];

export const clientOrderingOptions = [
  "company_name",
  "-company_name",
  "client_code",
  "-client_code",
  "created_at",
  "-created_at",
  "updated_at",
  "-updated_at",
  "country",
  "-country",
  "industry",
  "-industry",
] as const;

export type ClientOrdering =
  (typeof clientOrderingOptions)[number];

export interface ClientContact {
  id: string;
  first_name: string;
  last_name: string;
  position: string;
  department: string;
  email: string;
  phone: string;
  whatsapp: string;
  is_primary: boolean;
  receives_quotations: boolean;
  receives_invoices: boolean;
  receives_project_updates: boolean;
  notes: string;
  created_at: string;
}

export interface ClientWebsite {
  id: string;
  name: string;
  url: string;
  platform: string;
  admin_url: string;
  is_primary: boolean;
  is_active: boolean;
  notes: string;
  created_at: string;
}

export interface Client {
  id: string;
  client_code: string;
  company_name: string;
  legal_name: string;
  client_type: ClientType;
  status: ClientStatus;
  industry: string;
  country: string;
  timezone: string;
  email: string;
  phone: string;
  whatsapp: string;
  website: string;
  tax_number: string;
  registration_number: string;
  billing_address: string;
  shipping_address: string;
  default_currency: string;
  payment_terms_days: number;
  notes: string;
  tags: string[];
  source_lead_id: string | null;
  contacts: ClientContact[];
  websites: ClientWebsite[];
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedClients {
  items: Client[];
  pagination: PaginationMeta;
}

export interface ClientFilters {
  page: number;
  pageSize: number;
  search: string;
  status: ClientStatus | "";
  clientType: ClientType | "";
  country: string;
  industry: string;
  ordering: ClientOrdering;
}
