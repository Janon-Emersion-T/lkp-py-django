import {
  keepPreviousData,
  useQuery,
} from "@tanstack/react-query";

import {
  getExecutiveDashboardReport,
} from "./api";
import type {
  DashboardQuery,
} from "./types";

export const dashboardQueryKeys = {
  all: ["dashboard-reporting"] as const,

  executive: (
    query: DashboardQuery,
  ) => [
    ...dashboardQueryKeys.all,
    "executive",
    query,
  ] as const,
};

export function useExecutiveDashboard(
  query: DashboardQuery,
) {
  return useQuery({
    queryKey: dashboardQueryKeys.executive(query),
    queryFn: () => getExecutiveDashboardReport(query),
    placeholderData: keepPreviousData,
    staleTime: 60_000,
  });
}
