import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  generateSnapshot,
  getPublicPreview,
  getSnapshots,
  invalidateSnapshots,
  refreshAllSnapshots,
} from "./api";
import type {
  PreviewableSnapshotType,
  SnapshotFilters,
} from "./types";

export const snapshotQueryKeys = {
  all: [
    "public-website-snapshots",
  ] as const,
  lists: () => [
    ...snapshotQueryKeys.all,
    "list",
  ] as const,
  list: (
    filters: SnapshotFilters,
  ) => [
    ...snapshotQueryKeys.lists(),
    filters,
  ] as const,
  previews: () => [
    ...snapshotQueryKeys.all,
    "preview",
  ] as const,
  preview: (
    type: PreviewableSnapshotType,
    environment: string,
  ) => [
    ...snapshotQueryKeys.previews(),
    type,
    environment,
  ] as const,
};

export function useSnapshots(
  filters: SnapshotFilters,
) {
  return useQuery({
    queryKey:
      snapshotQueryKeys.list(filters),
    queryFn: () =>
      getSnapshots(filters),
  });
}

export function useSnapshotPreview(
  type: PreviewableSnapshotType,
  environment: string,
  enabled: boolean,
) {
  return useQuery({
    queryKey:
      snapshotQueryKeys.preview(
        type,
        environment,
      ),
    queryFn: () =>
      getPublicPreview(
        type,
        environment,
      ),
    enabled,
  });
}

function useSnapshotMutationInvalidation() {
  const queryClient =
    useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey:
        snapshotQueryKeys.all,
    });
  };
}

export function useGenerateSnapshot() {
  const invalidate =
    useSnapshotMutationInvalidation();

  return useMutation({
    mutationFn: generateSnapshot,
    onSuccess: invalidate,
  });
}

export function useInvalidateSnapshots() {
  const invalidate =
    useSnapshotMutationInvalidation();

  return useMutation({
    mutationFn: invalidateSnapshots,
    onSuccess: invalidate,
  });
}

export function useRefreshAllSnapshots() {
  const invalidate =
    useSnapshotMutationInvalidation();

  return useMutation({
    mutationFn: refreshAllSnapshots,
    onSuccess: invalidate,
  });
}
