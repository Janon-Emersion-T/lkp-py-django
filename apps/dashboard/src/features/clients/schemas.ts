import {
  z,
} from "zod";

import {
  clientStatuses,
  clientTypes,
} from "./types";

const clientContactSchema = z.object({
  id: z.string().uuid(),
  first_name: z.string(),
  last_name: z.string(),
  position: z.string(),
  department: z.string(),
  email: z.string(),
  phone: z.string(),
  whatsapp: z.string(),
  is_primary: z.boolean(),
  receives_quotations: z.boolean(),
  receives_invoices: z.boolean(),
  receives_project_updates: z.boolean(),
  notes: z.string(),
  created_at: z.string(),
});

const clientWebsiteSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  url: z.string(),
  platform: z.string(),
  admin_url: z.string(),
  is_primary: z.boolean(),
  is_active: z.boolean(),
  notes: z.string(),
  created_at: z.string(),
});

export const clientSchema = z.object({
  id: z.string().uuid(),
  client_code: z.string(),
  company_name: z.string(),
  legal_name: z.string(),
  client_type: z.enum(clientTypes),
  status: z.enum(clientStatuses),
  industry: z.string(),
  country: z.string(),
  timezone: z.string(),
  email: z.string(),
  phone: z.string(),
  whatsapp: z.string(),
  website: z.string(),
  tax_number: z.string(),
  registration_number: z.string(),
  billing_address: z.string(),
  shipping_address: z.string(),
  default_currency: z.string(),
  payment_terms_days: z.number().int().nonnegative(),
  notes: z.string(),
  tags: z.array(z.string()),
  source_lead_id: z.string().uuid().nullable(),
  contacts: z.array(clientContactSchema),
  websites: z.array(clientWebsiteSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedClientsSchema = z.object({
  items: z.array(clientSchema),
  pagination: z.object({
    page: z.number().int().positive(),
    page_size: z.number().int().positive(),
    total_items: z.number().int().nonnegative(),
    total_pages: z.number().int().nonnegative(),
  }),
});
