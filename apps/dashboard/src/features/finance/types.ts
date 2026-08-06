export const accountTypes = [
  "asset",
  "liability",
  "equity",
  "income",
  "expense",
] as const;

export type AccountType =
  (typeof accountTypes)[number];

export const transactionTypes = [
  "income",
  "expense",
  "transfer",
  "adjustment",
] as const;

export type TransactionType =
  (typeof transactionTypes)[number];

export const invoiceStatuses = [
  "draft",
  "sent",
  "partially_paid",
  "paid",
  "overdue",
  "cancelled",
] as const;

export type InvoiceStatus =
  (typeof invoiceStatuses)[number];

export const paymentMethods = [
  "cash",
  "bank_transfer",
  "card",
  "paypal",
  "stripe",
  "crypto",
  "other",
] as const;

export type PaymentMethod =
  (typeof paymentMethods)[number];

export const paymentStatuses = [
  "pending",
  "completed",
  "failed",
  "refunded",
  "voided",
] as const;

export type PaymentStatus =
  (typeof paymentStatuses)[number];

export const expenseCategories = [
  "hosting",
  "office",
  "salary",
  "marketing",
  "software",
  "equipment",
  "miscellaneous",
] as const;

export type ExpenseCategory =
  (typeof expenseCategories)[number];

export const expenseStatuses = [
  "draft",
  "approved",
  "paid",
  "rejected",
  "voided",
] as const;

export type ExpenseStatus =
  (typeof expenseStatuses)[number];

export type FinanceSection =
  | "overview"
  | "accounts"
  | "transactions"
  | "invoices"
  | "payments"
  | "expenses";

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface FinanceSummary {
  total_assets: string;
  total_liabilities: string;
  total_equity: string;
  total_income: string;
  total_expenses: string;
  profit: string;
  receivables: string;
}

export interface FinanceAccount {
  id: string;
  account_code: string;
  name: string;
  account_type: AccountType;
  description: string;
  opening_balance: string;
  current_balance: string;
  currency: string;
  is_system: boolean;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface LedgerEntry {
  id: string;
  account_id: string;
  account_code: string;
  account_name: string;
  debit: string;
  credit: string;
  narration: string;
}

export interface FinanceTransaction {
  id: string;
  transaction_number: string;
  transaction_type: TransactionType;
  transaction_date: string;
  description: string;
  reference: string;
  total_amount: string;
  entries: LedgerEntry[];
  created_at: string;
}

export interface InvoiceItem {
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

export interface Invoice {
  id: string;
  invoice_number: string;
  client_id: string;
  client_name: string;
  project_id: string | null;
  quotation_id: string | null;
  status: InvoiceStatus;
  issue_date: string;
  due_date: string | null;
  currency: string;
  subtotal: string;
  discount_amount: string;
  tax_amount: string;
  total_amount: string;
  paid_amount: string;
  balance_due: string;
  notes: string;
  terms: string;
  sent_at: string | null;
  paid_at: string | null;
  items: InvoiceItem[];
  created_at: string;
  updated_at: string;
}

export interface Payment {
  id: string;
  payment_number: string;
  invoice_id: string | null;
  client_id: string | null;
  project_id: string | null;
  account_id: string;
  transaction_id: string | null;
  payment_date: string;
  amount: string;
  currency: string;
  method: PaymentMethod;
  status: PaymentStatus;
  reference: string;
  notes: string;
  created_at: string;
}

export interface Expense {
  id: string;
  expense_number: string;
  account_id: string;
  expense_account_id: string;
  project_id: string | null;
  transaction_id: string | null;
  expense_date: string;
  category: ExpenseCategory;
  status: ExpenseStatus;
  vendor: string;
  description: string;
  amount: string;
  currency: string;
  reference: string;
  notes: string;
  created_at: string;
}

export interface PaginatedAccounts {
  items: FinanceAccount[];
  pagination: PaginationMeta;
}

export interface PaginatedTransactions {
  items: FinanceTransaction[];
  pagination: PaginationMeta;
}

export interface PaginatedInvoices {
  items: Invoice[];
  pagination: PaginationMeta;
}

export interface PaginatedPayments {
  items: Payment[];
  pagination: PaginationMeta;
}

export interface PaginatedExpenses {
  items: Expense[];
  pagination: PaginationMeta;
}

export interface AccountFilters {
  page: number;
  pageSize: number;
  search: string;
  accountType: AccountType | "";
  isActive: boolean | null;
  ordering: string;
}

export interface TransactionFilters {
  page: number;
  pageSize: number;
  search: string;
  transactionType: TransactionType | "";
  ordering: string;
}

export interface SimplePagination {
  page: number;
  pageSize: number;
}
