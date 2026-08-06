import { apiRequest } from "../../lib/http";
import {
  messageSchema,
  paginatedTestimonialsSchema,
  testimonialSchema,
} from "./schemas";
import type {
  PaginatedTestimonials,
  Testimonial,
  TestimonialFilters,
  TestimonialSchedulePayload,
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

function buildQuery(filters: TestimonialFilters): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set("page_size", String(filters.pageSize));

  if (filters.search.trim()) {
    params.set("search", filters.search.trim());
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.source) {
    params.set("source", filters.source);
  }

  if (filters.rating !== "") {
    params.set("rating", String(filters.rating));
  }

  addBooleanFilter(params, "is_featured", filters.featuredState, "featured");

  addBooleanFilter(params, "is_verified", filters.verifiedState, "verified");

  addBooleanFilter(params, "is_active", filters.activeState, "active");

  if (filters.clientId) {
    params.set("client_id", filters.clientId);
  }

  if (filters.projectId) {
    params.set("project_id", filters.projectId);
  }

  if (filters.ordering) {
    params.set("ordering", filters.ordering);
  }

  return params.toString();
}

export async function getTestimonials(
  filters: TestimonialFilters,
): Promise<PaginatedTestimonials> {
  const response = await apiRequest<unknown>(
    `/testimonials?${buildQuery(filters)}`,
  );

  return paginatedTestimonialsSchema.parse(response);
}

export async function getTestimonial(
  testimonialId: string,
): Promise<Testimonial> {
  const response = await apiRequest<unknown>(`/testimonials/${testimonialId}`);

  return testimonialSchema.parse(response);
}

export async function publishTestimonial(
  testimonialId: string,
): Promise<Testimonial> {
  const response = await apiRequest<unknown>(
    `/testimonials/${testimonialId}/publish`,
    {
      method: "POST",
    },
  );

  return testimonialSchema.parse(response);
}

export async function scheduleTestimonial({
  testimonialId,
  payload,
}: {
  testimonialId: string;
  payload: TestimonialSchedulePayload;
}): Promise<Testimonial> {
  const response = await apiRequest<unknown>(
    `/testimonials/${testimonialId}/schedule`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return testimonialSchema.parse(response);
}

export async function deleteTestimonial(
  testimonialId: string,
): Promise<string> {
  const response = await apiRequest<unknown>(`/testimonials/${testimonialId}`, {
    method: "DELETE",
  });

  return messageSchema.parse(response).message;
}
