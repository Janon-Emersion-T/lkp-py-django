import {
  apiRequest,
} from "../../lib/http";
import {
  executiveDashboardReportSchema,
} from "./schemas";
import type {
  DashboardQuery,
  ExecutiveDashboardReport,
} from "./types";

function buildDashboardQueryString(
  query: DashboardQuery,
): string {
  const params = new URLSearchParams();

  params.set("preset", query.preset);
  params.set(
    "environment",
    query.environment ?? "production",
  );

  if (query.preset === "custom") {
    if (!query.dateFrom || !query.dateTo) {
      throw new Error(
        "Custom dashboard periods require both dates.",
      );
    }

    params.set("date_from", query.dateFrom);
    params.set("date_to", query.dateTo);
  }

  return params.toString();
}

export async function getExecutiveDashboardReport(
  query: DashboardQuery,
): Promise<ExecutiveDashboardReport> {
  const queryString = buildDashboardQueryString(query);

  const response = await apiRequest<unknown>(
    `/dashboard-reporting/executive?${queryString}`,
  );

  return executiveDashboardReportSchema.parse(
    response,
  );
}
