import { apiRequest } from "../../lib/http";
import {
  campaignRecipientSchema,
  newsletterCampaignSchema,
  newsletterDashboardSchema,
  newsletterListSchema,
  newsletterTagSchema,
  subscriberSchema,
} from "./schemas";
import type {
  CampaignFilters,
  CampaignPayload,
  CampaignRecipient,
  CampaignSchedulePayload,
  NewsletterCampaign,
  NewsletterDashboard,
  NewsletterList,
  NewsletterListPayload,
  NewsletterTag,
  NewsletterTagPayload,
  Subscriber,
  SubscriberFilters,
  SubscriberPayload,
} from "./types";

function buildSubscriberQuery(filters: SubscriberFilters): string {
  const params = new URLSearchParams();

  if (filters.search.trim()) params.set("search", filters.search.trim());
  if (filters.status) params.set("status", filters.status);
  if (filters.source) params.set("source", filters.source);
  if (filters.country.trim()) params.set("country", filters.country.trim());
  if (filters.language.trim()) params.set("language", filters.language.trim());
  if (filters.listId) params.set("list_id", filters.listId);
  if (filters.tagId) params.set("tag_id", filters.tagId);
  if (filters.ordering) params.set("ordering", filters.ordering);

  return params.toString();
}

function buildCampaignQuery(filters: CampaignFilters): string {
  const params = new URLSearchParams();

  if (filters.search.trim()) params.set("search", filters.search.trim());
  if (filters.status) params.set("status", filters.status);
  if (filters.ordering) params.set("ordering", filters.ordering);

  return params.toString();
}

export async function getNewsletterDashboard(): Promise<NewsletterDashboard> {
  return newsletterDashboardSchema.parse(
    await apiRequest<unknown>("/newsletter/dashboard"),
  );
}

export async function getNewsletterLists(): Promise<NewsletterList[]> {
  return newsletterListSchema
    .array()
    .parse(await apiRequest<unknown>("/newsletter/lists"));
}

export async function createNewsletterList(
  payload: NewsletterListPayload,
): Promise<NewsletterList> {
  return newsletterListSchema.parse(
    await apiRequest<unknown>("/newsletter/lists", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  );
}

export async function getNewsletterTags(): Promise<NewsletterTag[]> {
  return newsletterTagSchema
    .array()
    .parse(await apiRequest<unknown>("/newsletter/tags"));
}

export async function createNewsletterTag(
  payload: NewsletterTagPayload,
): Promise<NewsletterTag> {
  return newsletterTagSchema.parse(
    await apiRequest<unknown>("/newsletter/tags", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  );
}

export async function getSubscribers(
  filters: SubscriberFilters,
): Promise<Subscriber[]> {
  return subscriberSchema
    .array()
    .parse(
      await apiRequest<unknown>(
        `/newsletter/subscribers?${buildSubscriberQuery(filters)}`,
      ),
    );
}

export async function getSubscriber(subscriberId: string): Promise<Subscriber> {
  return subscriberSchema.parse(
    await apiRequest<unknown>(`/newsletter/subscribers/${subscriberId}`),
  );
}

export async function createSubscriber(
  payload: SubscriberPayload,
): Promise<Subscriber> {
  return subscriberSchema.parse(
    await apiRequest<unknown>("/newsletter/subscribers", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  );
}

export async function updateSubscriber({
  subscriberId,
  payload,
}: {
  subscriberId: string;
  payload: SubscriberPayload;
}): Promise<Subscriber> {
  return subscriberSchema.parse(
    await apiRequest<unknown>(`/newsletter/subscribers/${subscriberId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),
  );
}

async function subscriberAction(
  subscriberId: string,
  action: "confirm" | "unsubscribe" | "resubscribe",
): Promise<Subscriber> {
  return subscriberSchema.parse(
    await apiRequest<unknown>(
      `/newsletter/subscribers/${subscriberId}/${action}`,
      { method: "POST" },
    ),
  );
}

export const confirmSubscriber = (subscriberId: string) =>
  subscriberAction(subscriberId, "confirm");

export const unsubscribeSubscriber = (subscriberId: string) =>
  subscriberAction(subscriberId, "unsubscribe");

export const resubscribeSubscriber = (subscriberId: string) =>
  subscriberAction(subscriberId, "resubscribe");

export async function getCampaigns(
  filters: CampaignFilters,
): Promise<NewsletterCampaign[]> {
  return newsletterCampaignSchema
    .array()
    .parse(
      await apiRequest<unknown>(
        `/newsletter/campaigns?${buildCampaignQuery(filters)}`,
      ),
    );
}

export async function getCampaign(
  campaignId: string,
): Promise<NewsletterCampaign> {
  return newsletterCampaignSchema.parse(
    await apiRequest<unknown>(`/newsletter/campaigns/${campaignId}`),
  );
}

export async function createCampaign(
  payload: CampaignPayload,
): Promise<NewsletterCampaign> {
  return newsletterCampaignSchema.parse(
    await apiRequest<unknown>("/newsletter/campaigns", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  );
}

export async function updateCampaign({
  campaignId,
  payload,
}: {
  campaignId: string;
  payload: CampaignPayload;
}): Promise<NewsletterCampaign> {
  return newsletterCampaignSchema.parse(
    await apiRequest<unknown>(`/newsletter/campaigns/${campaignId}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),
  );
}

export async function scheduleCampaign({
  campaignId,
  payload,
}: {
  campaignId: string;
  payload: CampaignSchedulePayload;
}): Promise<NewsletterCampaign> {
  return newsletterCampaignSchema.parse(
    await apiRequest<unknown>(`/newsletter/campaigns/${campaignId}/schedule`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  );
}

async function campaignAction(
  campaignId: string,
  action: "prepare" | "mark-sent",
): Promise<NewsletterCampaign> {
  return newsletterCampaignSchema.parse(
    await apiRequest<unknown>(`/newsletter/campaigns/${campaignId}/${action}`, {
      method: "POST",
    }),
  );
}

export const prepareCampaign = (campaignId: string) =>
  campaignAction(campaignId, "prepare");

export const markCampaignSent = (campaignId: string) =>
  campaignAction(campaignId, "mark-sent");

export async function getCampaignRecipients(
  campaignId: string,
): Promise<CampaignRecipient[]> {
  return campaignRecipientSchema
    .array()
    .parse(
      await apiRequest<unknown>(
        `/newsletter/campaigns/${campaignId}/recipients`,
      ),
    );
}
