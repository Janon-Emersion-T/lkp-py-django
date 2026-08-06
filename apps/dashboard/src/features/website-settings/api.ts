import {
  z,
} from "zod";

import {
  apiRequest,
} from "../../lib/http";
import {
  publicWebsiteSettingsSchema,
  websiteSettingGroupSchema,
  websiteSettingSchema,
} from "./schemas";
import type {
  PublicWebsiteSettings,
  WebsiteSetting,
  WebsiteSettingBulkItem,
  WebsiteSettingFilters,
  WebsiteSettingGroup,
  WebsiteSettingGroupPayload,
  WebsiteSettingPayload,
} from "./types";

function buildSettingsQuery(
  filters: WebsiteSettingFilters,
): string {
  const params = new URLSearchParams();

  const search = filters.search.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.groupId) {
    params.set(
      "group_id",
      filters.groupId,
    );
  }

  if (filters.valueType) {
    params.set(
      "value_type",
      filters.valueType,
    );
  }

  if (filters.environment) {
    params.set(
      "environment",
      filters.environment,
    );
  }

  if (filters.isPublic !== null) {
    params.set(
      "is_public",
      String(filters.isPublic),
    );
  }

  if (filters.isEditable !== null) {
    params.set(
      "is_editable",
      String(filters.isEditable),
    );
  }

  if (filters.isActive !== null) {
    params.set(
      "is_active",
      String(filters.isActive),
    );
  }

  params.set(
    "ordering",
    filters.ordering,
  );

  return params.toString();
}

export async function getSettingGroups():
Promise<WebsiteSettingGroup[]> {
  const response = await apiRequest<unknown>(
    "/website-settings/groups",
  );

  return z.array(
    websiteSettingGroupSchema,
  ).parse(response);
}

export async function createSettingGroup(
  payload: WebsiteSettingGroupPayload,
): Promise<WebsiteSettingGroup> {
  const response = await apiRequest<unknown>(
    "/website-settings/groups",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return websiteSettingGroupSchema.parse(
    response,
  );
}

export async function updateSettingGroup(
  groupId: string,
  payload: WebsiteSettingGroupPayload,
): Promise<WebsiteSettingGroup> {
  const response = await apiRequest<unknown>(
    `/website-settings/groups/${groupId}`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    },
  );

  return websiteSettingGroupSchema.parse(
    response,
  );
}

export async function getWebsiteSettings(
  filters: WebsiteSettingFilters,
): Promise<WebsiteSetting[]> {
  const response = await apiRequest<unknown>(
    `/website-settings/settings?${buildSettingsQuery(
      filters,
    )}`,
  );

  return z.array(
    websiteSettingSchema,
  ).parse(response);
}

export async function createWebsiteSetting(
  payload: WebsiteSettingPayload,
): Promise<WebsiteSetting> {
  const response = await apiRequest<unknown>(
    "/website-settings/settings",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return websiteSettingSchema.parse(
    response,
  );
}

export async function updateWebsiteSetting(
  settingId: string,
  payload: WebsiteSettingPayload,
): Promise<WebsiteSetting> {
  const response = await apiRequest<unknown>(
    `/website-settings/settings/${settingId}`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    },
  );

  return websiteSettingSchema.parse(
    response,
  );
}

export async function bulkUpdateWebsiteSettings(
  settings: WebsiteSettingBulkItem[],
): Promise<WebsiteSetting[]> {
  const response = await apiRequest<unknown>(
    "/website-settings/settings/bulk",
    {
      method: "PUT",
      body: JSON.stringify({
        settings,
      }),
    },
  );

  return z.array(
    websiteSettingSchema,
  ).parse(response);
}

export async function getPublicWebsiteSettings(
  environment: string,
): Promise<PublicWebsiteSettings> {
  const response = await apiRequest<unknown>(
    `/website-settings/public?environment=${encodeURIComponent(
      environment,
    )}`,
  );

  return publicWebsiteSettingsSchema.parse(
    response,
  );
}
