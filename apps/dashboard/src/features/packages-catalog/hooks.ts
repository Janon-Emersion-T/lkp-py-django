import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  deletePackage,
  getPackage,
  getPackages,
  publishPackage,
  schedulePackage,
} from "./api";
import type { PackageFilters } from "./types";

export const packagesCatalogQueryKeys = {
  all: ["packages-catalog"] as const,
  lists: () => ["packages-catalog", "list"] as const,
  list: (filters: PackageFilters) =>
    [...packagesCatalogQueryKeys.lists(), filters] as const,
  detail: (packageId: string) =>
    ["packages-catalog", "detail", packageId] as const,
};

export function usePackagesCatalog(filters: PackageFilters) {
  return useQuery({
    queryKey: packagesCatalogQueryKeys.list(filters),
    queryFn: () => getPackages(filters),
  });
}

export function useCatalogPackage(packageId: string, enabled: boolean) {
  return useQuery({
    queryKey: packagesCatalogQueryKeys.detail(packageId),
    queryFn: () => getPackage(packageId),
    enabled,
  });
}

function useInvalidatePackagesCatalog() {
  const queryClient = useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey: packagesCatalogQueryKeys.all,
    });
  };
}

export function usePublishPackage() {
  const invalidate = useInvalidatePackagesCatalog();

  return useMutation({
    mutationFn: publishPackage,
    onSuccess: invalidate,
  });
}

export function useSchedulePackage() {
  const invalidate = useInvalidatePackagesCatalog();

  return useMutation({
    mutationFn: schedulePackage,
    onSuccess: invalidate,
  });
}

export function useDeletePackage() {
  const invalidate = useInvalidatePackagesCatalog();

  return useMutation({
    mutationFn: deletePackage,
    onSuccess: invalidate,
  });
}
