import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  deleteCaseStudy,
  getCaseStudies,
  getCaseStudy,
  publishCaseStudy,
  scheduleCaseStudy,
} from "./api";
import type { CaseStudyFilters } from "./types";

export const caseStudiesQueryKeys = {
  all: ["case-studies"] as const,
  lists: () => ["case-studies", "list"] as const,
  list: (filters: CaseStudyFilters) =>
    [...caseStudiesQueryKeys.lists(), filters] as const,
  detail: (caseStudyId: string) =>
    ["case-studies", "detail", caseStudyId] as const,
};

export function useCaseStudies(filters: CaseStudyFilters) {
  return useQuery({
    queryKey: caseStudiesQueryKeys.list(filters),
    queryFn: () => getCaseStudies(filters),
  });
}

export function useCaseStudy(caseStudyId: string, enabled: boolean) {
  return useQuery({
    queryKey: caseStudiesQueryKeys.detail(caseStudyId),
    queryFn: () => getCaseStudy(caseStudyId),
    enabled,
  });
}

function useInvalidateCaseStudies() {
  const queryClient = useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey: caseStudiesQueryKeys.all,
    });
  };
}

export function usePublishCaseStudy() {
  const invalidate = useInvalidateCaseStudies();

  return useMutation({
    mutationFn: publishCaseStudy,
    onSuccess: invalidate,
  });
}

export function useScheduleCaseStudy() {
  const invalidate = useInvalidateCaseStudies();

  return useMutation({
    mutationFn: scheduleCaseStudy,
    onSuccess: invalidate,
  });
}

export function useDeleteCaseStudy() {
  const invalidate = useInvalidateCaseStudies();

  return useMutation({
    mutationFn: deleteCaseStudy,
    onSuccess: invalidate,
  });
}
