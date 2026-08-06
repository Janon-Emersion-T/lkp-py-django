import {
  apiRequest,
} from "../../lib/http";
import {
  paginatedTasksSchema,
  taskSchema,
} from "./schemas";
import type {
  PaginatedTasks,
  Task,
  TaskFilters,
} from "./types";

function buildTaskQueryString(
  filters: TaskFilters,
): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set(
    "page_size",
    String(filters.pageSize),
  );
  params.set("ordering", filters.ordering);

  const search = filters.search.trim();
  const projectId = filters.projectId.trim();
  const milestoneId =
    filters.milestoneId.trim();
  const assigneeId =
    filters.assigneeId.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.priority) {
    params.set("priority", filters.priority);
  }

  if (projectId) {
    params.set("project_id", projectId);
  }

  if (milestoneId) {
    params.set(
      "milestone_id",
      milestoneId,
    );
  }

  if (assigneeId) {
    params.set(
      "assignee_id",
      assigneeId,
    );
  }

  return params.toString();
}

export async function getTasks(
  filters: TaskFilters,
): Promise<PaginatedTasks> {
  const queryString =
    buildTaskQueryString(filters);

  const response = await apiRequest<unknown>(
    `/tasks?${queryString}`,
  );

  return paginatedTasksSchema.parse(
    response,
  );
}

export async function getTask(
  taskId: string,
): Promise<Task> {
  const response = await apiRequest<unknown>(
    `/tasks/${taskId}`,
  );

  return taskSchema.parse(response);
}
