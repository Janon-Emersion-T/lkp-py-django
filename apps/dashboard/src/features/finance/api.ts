import {
  apiRequest,
} from "../../lib/http";
import {
  financeSummarySchema,
  invoiceSchema,
  paginatedAccountsSchema,
  paginatedExpensesSchema,
  paginatedInvoicesSchema,
  paginatedPaymentsSchema,
  paginatedTransactionsSchema,
} from "./schemas";
import type {
  AccountFilters,
  FinanceSummary,
  Invoice,
  PaginatedAccounts,
  PaginatedExpenses,
  PaginatedInvoices,
  PaginatedPayments,
  PaginatedTransactions,
  SimplePagination,
  TransactionFilters,
} from "./types";

function paginationParams(
  pagination: SimplePagination,
): URLSearchParams {
  const params = new URLSearchParams();

  params.set(
    "page",
    String(pagination.page),
  );

  params.set(
    "page_size",
    String(pagination.pageSize),
  );

  return params;
}

export async function getFinanceSummary():
Promise<FinanceSummary> {
  const response = await apiRequest<unknown>(
    "/finance/summary",
  );

  return financeSummarySchema.parse(
    response,
  );
}

export async function getAccounts(
  filters: AccountFilters,
): Promise<PaginatedAccounts> {
  const params = paginationParams(filters);

  const search = filters.search.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.accountType) {
    params.set(
      "account_type",
      filters.accountType,
    );
  }

  if (filters.isActive !== null) {
    params.set(
      "is_active",
      String(filters.isActive),
    );
  }

  if (filters.ordering) {
    params.set(
      "ordering",
      filters.ordering,
    );
  }

  const response = await apiRequest<unknown>(
    `/finance/accounts?${params.toString()}`,
  );

  return paginatedAccountsSchema.parse(
    response,
  );
}

export async function getTransactions(
  filters: TransactionFilters,
): Promise<PaginatedTransactions> {
  const params = paginationParams(filters);

  const search = filters.search.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.transactionType) {
    params.set(
      "transaction_type",
      filters.transactionType,
    );
  }

  if (filters.ordering) {
    params.set(
      "ordering",
      filters.ordering,
    );
  }

  const response = await apiRequest<unknown>(
    `/finance/transactions?${params.toString()}`,
  );

  return paginatedTransactionsSchema.parse(
    response,
  );
}

export async function getInvoices(
  pagination: SimplePagination,
): Promise<PaginatedInvoices> {
  const params = paginationParams(pagination);

  const response = await apiRequest<unknown>(
    `/finance/invoices?${params.toString()}`,
  );

  return paginatedInvoicesSchema.parse(
    response,
  );
}

export async function getInvoice(
  invoiceId: string,
): Promise<Invoice> {
  const response = await apiRequest<unknown>(
    `/finance/invoices/${invoiceId}`,
  );

  return invoiceSchema.parse(response);
}

export async function getPayments(
  pagination: SimplePagination,
): Promise<PaginatedPayments> {
  const params = paginationParams(pagination);

  const response = await apiRequest<unknown>(
    `/finance/payments?${params.toString()}`,
  );

  return paginatedPaymentsSchema.parse(
    response,
  );
}

export async function getExpenses(
  pagination: SimplePagination,
): Promise<PaginatedExpenses> {
  const params = paginationParams(pagination);

  const response = await apiRequest<unknown>(
    `/finance/expenses?${params.toString()}`,
  );

  return paginatedExpensesSchema.parse(
    response,
  );
}
