import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  addEnquiryNote,
  assignEnquiry,
  completeEnquiryFollowUp,
  getContactEnquiries,
  getContactEnquiry,
  getEnquiryDashboard,
  getQuoteEnquiries,
  getQuoteEnquiry,
  updateEnquiryStatus,
} from "./api";
import type {
  ContactEnquiry,
  ContactEnquiryFilters,
  EnquiryKind,
  QuoteEnquiry,
  QuoteEnquiryFilters,
} from "./types";

export const enquiriesQueryKeys = {
  all: ["enquiries"] as const,
  dashboard: ["enquiries", "dashboard"] as const,
  contacts: (filters: ContactEnquiryFilters) =>
    ["enquiries", "contacts", filters] as const,
  quotes: (filters: QuoteEnquiryFilters) =>
    ["enquiries", "quotes", filters] as const,
  detail: (kind: EnquiryKind, enquiryId: string) =>
    ["enquiries", kind, "detail", enquiryId] as const,
};

export function useEnquiryDashboard() {
  return useQuery({
    queryKey: enquiriesQueryKeys.dashboard,
    queryFn: getEnquiryDashboard,
  });
}

export function useContactEnquiries(filters: ContactEnquiryFilters) {
  return useQuery({
    queryKey: enquiriesQueryKeys.contacts(filters),
    queryFn: () => getContactEnquiries(filters),
  });
}

export function useQuoteEnquiries(filters: QuoteEnquiryFilters) {
  return useQuery({
    queryKey: enquiriesQueryKeys.quotes(filters),
    queryFn: () => getQuoteEnquiries(filters),
  });
}

export function useEnquiryDetail(
  kind: EnquiryKind,
  enquiryId: string,
  enabled: boolean,
) {
  return useQuery<ContactEnquiry | QuoteEnquiry>({
    queryKey: enquiriesQueryKeys.detail(kind, enquiryId),
    queryFn: async () => {
      if (kind === "contact") {
        return getContactEnquiry(enquiryId);
      }

      return getQuoteEnquiry(enquiryId);
    },
    enabled,
  });
}

function useInvalidateEnquiries() {
  const queryClient = useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey: enquiriesQueryKeys.all,
    });
  };
}

export function useUpdateEnquiryStatus() {
  const invalidate = useInvalidateEnquiries();

  return useMutation({
    mutationFn: updateEnquiryStatus,
    onSuccess: invalidate,
  });
}

export function useAssignEnquiry() {
  const invalidate = useInvalidateEnquiries();

  return useMutation({
    mutationFn: assignEnquiry,
    onSuccess: invalidate,
  });
}

export function useCompleteEnquiryFollowUp() {
  const invalidate = useInvalidateEnquiries();

  return useMutation({
    mutationFn: completeEnquiryFollowUp,
    onSuccess: invalidate,
  });
}

export function useAddEnquiryNote() {
  const invalidate = useInvalidateEnquiries();

  return useMutation({
    mutationFn: addEnquiryNote,
    onSuccess: invalidate,
  });
}
