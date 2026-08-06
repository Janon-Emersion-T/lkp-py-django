import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";

import {
  getAccounts,
  getExpenses,
  getFinanceSummary,
  getInvoice,
  getInvoices,
  getPayments,
  getTransactions,
} from "./api";
import type {
  AccountFilters,
  SimplePagination,
  TransactionFilters,
} from "./types";

const financeRootKey = [
  "finance",
] as const;

export const financeQueryKeys = {
  all: financeRootKey,

  summary: [
    ...financeRootKey,
    "summary",
  ] as const,

  accounts: (
    filters: AccountFilters,
  ) => [
    ...financeRootKey,
    "accounts",
    filters,
  ] as const,

  transactions: (
    filters: TransactionFilters,
  ) => [
    ...financeRootKey,
    "transactions",
    filters,
  ] as const,

  invoices: (
    pagination: SimplePagination,
  ) => [
    ...financeRootKey,
    "invoices",
    pagination,
  ] as const,

  invoice: (
    invoiceId: string,
  ) => [
    ...financeRootKey,
    "invoice",
    invoiceId,
  ] as const,

  payments: (
    pagination: SimplePagination,
  ) => [
    ...financeRootKey,
    "payments",
    pagination,
  ] as const,

  expenses: (
    pagination: SimplePagination,
  ) => [
    ...financeRootKey,
    "expenses",
    pagination,
  ] as const,
};

export function useFinanceSummary() {
  return useQuery({
    queryKey: financeQueryKeys.summary,
    queryFn: getFinanceSummary,
    staleTime: 30_000,
  });
}

export function useFinanceAccounts(
  filters: AccountFilters,
) {
  return useQuery({
    queryKey:
      financeQueryKeys.accounts(filters),
    queryFn: () => getAccounts(filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useFinanceTransactions(
  filters: TransactionFilters,
) {
  return useQuery({
    queryKey:
      financeQueryKeys.transactions(filters),
    queryFn: () =>
      getTransactions(filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useFinanceInvoices(
  pagination: SimplePagination,
) {
  return useQuery({
    queryKey:
      financeQueryKeys.invoices(
        pagination,
      ),
    queryFn: () =>
      getInvoices(pagination),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useFinanceInvoice(
  invoiceId: string | null,
) {
  return useQuery({
    queryKey: financeQueryKeys.invoice(
      invoiceId ?? "not-selected",
    ),
    queryFn: () => {
      if (!invoiceId) {
        throw new Error(
          "An invoice ID is required.",
        );
      }

      return getInvoice(invoiceId);
    },
    enabled: Boolean(invoiceId),
    staleTime: 30_000,
  });
}

export function useFinancePayments(
  pagination: SimplePagination,
) {
  return useQuery({
    queryKey:
      financeQueryKeys.payments(
        pagination,
      ),
    queryFn: () =>
      getPayments(pagination),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useFinanceExpenses(
  pagination: SimplePagination,
) {
  return useQuery({
    queryKey:
      financeQueryKeys.expenses(
        pagination,
      ),
    queryFn: () =>
      getExpenses(pagination),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}
