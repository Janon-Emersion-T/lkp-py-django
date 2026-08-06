import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";

import {
  getQuotation,
  getQuotations,
} from "./api";
import type {
  QuotationFilters,
} from "./types";

const quotationRootKey = [
  "quotations",
] as const;

export const quotationQueryKeys = {
  all: quotationRootKey,

  list: (
    filters: QuotationFilters,
  ) => [
    ...quotationRootKey,
    "list",
    filters,
  ] as const,

  detail: (
    quotationId: string,
  ) => [
    ...quotationRootKey,
    "detail",
    quotationId,
  ] as const,
};

export function useQuotations(
  filters: QuotationFilters,
) {
  return useQuery({
    queryKey:
      quotationQueryKeys.list(filters),
    queryFn: () =>
      getQuotations(filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useQuotation(
  quotationId: string | null,
) {
  return useQuery({
    queryKey:
      quotationQueryKeys.detail(
        quotationId ?? "not-selected",
      ),
    queryFn: () => {
      if (!quotationId) {
        throw new Error(
          "A quotation ID is required.",
        );
      }

      return getQuotation(quotationId);
    },
    enabled: Boolean(quotationId),
    staleTime: 30_000,
  });
}
