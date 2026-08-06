import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";

import {
  getCrmReport,
  getLead,
  getLeads,
} from "./api";
import type {
  LeadFilters,
} from "./types";

const crmRootQueryKey = [
  "crm",
] as const;

export const crmQueryKeys = {
  all: crmRootQueryKey,

  leads: (
    filters: LeadFilters,
  ) => [
    ...crmRootQueryKey,
    "leads",
    filters,
  ] as const,

  lead: (
    leadId: string,
  ) => [
    ...crmRootQueryKey,
    "lead",
    leadId,
  ] as const,

  reporting: [
    ...crmRootQueryKey,
    "reporting",
    "this_month",
  ] as const,
};

export function useLeads(
  filters: LeadFilters,
) {
  return useQuery({
    queryKey: crmQueryKeys.leads(filters),
    queryFn: () => getLeads(filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useLead(
  leadId: string | null,
) {
  return useQuery({
    queryKey: crmQueryKeys.lead(
      leadId ?? "not-selected",
    ),
    queryFn: () => {
      if (!leadId) {
        throw new Error(
          "A lead ID is required.",
        );
      }

      return getLead(leadId);
    },
    enabled: Boolean(leadId),
    staleTime: 30_000,
  });
}

export function useCrmReport() {
  return useQuery({
    queryKey: crmQueryKeys.reporting,
    queryFn: getCrmReport,
    staleTime: 60_000,
  });
}
