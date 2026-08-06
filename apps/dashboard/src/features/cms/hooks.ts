import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";

import {
  getCmsRecord,
  getCmsRecords,
} from "./api";
import type {
  CmsContentType,
  CmsFilters,
} from "./types";

const cmsRootKey = [
  "cms",
] as const;

export const cmsQueryKeys = {
  all: cmsRootKey,

  list: (
    type: CmsContentType,
    filters: CmsFilters,
  ) => [
    ...cmsRootKey,
    type,
    "list",
    filters,
  ] as const,

  detail: (
    type: CmsContentType,
    id: string,
  ) => [
    ...cmsRootKey,
    type,
    "detail",
    id,
  ] as const,
};

export function useCmsRecords(
  type: CmsContentType,
  filters: CmsFilters,
) {
  return useQuery({
    queryKey: cmsQueryKeys.list(
      type,
      filters,
    ),
    queryFn: () =>
      getCmsRecords(type, filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useCmsRecord(
  type: CmsContentType,
  id: string | null,
) {
  return useQuery({
    queryKey: cmsQueryKeys.detail(
      type,
      id ?? "not-selected",
    ),
    queryFn: () => {
      if (!id) {
        throw new Error(
          "A content ID is required.",
        );
      }

      return getCmsRecord(type, id);
    },
    enabled: Boolean(id),
    staleTime: 30_000,
  });
}
