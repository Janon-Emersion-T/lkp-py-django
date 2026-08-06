import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  deleteInsight,
  getInsight,
  getInsightCategories,
  getInsights,
  getInsightTags,
  publishInsight,
  scheduleInsight,
} from "./api";
import type { InsightFilters } from "./types";

export const insightsQueryKeys = {
  all: ["insights"] as const,
  lists: () => ["insights", "list"] as const,
  list: (filters: InsightFilters) =>
    [...insightsQueryKeys.lists(), filters] as const,
  detail: (articleId: string) => ["insights", "detail", articleId] as const,
  categories: ["insights", "categories"] as const,
  tags: ["insights", "tags"] as const,
};

export function useInsights(filters: InsightFilters) {
  return useQuery({
    queryKey: insightsQueryKeys.list(filters),
    queryFn: () => getInsights(filters),
  });
}

export function useInsight(articleId: string, enabled: boolean) {
  return useQuery({
    queryKey: insightsQueryKeys.detail(articleId),
    queryFn: () => getInsight(articleId),
    enabled,
  });
}

export function useInsightCategories() {
  return useQuery({
    queryKey: insightsQueryKeys.categories,
    queryFn: getInsightCategories,
  });
}

export function useInsightTags() {
  return useQuery({
    queryKey: insightsQueryKeys.tags,
    queryFn: getInsightTags,
  });
}

function useInvalidateInsights() {
  const queryClient = useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey: insightsQueryKeys.all,
    });
  };
}

export function usePublishInsight() {
  const invalidate = useInvalidateInsights();

  return useMutation({
    mutationFn: publishInsight,
    onSuccess: invalidate,
  });
}

export function useScheduleInsight() {
  const invalidate = useInvalidateInsights();

  return useMutation({
    mutationFn: scheduleInsight,
    onSuccess: invalidate,
  });
}

export function useDeleteInsight() {
  const invalidate = useInvalidateInsights();

  return useMutation({
    mutationFn: deleteInsight,
    onSuccess: invalidate,
  });
}
