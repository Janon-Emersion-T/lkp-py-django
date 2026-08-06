import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";

import {
  getTask,
  getTasks,
} from "./api";
import type {
  TaskFilters,
} from "./types";

const taskRootKey = [
  "tasks",
] as const;

export const taskQueryKeys = {
  all: taskRootKey,

  list: (
    filters: TaskFilters,
  ) => [
    ...taskRootKey,
    "list",
    filters,
  ] as const,

  detail: (
    taskId: string,
  ) => [
    ...taskRootKey,
    "detail",
    taskId,
  ] as const,
};

export function useTasks(
  filters: TaskFilters,
) {
  return useQuery({
    queryKey:
      taskQueryKeys.list(filters),
    queryFn: () => getTasks(filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useTask(
  taskId: string | null,
) {
  return useQuery({
    queryKey: taskQueryKeys.detail(
      taskId ?? "not-selected",
    ),
    queryFn: () => {
      if (!taskId) {
        throw new Error(
          "A task ID is required.",
        );
      }

      return getTask(taskId);
    },
    enabled: Boolean(taskId),
    staleTime: 30_000,
  });
}
