import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import {
  confirmSubscriber,
  createCampaign,
  createNewsletterList,
  createNewsletterTag,
  createSubscriber,
  getCampaign,
  getCampaignRecipients,
  getCampaigns,
  getNewsletterDashboard,
  getNewsletterLists,
  getNewsletterTags,
  getSubscriber,
  getSubscribers,
  markCampaignSent,
  prepareCampaign,
  resubscribeSubscriber,
  scheduleCampaign,
  unsubscribeSubscriber,
  updateCampaign,
  updateSubscriber,
} from "./api";
import type { CampaignFilters, SubscriberFilters } from "./types";

export const newsletterQueryKeys = {
  all: ["newsletter"] as const,
  dashboard: ["newsletter", "dashboard"] as const,
  lists: ["newsletter", "lists"] as const,
  tags: ["newsletter", "tags"] as const,
  subscribers: (filters: SubscriberFilters) =>
    ["newsletter", "subscribers", filters] as const,
  subscriber: (subscriberId: string) =>
    ["newsletter", "subscriber", subscriberId] as const,
  campaigns: (filters: CampaignFilters) =>
    ["newsletter", "campaigns", filters] as const,
  campaign: (campaignId: string) =>
    ["newsletter", "campaign", campaignId] as const,
  recipients: (campaignId: string) =>
    ["newsletter", "campaign", campaignId, "recipients"] as const,
};

export const useNewsletterDashboard = () =>
  useQuery({
    queryKey: newsletterQueryKeys.dashboard,
    queryFn: getNewsletterDashboard,
  });

export const useNewsletterLists = () =>
  useQuery({
    queryKey: newsletterQueryKeys.lists,
    queryFn: getNewsletterLists,
  });

export const useNewsletterTags = () =>
  useQuery({
    queryKey: newsletterQueryKeys.tags,
    queryFn: getNewsletterTags,
  });

export const useSubscribers = (filters: SubscriberFilters) =>
  useQuery({
    queryKey: newsletterQueryKeys.subscribers(filters),
    queryFn: () => getSubscribers(filters),
  });

export const useSubscriber = (subscriberId: string, enabled: boolean) =>
  useQuery({
    queryKey: newsletterQueryKeys.subscriber(subscriberId),
    queryFn: () => getSubscriber(subscriberId),
    enabled,
  });

export const useCampaigns = (filters: CampaignFilters) =>
  useQuery({
    queryKey: newsletterQueryKeys.campaigns(filters),
    queryFn: () => getCampaigns(filters),
  });

export const useCampaign = (campaignId: string, enabled: boolean) =>
  useQuery({
    queryKey: newsletterQueryKeys.campaign(campaignId),
    queryFn: () => getCampaign(campaignId),
    enabled,
  });

export const useCampaignRecipients = (campaignId: string, enabled: boolean) =>
  useQuery({
    queryKey: newsletterQueryKeys.recipients(campaignId),
    queryFn: () => getCampaignRecipients(campaignId),
    enabled,
  });

function useInvalidateNewsletter() {
  const queryClient = useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey: newsletterQueryKeys.all,
    });
  };
}

function mutation<TVariables, TResult>(
  mutationFn: (variables: TVariables) => Promise<TResult>,
) {
  return function useNewsletterMutation() {
    const invalidate = useInvalidateNewsletter();

    return useMutation({
      mutationFn,
      onSuccess: invalidate,
    });
  };
}

export const useCreateNewsletterList = mutation(createNewsletterList);
export const useCreateNewsletterTag = mutation(createNewsletterTag);
export const useCreateSubscriber = mutation(createSubscriber);
export const useUpdateSubscriber = mutation(updateSubscriber);
export const useConfirmSubscriber = mutation(confirmSubscriber);
export const useUnsubscribeSubscriber = mutation(unsubscribeSubscriber);
export const useResubscribeSubscriber = mutation(resubscribeSubscriber);
export const useCreateCampaign = mutation(createCampaign);
export const useUpdateCampaign = mutation(updateCampaign);
export const useScheduleCampaign = mutation(scheduleCampaign);
export const usePrepareCampaign = mutation(prepareCampaign);
export const useMarkCampaignSent = mutation(markCampaignSent);
