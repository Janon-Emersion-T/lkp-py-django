import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  deleteService,
  getService,
  getServices,
  publishService,
  scheduleService,
} from "./api";
import type {
  ServiceFilters,
} from "./types";

export const servicesCatalogQueryKeys = {
  all: [
    "services-catalog",
  ] as const,
  lists: () => [
    "services-catalog",
    "list",
  ] as const,
  list: (
    filters: ServiceFilters,
  ) => [
    ...servicesCatalogQueryKeys.lists(),
    filters,
  ] as const,
  detail: (
    serviceId: string,
  ) => [
    "services-catalog",
    "detail",
    serviceId,
  ] as const,
};

export function useServicesCatalog(
  filters: ServiceFilters,
) {
  return useQuery({
    queryKey:
      servicesCatalogQueryKeys.list(
        filters,
      ),
    queryFn: () =>
      getServices(filters),
  });
}

export function useCatalogService(
  serviceId: string,
  enabled: boolean,
) {
  return useQuery({
    queryKey:
      servicesCatalogQueryKeys.detail(
        serviceId,
      ),
    queryFn: () =>
      getService(serviceId),
    enabled,
  });
}

function useInvalidateServicesCatalog() {
  const queryClient =
    useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey:
        servicesCatalogQueryKeys.all,
    });
  };
}

export function usePublishService() {
  const invalidate =
    useInvalidateServicesCatalog();

  return useMutation({
    mutationFn: publishService,
    onSuccess: invalidate,
  });
}

export function useScheduleService() {
  const invalidate =
    useInvalidateServicesCatalog();

  return useMutation({
    mutationFn: scheduleService,
    onSuccess: invalidate,
  });
}

export function useDeleteService() {
  const invalidate =
    useInvalidateServicesCatalog();

  return useMutation({
    mutationFn: deleteService,
    onSuccess: invalidate,
  });
}
