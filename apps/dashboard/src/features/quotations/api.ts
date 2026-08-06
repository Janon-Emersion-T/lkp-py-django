import {
  apiRequest,
} from "../../lib/http";
import {
  paginatedQuotationsSchema,
  quotationSchema,
} from "./schemas";
import type {
  PaginatedQuotations,
  Quotation,
  QuotationFilters,
} from "./types";

function buildQuotationQueryString(
  filters: QuotationFilters,
): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set(
    "page_size",
    String(filters.pageSize),
  );
  params.set("ordering", filters.ordering);

  const search = filters.search.trim();
  const clientId = filters.clientId.trim();
  const currency = filters.currency
    .trim()
    .toUpperCase();

  if (search) {
    params.set("search", search);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (clientId) {
    params.set("client_id", clientId);
  }

  if (currency) {
    params.set("currency", currency);
  }

  return params.toString();
}

export async function getQuotations(
  filters: QuotationFilters,
): Promise<PaginatedQuotations> {
  const queryString =
    buildQuotationQueryString(filters);

  const response = await apiRequest<unknown>(
    `/quotations?${queryString}`,
  );

  return paginatedQuotationsSchema.parse(
    response,
  );
}

export async function getQuotation(
  quotationId: string,
): Promise<Quotation> {
  const response = await apiRequest<unknown>(
    `/quotations/${quotationId}`,
  );

  return quotationSchema.parse(response);
}
