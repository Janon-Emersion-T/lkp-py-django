import { apiRequest } from "../../lib/http";
import {
  contactEnquirySchema,
  enquiryDashboardSchema,
  enquiryNoteSchema,
  quoteEnquirySchema,
} from "./schemas";
import type {
  ContactEnquiry,
  ContactEnquiryFilters,
  EnquiryAssignmentPayload,
  EnquiryDashboard,
  EnquiryFollowUpPayload,
  EnquiryKind,
  EnquiryNote,
  EnquiryNotePayload,
  EnquiryStatusPayload,
  QuoteEnquiry,
  QuoteEnquiryFilters,
} from "./types";

function buildCommonQuery(filters: ContactEnquiryFilters) {
  const params = new URLSearchParams();

  if (filters.search.trim()) {
    params.set("search", filters.search.trim());
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (filters.priority) {
    params.set("priority", filters.priority);
  }

  if (filters.source) {
    params.set("source", filters.source);
  }

  if (filters.assignedToId.trim()) {
    params.set("assigned_to_id", filters.assignedToId.trim());
  }

  if (filters.ordering) {
    params.set("ordering", filters.ordering);
  }

  return params;
}

export async function getEnquiryDashboard(): Promise<EnquiryDashboard> {
  const response = await apiRequest<unknown>("/enquiries/dashboard");

  return enquiryDashboardSchema.parse(response);
}

export async function getContactEnquiries(
  filters: ContactEnquiryFilters,
): Promise<ContactEnquiry[]> {
  const params = buildCommonQuery(filters);

  const response = await apiRequest<unknown>(`/enquiries/contacts?${params}`);

  return contactEnquirySchema.array().parse(response);
}

export async function getContactEnquiry(
  enquiryId: string,
): Promise<ContactEnquiry> {
  const response = await apiRequest<unknown>(
    `/enquiries/contacts/${enquiryId}`,
  );

  return contactEnquirySchema.parse(response);
}

export async function getQuoteEnquiries(
  filters: QuoteEnquiryFilters,
): Promise<QuoteEnquiry[]> {
  const params = buildCommonQuery(filters);

  if (filters.country.trim()) {
    params.set("country", filters.country.trim());
  }

  if (filters.serviceId.trim()) {
    params.set("service_id", filters.serviceId.trim());
  }

  const response = await apiRequest<unknown>(`/enquiries/quotes?${params}`);

  return quoteEnquirySchema.array().parse(response);
}

export async function getQuoteEnquiry(
  enquiryId: string,
): Promise<QuoteEnquiry> {
  const response = await apiRequest<unknown>(`/enquiries/quotes/${enquiryId}`);

  return quoteEnquirySchema.parse(response);
}

function enquiryPath(kind: EnquiryKind) {
  return kind === "contact" ? "contacts" : "quotes";
}

export async function updateEnquiryStatus({
  kind,
  enquiryId,
  payload,
}: {
  kind: EnquiryKind;
  enquiryId: string;
  payload: EnquiryStatusPayload;
}): Promise<ContactEnquiry | QuoteEnquiry> {
  const response = await apiRequest<unknown>(
    `/enquiries/${enquiryPath(kind)}/${enquiryId}/status`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return kind === "contact"
    ? contactEnquirySchema.parse(response)
    : quoteEnquirySchema.parse(response);
}

export async function assignEnquiry({
  kind,
  enquiryId,
  payload,
}: {
  kind: EnquiryKind;
  enquiryId: string;
  payload: EnquiryAssignmentPayload;
}): Promise<ContactEnquiry | QuoteEnquiry> {
  const response = await apiRequest<unknown>(
    `/enquiries/${enquiryPath(kind)}/${enquiryId}/assignment`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    },
  );

  return kind === "contact"
    ? contactEnquirySchema.parse(response)
    : quoteEnquirySchema.parse(response);
}

export async function completeEnquiryFollowUp({
  kind,
  enquiryId,
  payload,
}: {
  kind: EnquiryKind;
  enquiryId: string;
  payload: EnquiryFollowUpPayload;
}): Promise<ContactEnquiry | QuoteEnquiry> {
  const response = await apiRequest<unknown>(
    `/enquiries/${enquiryPath(kind)}/${enquiryId}/follow-up`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return kind === "contact"
    ? contactEnquirySchema.parse(response)
    : quoteEnquirySchema.parse(response);
}

export async function addEnquiryNote({
  kind,
  enquiryId,
  payload,
}: {
  kind: EnquiryKind;
  enquiryId: string;
  payload: EnquiryNotePayload;
}): Promise<EnquiryNote> {
  const response = await apiRequest<unknown>(
    `/enquiries/${enquiryPath(kind)}/${enquiryId}/notes`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return enquiryNoteSchema.parse(response);
}
