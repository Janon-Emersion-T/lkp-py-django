import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  createMediaFolder,
  deleteMediaAsset,
  getMediaAsset,
  getMediaAssets,
  getMediaFolders,
  updateMediaAsset,
  uploadMediaAsset,
} from "./api";
import type {
  MediaFilters,
} from "./types";

export const mediaLibraryQueryKeys = {
  all: [
    "media-library",
  ] as const,
  folders: [
    "media-library",
    "folders",
  ] as const,
  assets: () => [
    "media-library",
    "assets",
  ] as const,
  assetList: (
    filters: MediaFilters,
  ) => [
    ...mediaLibraryQueryKeys.assets(),
    "list",
    filters,
  ] as const,
  asset: (assetId: string) => [
    ...mediaLibraryQueryKeys.assets(),
    "detail",
    assetId,
  ] as const,
};

export function useMediaFolders() {
  return useQuery({
    queryKey:
      mediaLibraryQueryKeys.folders,
    queryFn: getMediaFolders,
  });
}

export function useMediaAssets(
  filters: MediaFilters,
) {
  return useQuery({
    queryKey:
      mediaLibraryQueryKeys.assetList(
        filters,
      ),
    queryFn: () =>
      getMediaAssets(filters),
  });
}

export function useMediaAsset(
  assetId: string,
  enabled: boolean,
) {
  return useQuery({
    queryKey:
      mediaLibraryQueryKeys.asset(
        assetId,
      ),
    queryFn: () =>
      getMediaAsset(assetId),
    enabled,
  });
}

function useInvalidateMediaLibrary() {
  const queryClient =
    useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey:
        mediaLibraryQueryKeys.all,
    });
  };
}

export function useCreateMediaFolder() {
  const invalidate =
    useInvalidateMediaLibrary();

  return useMutation({
    mutationFn:
      createMediaFolder,
    onSuccess: invalidate,
  });
}

export function useUploadMediaAsset() {
  const invalidate =
    useInvalidateMediaLibrary();

  return useMutation({
    mutationFn:
      uploadMediaAsset,
    onSuccess: invalidate,
  });
}

export function useUpdateMediaAsset() {
  const invalidate =
    useInvalidateMediaLibrary();

  return useMutation({
    mutationFn:
      updateMediaAsset,
    onSuccess: invalidate,
  });
}

export function useDeleteMediaAsset() {
  const invalidate =
    useInvalidateMediaLibrary();

  return useMutation({
    mutationFn:
      deleteMediaAsset,
    onSuccess: invalidate,
  });
}
