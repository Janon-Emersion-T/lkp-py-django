import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";

import {
  getProject,
  getProjects,
} from "./api";
import type {
  ProjectFilters,
} from "./types";

const projectsRootKey = [
  "projects",
] as const;

export const projectQueryKeys = {
  all: projectsRootKey,

  list: (
    filters: ProjectFilters,
  ) => [
    ...projectsRootKey,
    "list",
    filters,
  ] as const,

  detail: (
    projectId: string,
  ) => [
    ...projectsRootKey,
    "detail",
    projectId,
  ] as const,
};

export function useProjects(
  filters: ProjectFilters,
) {
  return useQuery({
    queryKey:
      projectQueryKeys.list(filters),
    queryFn: () => getProjects(filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useProject(
  projectId: string | null,
) {
  return useQuery({
    queryKey: projectQueryKeys.detail(
      projectId ?? "not-selected",
    ),
    queryFn: () => {
      if (!projectId) {
        throw new Error(
          "A project ID is required.",
        );
      }

      return getProject(projectId);
    },
    enabled: Boolean(projectId),
    staleTime: 30_000,
  });
}
