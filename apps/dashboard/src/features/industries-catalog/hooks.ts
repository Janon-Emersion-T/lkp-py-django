import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  deleteIndustry,
  getIndustries,
  getIndustry,
  publishIndustry,
  scheduleIndustry,
} from "./api";
import type { IndustryFilters } from "./types";

export const industriesCatalogQueryKeys = {
  all: ["industries-catalog"] as const,
  lists: () => ["industries-catalog", "list"] as const,
  list: (filters: IndustryFilters) =>
    [...industriesCatalogQueryKeys.lists(), filters] as const,
  detail: (industryId: string) =>
    ["industries-catalog", "detail", industryId] as const,
};

export function useIndustriesCatalog(filters: IndustryFilters) {
  return useQuery({
    queryKey: industriesCatalogQueryKeys.list(filters),
    queryFn: () => getIndustries(filters),
  });
}

export function useCatalogIndustry(industryId: string, enabled: boolean) {
  return useQuery({
    queryKey: industriesCatalogQueryKeys.detail(industryId),
    queryFn: () => getIndustry(industryId),
    enabled,
  });
}

function useInvalidateIndustriesCatalog() {
  const queryClient = useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey: industriesCatalogQueryKeys.all,
    });
  };
}

export function usePublishIndustry() {
  const invalidate = useInvalidateIndustriesCatalog();

  return useMutation({
    mutationFn: publishIndustry,
    onSuccess: invalidate,
  });
}

export function useScheduleIndustry() {
  const invalidate = useInvalidateIndustriesCatalog();

  return useMutation({
    mutationFn: scheduleIndustry,
    onSuccess: invalidate,
  });
}

export function useDeleteIndustry() {
  const invalidate = useInvalidateIndustriesCatalog();

  return useMutation({
    mutationFn: deleteIndustry,
    onSuccess: invalidate,
  });
}
