export const settingEnvironments = [
  "global",
  "development",
  "staging",
  "production",
] as const;

export type SettingEnvironment =
  (typeof settingEnvironments)[number];

export const settingValueTypes = [
  "string",
  "text",
  "integer",
  "decimal",
  "boolean",
  "json",
  "email",
  "url",
  "color",
  "media",
] as const;

export type SettingValueType =
  (typeof settingValueTypes)[number];

export const settingOrderingValues = [
  "sort_order",
  "-sort_order",
  "key",
  "-key",
  "label",
  "-label",
  "value_type",
  "-value_type",
  "environment",
  "-environment",
  "created_at",
  "-created_at",
  "updated_at",
  "-updated_at",
] as const;

export type SettingOrdering =
  (typeof settingOrderingValues)[number];

export interface WebsiteSetting {
  id: string;
  group_id: string;
  group_name: string;
  key: string;
  label: string;
  description: string;
  value_type: SettingValueType;
  environment: SettingEnvironment;
  value: string;
  json_value: unknown;
  media_asset_id: string | null;
  default_value: string;
  validation_rules: Record<string, unknown>;
  typed_value: unknown;
  is_public: boolean;
  is_editable: boolean;
  is_required: boolean;
  is_active: boolean;
  sort_order: number;
}

export interface WebsiteSettingGroup {
  id: string;
  name: string;
  slug: string;
  description: string;
  icon: string;
  is_active: boolean;
  sort_order: number;
  setting_count: number;
  settings: WebsiteSetting[];
}

export interface WebsiteSettingGroupPayload {
  name: string;
  slug: string;
  description: string;
  icon: string;
  is_active: boolean;
  sort_order: number;
}

export interface WebsiteSettingPayload {
  group_id: string;
  key: string;
  label: string;
  description: string;
  value_type: SettingValueType;
  environment: SettingEnvironment;
  value: string;
  json_value: unknown;
  media_asset_id: string | null;
  default_value: string;
  validation_rules: Record<string, unknown>;
  is_public: boolean;
  is_editable: boolean;
  is_required: boolean;
  is_active: boolean;
  sort_order: number;
}

export interface WebsiteSettingBulkItem {
  setting_id: string;
  value?: string;
  json_value?: unknown;
  media_asset_id?: string | null;
}

export interface WebsiteSettingFilters {
  search: string;
  groupId: string;
  valueType: SettingValueType | "";
  environment: SettingEnvironment | "";
  isPublic: boolean | null;
  isEditable: boolean | null;
  isActive: boolean | null;
  ordering: SettingOrdering;
}

export interface PublicWebsiteSettings {
  environment: string;
  settings: Record<string, unknown>;
}
