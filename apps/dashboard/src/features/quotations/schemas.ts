import {
  z,
} from "zod";

import {
  quotationStatuses,
} from "./types";

const quotationItemSchema = z.object({
  id: z.string().uuid(),
  title: z.string(),
  description: z.string(),
  quantity: z.string(),
  unit_price: z.string(),
  discount_amount: z.string(),
  tax_rate: z.string(),
  subtotal: z.string(),
  tax_amount: z.string(),
  total_amount: z.string(),
  sort_order: z.number().int().nonnegative(),
});

const quotationRecipientSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  email: z.string(),
  is_primary: z.boolean(),
  received_at: z.string().nullable(),
  viewed_at: z.string().nullable(),
});

const quotationEventSchema = z.object({
  id: z.string().uuid(),
  event_type: z.string(),
  description: z.string(),
  metadata: z.record(
    z.string(),
    z.unknown(),
  ),
  created_at: z.string(),
});

export const quotationSchema = z.object({
  id: z.string().uuid(),
  quotation_number: z.string(),
  client_id: z.string().uuid(),
  client_name: z.string(),
  lead_id: z.string().uuid().nullable(),
  title: z.string(),
  subject: z.string(),
  description: z.string(),
  status: z.enum(quotationStatuses),
  issue_date: z.string(),
  expiry_date: z.string().nullable(),
  currency: z.string(),
  subtotal: z.string(),
  discount_amount: z.string(),
  tax_amount: z.string(),
  total_amount: z.string(),
  terms: z.string(),
  notes: z.string(),
  accepted_at: z.string().nullable(),
  accepted_by_name: z.string(),
  accepted_by_email: z.string(),
  sent_at: z.string().nullable(),
  duplicated_from_id: z.string().uuid().nullable(),
  is_expired: z.boolean(),
  items: z.array(quotationItemSchema),
  recipients: z.array(
    quotationRecipientSchema,
  ),
  events: z.array(quotationEventSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedQuotationsSchema =
  z.object({
    items: z.array(quotationSchema),
    pagination: z.object({
      page: z.number().int().positive(),
      page_size: z.number().int().positive(),
      total_items: z.number().int().nonnegative(),
      total_pages: z.number().int().nonnegative(),
    }),
  });
