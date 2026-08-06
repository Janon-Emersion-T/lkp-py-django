import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  addApplicationNote,
  archiveListing,
  closeListing,
  getApplication,
  getApplications,
  getCareersDashboard,
  getDepartments,
  getEmploymentTypes,
  getInterviews,
  getListings,
  getPositions,
  publishListing,
  reviewApplication,
  scheduleListing,
  updateApplicationStatus,
} from "./api";
import type {
  ApplicationFilters,
  InterviewFilters,
  ListingFilters,
} from "./types";

export const careersQueryKeys = {
  all: ["careers"] as const,
  dashboard: ["careers", "dashboard"] as const,
  departments: ["careers", "departments"] as const,
  employmentTypes: ["careers", "employment-types"] as const,
  positions: ["careers", "positions"] as const,
  listings: (filters: ListingFilters) =>
    ["careers", "listings", filters] as const,
  applications: (filters: ApplicationFilters) =>
    ["careers", "applications", filters] as const,
  application: (applicationId: string) =>
    ["careers", "application", applicationId] as const,
  interviews: (filters: InterviewFilters) =>
    ["careers", "interviews", filters] as const,
};

export function useCareersDashboard() {
  return useQuery({
    queryKey: careersQueryKeys.dashboard,
    queryFn: getCareersDashboard,
  });
}

export function useCareerReferenceData() {
  const departments = useQuery({
    queryKey: careersQueryKeys.departments,
    queryFn: getDepartments,
  });

  const employmentTypes = useQuery({
    queryKey: careersQueryKeys.employmentTypes,
    queryFn: getEmploymentTypes,
  });

  const positions = useQuery({
    queryKey: careersQueryKeys.positions,
    queryFn: getPositions,
  });

  return {
    departments,
    employmentTypes,
    positions,
  };
}

export function useJobListings(filters: ListingFilters) {
  return useQuery({
    queryKey: careersQueryKeys.listings(filters),
    queryFn: () => getListings(filters),
  });
}

export function useJobApplications(filters: ApplicationFilters) {
  return useQuery({
    queryKey: careersQueryKeys.applications(filters),
    queryFn: () => getApplications(filters),
  });
}

export function useJobApplication(applicationId: string, enabled: boolean) {
  return useQuery({
    queryKey: careersQueryKeys.application(applicationId),
    queryFn: () => getApplication(applicationId),
    enabled,
  });
}

export function useInterviews(filters: InterviewFilters) {
  return useQuery({
    queryKey: careersQueryKeys.interviews(filters),
    queryFn: () => getInterviews(filters),
  });
}

function useInvalidateCareers() {
  const queryClient = useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey: careersQueryKeys.all,
    });
  };
}

export function usePublishListing() {
  const invalidate = useInvalidateCareers();

  return useMutation({
    mutationFn: publishListing,
    onSuccess: invalidate,
  });
}

export function useScheduleListing() {
  const invalidate = useInvalidateCareers();

  return useMutation({
    mutationFn: scheduleListing,
    onSuccess: invalidate,
  });
}

export function useCloseListing() {
  const invalidate = useInvalidateCareers();

  return useMutation({
    mutationFn: closeListing,
    onSuccess: invalidate,
  });
}

export function useArchiveListing() {
  const invalidate = useInvalidateCareers();

  return useMutation({
    mutationFn: archiveListing,
    onSuccess: invalidate,
  });
}

export function useUpdateApplicationStatus() {
  const invalidate = useInvalidateCareers();

  return useMutation({
    mutationFn: updateApplicationStatus,
    onSuccess: invalidate,
  });
}

export function useReviewApplication() {
  const invalidate = useInvalidateCareers();

  return useMutation({
    mutationFn: reviewApplication,
    onSuccess: invalidate,
  });
}

export function useAddApplicationNote() {
  const invalidate = useInvalidateCareers();

  return useMutation({
    mutationFn: addApplicationNote,
    onSuccess: invalidate,
  });
}
