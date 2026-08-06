import { apiRequest } from "../../lib/http";
import {
  catalogPackageSchema,
  messageSchema,
  paginatedPackagesSchema,
} from "./schemas";
import type {
  CatalogPackage,
  PackageFilters,
  PackageSchedulePayload,
  PaginatedPackages,
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

function buildQuery(filters: PackageFilters): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set("page_size", String(filters.pageSize));

  if (filters.search.trim()) {
    params.set("search", filters.search.trim());
  }

  if (filters.category) {
    params.set("category", filters.category);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.currency.trim()) {
    params.set("currency", filters.currency.trim().toUpperCase());
  }

  if (filters.billingCycle) {
    params.set("billing_cycle", filters.billingCycle);
  }

  addBooleanFilter(params, "is_featured", filters.featuredState, "featured");

  addBooleanFilter(params, "is_popular", filters.popularState, "popular");

  addBooleanFilter(params, "is_active", filters.activeState, "active");

  if (filters.ordering) {
    params.set("ordering", filters.ordering);
  }

  return params.toString();
}

export async function getPackages(
  filters: PackageFilters,
): Promise<PaginatedPackages> {
  const response = await apiRequest<unknown>(
    `/packages?${buildQuery(filters)}`,
  );

  return paginatedPackagesSchema.parse(response);
}

export async function getPackage(packageId: string): Promise<CatalogPackage> {
  const response = await apiRequest<unknown>(`/packages/${packageId}`);

  return catalogPackageSchema.parse(response);
}

export async function publishPackage(
  packageId: string,
): Promise<CatalogPackage> {
  const response = await apiRequest<unknown>(`/packages/${packageId}/publish`, {
    method: "POST",
  });

  return catalogPackageSchema.parse(response);
}

export async function schedulePackage({
  packageId,
  payload,
}: {
  packageId: string;
  payload: PackageSchedulePayload;
}): Promise<CatalogPackage> {
  const response = await apiRequest<unknown>(
    `/packages/${packageId}/schedule`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return catalogPackageSchema.parse(response);
}

export async function deletePackage(packageId: string): Promise<string> {
  const response = await apiRequest<unknown>(`/packages/${packageId}`, {
    method: "DELETE",
  });

  return messageSchema.parse(response).message;
}
