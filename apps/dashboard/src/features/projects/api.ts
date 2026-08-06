import {
  apiRequest,
} from "../../lib/http";
import {
  paginatedProjectsSchema,
  projectSchema,
} from "./schemas";
import type {
  PaginatedProjects,
  Project,
  ProjectFilters,
} from "./types";

function buildProjectQueryString(
  filters: ProjectFilters,
): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set(
    "page_size",
    String(filters.pageSize),
  );
  params.set("ordering", filters.ordering);

  const search = filters.search.trim();
  const clientId = filters.clientId.trim();
  const managerId =
    filters.projectManagerId.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.priority) {
    params.set("priority", filters.priority);
  }

  if (clientId) {
    params.set("client_id", clientId);
  }

  if (managerId) {
    params.set(
      "project_manager_id",
      managerId,
    );
  }

  return params.toString();
}

export async function getProjects(
  filters: ProjectFilters,
): Promise<PaginatedProjects> {
  const queryString =
    buildProjectQueryString(filters);

  const response = await apiRequest<unknown>(
    `/projects?${queryString}`,
  );

  return paginatedProjectsSchema.parse(
    response,
  );
}

export async function getProject(
  projectId: string,
): Promise<Project> {
  const response = await apiRequest<unknown>(
    `/projects/${projectId}`,
  );

  return projectSchema.parse(response);
}
