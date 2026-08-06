import {
  apiRequest,
} from "../../lib/http";
import {
  catalogServiceSchema,
  messageSchema,
  paginatedServicesSchema,
} from "./schemas";
import type {
  CatalogService,
  PaginatedServices,
  ServiceFilters,
  ServiceSchedulePayload,
} from "./types";

function addBooleanFilter(
  params: URLSearchParams,
  key: string,
  state: string,
  trueState: string,
) {
  if (state === "all") {
    return;
  }

  params.set(
    key,
    String(state === trueState),
  );
}

function buildQuery(
  filters: ServiceFilters,
): string {
  const params =
    new URLSearchParams();

  params.set(
    "page",
    String(filters.page),
  );

  params.set(
    "page_size",
    String(filters.pageSize),
  );

  if (filters.search.trim()) {
    params.set(
      "search",
      filters.search.trim(),
    );
  }

  if (filters.status) {
    params.set(
      "status",
      filters.status,
    );
  }

  addBooleanFilter(
    params,
    "is_featured",
    filters.featuredState,
    "featured",
  );

  addBooleanFilter(
    params,
    "is_active",
    filters.activeState,
    "active",
  );

  if (filters.ordering) {
    params.set(
      "ordering",
      filters.ordering,
    );
  }

  return params.toString();
}

export async function getServices(
  filters: ServiceFilters,
): Promise<PaginatedServices> {
  const response =
    await apiRequest<unknown>(
      `/services?${buildQuery(
        filters,
      )}`,
    );

  return paginatedServicesSchema.parse(
    response,
  );
}

export async function getService(
  serviceId: string,
): Promise<CatalogService> {
  const response =
    await apiRequest<unknown>(
      `/services/${serviceId}`,
    );

  return catalogServiceSchema.parse(
    response,
  );
}

export async function publishService(
  serviceId: string,
): Promise<CatalogService> {
  const response =
    await apiRequest<unknown>(
      `/services/${serviceId}/publish`,
      {
        method: "POST",
      },
    );

  return catalogServiceSchema.parse(
    response,
  );
}

export async function scheduleService({
  serviceId,
  payload,
}: {
  serviceId: string;
  payload: ServiceSchedulePayload;
}): Promise<CatalogService> {
  const response =
    await apiRequest<unknown>(
      `/services/${serviceId}/schedule`,
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );

  return catalogServiceSchema.parse(
    response,
  );
}

export async function deleteService(
  serviceId: string,
): Promise<string> {
  const response =
    await apiRequest<unknown>(
      `/services/${serviceId}`,
      {
        method: "DELETE",
      },
    );

  return messageSchema.parse(
    response,
  ).message;
}
