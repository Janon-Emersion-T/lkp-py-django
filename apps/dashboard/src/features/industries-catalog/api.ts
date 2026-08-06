import { apiRequest } from "../../lib/http";
import {
  catalogIndustrySchema,
  messageSchema,
  paginatedIndustriesSchema,
} from "./schemas";
import type {
  CatalogIndustry,
  IndustryFilters,
  IndustrySchedulePayload,
  PaginatedIndustries,
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

  params.set(key, String(state === trueState));
}

function buildQuery(filters: IndustryFilters): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set("page_size", String(filters.pageSize));

  if (filters.search.trim()) {
    params.set("search", filters.search.trim());
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  addBooleanFilter(params, "is_featured", filters.featuredState, "featured");

  addBooleanFilter(params, "is_active", filters.activeState, "active");

  if (filters.ordering) {
    params.set("ordering", filters.ordering);
  }

  return params.toString();
}

export async function getIndustries(
  filters: IndustryFilters,
): Promise<PaginatedIndustries> {
  const response = await apiRequest<unknown>(
    `/industries?${buildQuery(filters)}`,
  );

  return paginatedIndustriesSchema.parse(response);
}

export async function getIndustry(
  industryId: string,
): Promise<CatalogIndustry> {
  const response = await apiRequest<unknown>(`/industries/${industryId}`);

  return catalogIndustrySchema.parse(response);
}

export async function publishIndustry(
  industryId: string,
): Promise<CatalogIndustry> {
  const response = await apiRequest<unknown>(
    `/industries/${industryId}/publish`,
    {
      method: "POST",
    },
  );

  return catalogIndustrySchema.parse(response);
}

export async function scheduleIndustry({
  industryId,
  payload,
}: {
  industryId: string;
  payload: IndustrySchedulePayload;
}): Promise<CatalogIndustry> {
  const response = await apiRequest<unknown>(
    `/industries/${industryId}/schedule`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return catalogIndustrySchema.parse(response);
}

export async function deleteIndustry(industryId: string): Promise<string> {
  const response = await apiRequest<unknown>(`/industries/${industryId}`, {
    method: "DELETE",
  });

  return messageSchema.parse(response).message;
}
