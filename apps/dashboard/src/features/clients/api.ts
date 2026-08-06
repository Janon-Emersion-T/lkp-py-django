import {
  apiRequest,
} from "../../lib/http";
import {
  clientSchema,
  paginatedClientsSchema,
} from "./schemas";
import type {
  Client,
  ClientFilters,
  PaginatedClients,
} from "./types";

function buildClientQueryString(
  filters: ClientFilters,
): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set(
    "page_size",
    String(filters.pageSize),
  );
  params.set("ordering", filters.ordering);

  const search = filters.search.trim();
  const country = filters.country.trim();
  const industry = filters.industry.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.clientType) {
    params.set(
      "client_type",
      filters.clientType,
    );
  }

  if (country) {
    params.set("country", country);
  }

  if (industry) {
    params.set("industry", industry);
  }

  return params.toString();
}

export async function getClients(
  filters: ClientFilters,
): Promise<PaginatedClients> {
  const queryString =
    buildClientQueryString(filters);

  const response = await apiRequest<unknown>(
    `/clients?${queryString}`,
  );

  return paginatedClientsSchema.parse(
    response,
  );
}

export async function getClient(
  clientId: string,
): Promise<Client> {
  const response = await apiRequest<unknown>(
    `/clients/${clientId}`,
  );

  return clientSchema.parse(response);
}
