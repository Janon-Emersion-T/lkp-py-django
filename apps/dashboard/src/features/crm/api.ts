import {
  apiRequest,
} from "../../lib/http";
import {
  crmReportSchema,
  leadSchema,
  paginatedLeadsSchema,
} from "./schemas";
import type {
  CrmReport,
  Lead,
  LeadFilters,
  PaginatedLeads,
} from "./types";

function buildLeadQueryString(
  filters: LeadFilters,
): string {
  const params = new URLSearchParams();

  params.set("page", String(filters.page));
  params.set(
    "page_size",
    String(filters.pageSize),
  );
  params.set("ordering", filters.ordering);

  const search = filters.search.trim();
  const country = filters.country.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.source) {
    params.set("source", filters.source);
  }

  if (country) {
    params.set("country", country);
  }

  return params.toString();
}

export async function getLeads(
  filters: LeadFilters,
): Promise<PaginatedLeads> {
  const queryString = buildLeadQueryString(filters);

  const response = await apiRequest<unknown>(
    `/crm?${queryString}`,
  );

  return paginatedLeadsSchema.parse(response);
}

export async function getLead(
  leadId: string,
): Promise<Lead> {
  const response = await apiRequest<unknown>(
    `/crm/${leadId}`,
  );

  return leadSchema.parse(response);
}

export async function getCrmReport(): Promise<CrmReport> {
  const response = await apiRequest<unknown>(
    "/dashboard-reporting/crm?preset=this_month&environment=production",
  );

  return crmReportSchema.parse(response);
}
