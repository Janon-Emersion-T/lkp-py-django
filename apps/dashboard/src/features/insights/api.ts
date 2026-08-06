import { apiRequest } from "../../lib/http";
import {
  insightArticleSchema,
  insightCategorySchema,
  insightTagSchema,
  messageSchema,
  paginatedInsightsSchema,
} from "./schemas";
import type {
  InsightArticle,
  InsightCategory,
  InsightFilters,
  InsightSchedulePayload,
  InsightTag,
  PaginatedInsights,
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

function buildQuery(filters: InsightFilters): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set("page_size", String(filters.pageSize));

  if (filters.search.trim()) {
    params.set("search", filters.search.trim());
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.categoryId) {
    params.set("category_id", filters.categoryId);
  }

  if (filters.tagId) {
    params.set("tag_id", filters.tagId);
  }

  addBooleanFilter(params, "is_featured", filters.featuredState, "featured");

  addBooleanFilter(params, "is_active", filters.activeState, "active");

  if (filters.ordering) {
    params.set("ordering", filters.ordering);
  }

  return params.toString();
}

export async function getInsights(
  filters: InsightFilters,
): Promise<PaginatedInsights> {
  const response = await apiRequest<unknown>(
    `/insights?${buildQuery(filters)}`,
  );

  return paginatedInsightsSchema.parse(response);
}

export async function getInsight(articleId: string): Promise<InsightArticle> {
  const response = await apiRequest<unknown>(`/insights/${articleId}`);

  return insightArticleSchema.parse(response);
}

export async function getInsightCategories(): Promise<InsightCategory[]> {
  const response = await apiRequest<unknown>("/insights/categories");

  return insightCategorySchema.array().parse(response);
}

export async function getInsightTags(): Promise<InsightTag[]> {
  const response = await apiRequest<unknown>("/insights/tags");

  return insightTagSchema.array().parse(response);
}

export async function publishInsight(
  articleId: string,
): Promise<InsightArticle> {
  const response = await apiRequest<unknown>(`/insights/${articleId}/publish`, {
    method: "POST",
  });

  return insightArticleSchema.parse(response);
}

export async function scheduleInsight({
  articleId,
  payload,
}: {
  articleId: string;
  payload: InsightSchedulePayload;
}): Promise<InsightArticle> {
  const response = await apiRequest<unknown>(
    `/insights/${articleId}/schedule`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return insightArticleSchema.parse(response);
}

export async function deleteInsight(articleId: string): Promise<string> {
  const response = await apiRequest<unknown>(`/insights/${articleId}`, {
    method: "DELETE",
  });

  return messageSchema.parse(response).message;
}
