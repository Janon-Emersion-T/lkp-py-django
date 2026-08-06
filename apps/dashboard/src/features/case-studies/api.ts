import { apiRequest } from "../../lib/http";
import {
  caseStudySchema,
  messageSchema,
  paginatedCaseStudiesSchema,
} from "./schemas";
import type {
  CaseStudy,
  CaseStudyFilters,
  CaseStudySchedulePayload,
  PaginatedCaseStudies,
} from "./types";

function addBooleanFilter(
  params: URLSearchParams,
  key: string,
  state: string,
  trueState: string,
) {
  if (state === "all") {
    return;
  }

  params.set(key, String(state === trueState));
}

function buildQuery(filters: CaseStudyFilters): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set("page_size", String(filters.pageSize));

  if (filters.search.trim()) {
    params.set("search", filters.search.trim());
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.clientId) {
    params.set("client_id", filters.clientId);
  }

  if (filters.projectId) {
    params.set("project_id", filters.projectId);
  }

  if (filters.industryId) {
    params.set("industry_id", filters.industryId);
  }

  if (filters.serviceId) {
    params.set("service_id", filters.serviceId);
  }

  addBooleanFilter(params, "is_featured", filters.featuredState, "featured");

  addBooleanFilter(params, "is_active", filters.activeState, "active");

  if (filters.ordering) {
    params.set("ordering", filters.ordering);
  }

  return params.toString();
}

export async function getCaseStudies(
  filters: CaseStudyFilters,
): Promise<PaginatedCaseStudies> {
  const response = await apiRequest<unknown>(
    `/case-studies?${buildQuery(filters)}`,
  );

  return paginatedCaseStudiesSchema.parse(response);
}

export async function getCaseStudy(caseStudyId: string): Promise<CaseStudy> {
  const response = await apiRequest<unknown>(`/case-studies/${caseStudyId}`);

  return caseStudySchema.parse(response);
}

export async function publishCaseStudy(
  caseStudyId: string,
): Promise<CaseStudy> {
  const response = await apiRequest<unknown>(
    `/case-studies/${caseStudyId}/publish`,
    {
      method: "POST",
    },
  );

  return caseStudySchema.parse(response);
}

export async function scheduleCaseStudy({
  caseStudyId,
  payload,
}: {
  caseStudyId: string;
  payload: CaseStudySchedulePayload;
}): Promise<CaseStudy> {
  const response = await apiRequest<unknown>(
    `/case-studies/${caseStudyId}/schedule`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return caseStudySchema.parse(response);
}

export async function deleteCaseStudy(caseStudyId: string): Promise<string> {
  const response = await apiRequest<unknown>(`/case-studies/${caseStudyId}`, {
    method: "DELETE",
  });

  return messageSchema.parse(response).message;
}
