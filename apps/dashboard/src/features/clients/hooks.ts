import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";

import {
  getClient,
  getClients,
} from "./api";
import type {
  ClientFilters,
} from "./types";

const clientsRootQueryKey = [
  "clients",
] as const;

export const clientQueryKeys = {
  all: clientsRootQueryKey,

  list: (
    filters: ClientFilters,
  ) => [
    ...clientsRootQueryKey,
    "list",
    filters,
  ] as const,

  detail: (
    clientId: string,
  ) => [
    ...clientsRootQueryKey,
    "detail",
    clientId,
  ] as const,
};

export function useClients(
  filters: ClientFilters,
) {
  return useQuery({
    queryKey:
      clientQueryKeys.list(filters),
    queryFn: () => getClients(filters),
    placeholderData: keepPreviousData,
    staleTime: 30_000,
  });
}

export function useClient(
  clientId: string | null,
) {
  return useQuery({
    queryKey: clientQueryKeys.detail(
      clientId ?? "not-selected",
    ),
    queryFn: () => {
      if (!clientId) {
        throw new Error(
          "A client ID is required.",
        );
      }

      return getClient(clientId);
    },
    enabled: Boolean(clientId),
    staleTime: 30_000,
  });
}
