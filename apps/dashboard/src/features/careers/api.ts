import { apiRequest } from "../../lib/http";
import {
  applicationNoteSchema,
  careersDashboardSchema,
  employmentTypeSchema,
  interviewSchema,
  jobApplicationSchema,
  jobDepartmentSchema,
  jobListingSchema,
  jobPositionSchema,
} from "./schemas";
import type {
  ApplicationFilters,
  ApplicationNote,
  ApplicationNotePayload,
  ApplicationReviewPayload,
  ApplicationStatusPayload,
  CareersDashboard,
  EmploymentType,
  Interview,
  InterviewFilters,
  JobApplication,
  JobDepartment,
  JobListing,
  JobPosition,
  ListingFilters,
  ListingSchedulePayload,
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

export async function getCareersDashboard(): Promise<CareersDashboard> {
  return careersDashboardSchema.parse(
    await apiRequest<unknown>("/careers/dashboard"),
  );
}

export async function getDepartments(): Promise<JobDepartment[]> {
  return jobDepartmentSchema
    .array()
    .parse(await apiRequest<unknown>("/careers/departments?is_active=true"));
}

export async function getEmploymentTypes(): Promise<EmploymentType[]> {
  return employmentTypeSchema
    .array()
    .parse(
      await apiRequest<unknown>("/careers/employment-types?is_active=true"),
    );
}

export async function getPositions(): Promise<JobPosition[]> {
  return jobPositionSchema
    .array()
    .parse(
      await apiRequest<unknown>(
        "/careers/positions?is_active=true&ordering=sort_order",
      ),
    );
}

export async function getListings(
  filters: ListingFilters,
): Promise<JobListing[]> {
  const params = new URLSearchParams();

  if (filters.search.trim()) {
    params.set("search", filters.search.trim());
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.departmentId) {
    params.set("department_id", filters.departmentId);
  }

  if (filters.employmentTypeId) {
    params.set("employment_type_id", filters.employmentTypeId);
  }

  addBooleanFilter(params, "is_featured", filters.featuredState, "featured");

  addBooleanFilter(params, "is_active", filters.activeState, "active");

  params.set("ordering", filters.ordering);

  return jobListingSchema
    .array()
    .parse(await apiRequest<unknown>(`/careers/listings?${params}`));
}

export async function publishListing(listingId: string): Promise<JobListing> {
  return jobListingSchema.parse(
    await apiRequest<unknown>(`/careers/listings/${listingId}/publish`, {
      method: "POST",
    }),
  );
}

export async function scheduleListing({
  listingId,
  payload,
}: {
  listingId: string;
  payload: ListingSchedulePayload;
}): Promise<JobListing> {
  return jobListingSchema.parse(
    await apiRequest<unknown>(`/careers/listings/${listingId}/schedule`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  );
}

export async function closeListing(listingId: string): Promise<JobListing> {
  return jobListingSchema.parse(
    await apiRequest<unknown>(`/careers/listings/${listingId}/close`, {
      method: "POST",
    }),
  );
}

export async function archiveListing(listingId: string): Promise<JobListing> {
  return jobListingSchema.parse(
    await apiRequest<unknown>(`/careers/listings/${listingId}/archive`, {
      method: "POST",
    }),
  );
}

export async function getApplications(
  filters: ApplicationFilters,
): Promise<JobApplication[]> {
  const params = new URLSearchParams();

  if (filters.search.trim()) {
    params.set("search", filters.search.trim());
  }

  if (filters.listingId) {
    params.set("listing_id", filters.listingId);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.source) {
    params.set("source", filters.source);
  }

  if (filters.assignedToId) {
    params.set("assigned_to_id", filters.assignedToId);
  }

  params.set("ordering", filters.ordering);

  return jobApplicationSchema
    .array()
    .parse(await apiRequest<unknown>(`/careers/applications?${params}`));
}

export async function getApplication(
  applicationId: string,
): Promise<JobApplication> {
  return jobApplicationSchema.parse(
    await apiRequest<unknown>(`/careers/applications/${applicationId}`),
  );
}

export async function updateApplicationStatus({
  applicationId,
  payload,
}: {
  applicationId: string;
  payload: ApplicationStatusPayload;
}): Promise<JobApplication> {
  return jobApplicationSchema.parse(
    await apiRequest<unknown>(`/careers/applications/${applicationId}/status`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  );
}

export async function reviewApplication({
  applicationId,
  payload,
}: {
  applicationId: string;
  payload: ApplicationReviewPayload;
}): Promise<JobApplication> {
  return jobApplicationSchema.parse(
    await apiRequest<unknown>(`/careers/applications/${applicationId}/review`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),
  );
}

export async function addApplicationNote({
  applicationId,
  payload,
}: {
  applicationId: string;
  payload: ApplicationNotePayload;
}): Promise<ApplicationNote> {
  return applicationNoteSchema.parse(
    await apiRequest<unknown>(`/careers/applications/${applicationId}/notes`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  );
}

export async function getInterviews(
  filters: InterviewFilters,
): Promise<Interview[]> {
  const params = new URLSearchParams();

  if (filters.applicationId) {
    params.set("application_id", filters.applicationId);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.interviewType) {
    params.set("interview_type", filters.interviewType);
  }

  if (filters.organizerId) {
    params.set("organizer_id", filters.organizerId);
  }

  params.set("ordering", filters.ordering);

  return interviewSchema
    .array()
    .parse(await apiRequest<unknown>(`/careers/interviews?${params}`));
}
