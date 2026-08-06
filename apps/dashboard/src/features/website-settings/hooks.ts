import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  bulkUpdateWebsiteSettings,
  createSettingGroup,
  createWebsiteSetting,
  getPublicWebsiteSettings,
  getSettingGroups,
  getWebsiteSettings,
  updateSettingGroup,
  updateWebsiteSetting,
} from "./api";
import type {
  WebsiteSettingBulkItem,
  WebsiteSettingFilters,
  WebsiteSettingGroupPayload,
  WebsiteSettingPayload,
} from "./types";

const settingsRootKey = [
  "website-settings",
] as const;

export const websiteSettingsQueryKeys = {
  all: settingsRootKey,

  groups: [
    ...settingsRootKey,
    "groups",
  ] as const,

  settings: (
    filters: WebsiteSettingFilters,
  ) => [
    ...settingsRootKey,
    "settings",
    filters,
  ] as const,

  public: (
    environment: string,
  ) => [
    ...settingsRootKey,
    "public",
    environment,
  ] as const,
};

export function useSettingGroups() {
  return useQuery({
    queryKey:
      websiteSettingsQueryKeys.groups,
    queryFn: getSettingGroups,
    staleTime: 30_000,
  });
}

export function useWebsiteSettings(
  filters: WebsiteSettingFilters,
) {
  return useQuery({
    queryKey:
      websiteSettingsQueryKeys.settings(
        filters,
      ),
    queryFn: () =>
      getWebsiteSettings(filters),
    staleTime: 30_000,
  });
}

export function usePublicWebsiteSettings(
  environment: string,
  enabled: boolean,
) {
  return useQuery({
    queryKey:
      websiteSettingsQueryKeys.public(
        environment,
      ),
    queryFn: () =>
      getPublicWebsiteSettings(
        environment,
      ),
    enabled,
    staleTime: 10_000,
  });
}

export function useCreateSettingGroup() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createSettingGroup,
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey:
          websiteSettingsQueryKeys.all,
      });
    },
  });
}

export function useUpdateSettingGroup() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      groupId,
      payload,
    }: {
      groupId: string;
      payload:
        WebsiteSettingGroupPayload;
    }) =>
      updateSettingGroup(
        groupId,
        payload,
      ),
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey:
          websiteSettingsQueryKeys.all,
      });
    },
  });
}

export function useCreateWebsiteSetting() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn:
      createWebsiteSetting,
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey:
          websiteSettingsQueryKeys.all,
      });
    },
  });
}

export function useUpdateWebsiteSetting() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      settingId,
      payload,
    }: {
      settingId: string;
      payload: WebsiteSettingPayload;
    }) =>
      updateWebsiteSetting(
        settingId,
        payload,
      ),
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey:
          websiteSettingsQueryKeys.all,
      });
    },
  });
}

export function useBulkUpdateWebsiteSettings() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (
      settings:
        WebsiteSettingBulkItem[],
    ) =>
      bulkUpdateWebsiteSettings(
        settings,
      ),
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey:
          websiteSettingsQueryKeys.all,
      });
    },
  });
}
