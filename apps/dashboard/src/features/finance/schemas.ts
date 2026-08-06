import {
  z,
} from "zod";

import {
  accountTypes,
  expenseCategories,
  expenseStatuses,
  invoiceStatuses,
  paymentMethods,
  paymentStatuses,
  transactionTypes,
} from "./types";

const paginationSchema = z.object({
  page: z.number().int(),
  page_size: z.number().int(),
  total_items: z.number().int().nonnegative(),
  total_pages: z.number().int().nonnegative(),
});

export const financeSummarySchema = z.object({
  total_assets: z.string(),
  total_liabilities: z.string(),
  total_equity: z.string(),
  total_income: z.string(),
  total_expenses: z.string(),
  profit: z.string(),
  receivables: z.string(),
});

export const financeAccountSchema = z.object({
  id: z.string().uuid(),
  account_code: z.string(),
  name: z.string(),
  account_type: z.enum(accountTypes),
  description: z.string(),
  opening_balance: z.string(),
  current_balance: z.string(),
  currency: z.string(),
  is_system: z.boolean(),
  is_active: z.boolean(),
  created_at: z.string(),
  updated_at: z.string(),
});

const ledgerEntrySchema = z.object({
  id: z.string().uuid(),
  account_id: z.string().uuid(),
  account_code: z.string(),
  account_name: z.string(),
  debit: z.string(),
  credit: z.string(),
  narration: z.string(),
});

export const transactionSchema = z.object({
  id: z.string().uuid(),
  transaction_number: z.string(),
  transaction_type: z.enum(transactionTypes),
  transaction_date: z.string(),
  description: z.string(),
  reference: z.string(),
  total_amount: z.string(),
  entries: z.array(ledgerEntrySchema),
  created_at: z.string(),
});

const invoiceItemSchema = z.object({
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
  sort_order: z.number().int(),
});

export const invoiceSchema = z.object({
  id: z.string().uuid(),
  invoice_number: z.string(),
  client_id: z.string().uuid(),
  client_name: z.string(),
  project_id: z.string().uuid().nullable(),
  quotation_id: z.string().uuid().nullable(),
  status: z.enum(invoiceStatuses),
  issue_date: z.string(),
  due_date: z.string().nullable(),
  currency: z.string(),
  subtotal: z.string(),
  discount_amount: z.string(),
  tax_amount: z.string(),
  total_amount: z.string(),
  paid_amount: z.string(),
  balance_due: z.string(),
  notes: z.string(),
  terms: z.string(),
  sent_at: z.string().nullable(),
  paid_at: z.string().nullable(),
  items: z.array(invoiceItemSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paymentSchema = z.object({
  id: z.string().uuid(),
  payment_number: z.string(),
  invoice_id: z.string().uuid().nullable(),
  client_id: z.string().uuid().nullable(),
  project_id: z.string().uuid().nullable(),
  account_id: z.string().uuid(),
  transaction_id: z.string().uuid().nullable(),
  payment_date: z.string(),
  amount: z.string(),
  currency: z.string(),
  method: z.enum(paymentMethods),
  status: z.enum(paymentStatuses),
  reference: z.string(),
  notes: z.string(),
  created_at: z.string(),
});

export const expenseSchema = z.object({
  id: z.string().uuid(),
  expense_number: z.string(),
  account_id: z.string().uuid(),
  expense_account_id: z.string().uuid(),
  project_id: z.string().uuid().nullable(),
  transaction_id: z.string().uuid().nullable(),
  expense_date: z.string(),
  category: z.enum(expenseCategories),
  status: z.enum(expenseStatuses),
  vendor: z.string(),
  description: z.string(),
  amount: z.string(),
  currency: z.string(),
  reference: z.string(),
  notes: z.string(),
  created_at: z.string(),
});

export const paginatedAccountsSchema = z.object({
  items: z.array(financeAccountSchema),
  pagination: paginationSchema,
});

export const paginatedTransactionsSchema = z.object({
  items: z.array(transactionSchema),
  pagination: paginationSchema,
});

export const paginatedInvoicesSchema = z.object({
  items: z.array(invoiceSchema),
  pagination: paginationSchema,
});

export const paginatedPaymentsSchema = z.object({
  items: z.array(paymentSchema),
  pagination: paginationSchema,
});

export const paginatedExpensesSchema = z.object({
  items: z.array(expenseSchema),
  pagination: paginationSchema,
});
