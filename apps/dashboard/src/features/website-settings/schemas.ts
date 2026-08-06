import {
  z,
} from "zod";

import {
  settingEnvironments,
  settingValueTypes,
} from "./types";

const jsonObjectSchema = z.record(
  z.string(),
  z.unknown(),
);

export const websiteSettingSchema =
  z.object({
    id: z.string().uuid(),
    group_id: z.string().uuid(),
    group_name: z.string(),
    key: z.string(),
    label: z.string(),
    description: z.string(),
    value_type: z.enum(
      settingValueTypes,
    ),
    environment: z.enum(
      settingEnvironments,
    ),
    value: z.string(),
    json_value: z.unknown(),
    media_asset_id:
      z.string().uuid().nullable(),
    default_value: z.string(),
    validation_rules:
      jsonObjectSchema,
    typed_value: z.unknown(),
    is_public: z.boolean(),
    is_editable: z.boolean(),
    is_required: z.boolean(),
    is_active: z.boolean(),
    sort_order: z.number().int(),
  });

export const websiteSettingGroupSchema:
z.ZodType<{
  id: string;
  name: string;
  slug: string;
  description: string;
  icon: string;
  is_active: boolean;
  sort_order: number;
  setting_count: number;
  settings: z.infer<
    typeof websiteSettingSchema
  >[];
}> = z.object({
  id: z.string().uuid(),
  name: z.string(),
  slug: z.string(),
  description: z.string(),
  icon: z.string(),
  is_active: z.boolean(),
  sort_order: z.number().int(),
  setting_count: z.number().int(),
  settings: z.array(
    websiteSettingSchema,
  ),
});

export const websiteSettingGroupPayloadSchema =
  z.object({
    name: z.string().trim().min(
      1,
      "Group name is required.",
    ),
    slug: z.string().trim().min(
      1,
      "Group slug is required.",
    ),
    description: z.string(),
    icon: z.string(),
    is_active: z.boolean(),
    sort_order: z.number().int(),
  });

export const websiteSettingPayloadSchema =
  z.object({
    group_id: z.string().uuid(),
    key: z.string().trim().min(
      1,
      "Setting key is required.",
    ),
    label: z.string().trim().min(
      1,
      "Setting label is required.",
    ),
    description: z.string(),
    value_type: z.enum(
      settingValueTypes,
    ),
    environment: z.enum(
      settingEnvironments,
    ),
    value: z.string(),
    json_value: z.unknown(),
    media_asset_id:
      z.string().uuid().nullable(),
    default_value: z.string(),
    validation_rules:
      jsonObjectSchema,
    is_public: z.boolean(),
    is_editable: z.boolean(),
    is_required: z.boolean(),
    is_active: z.boolean(),
    sort_order: z.number().int(),
  });

export const publicWebsiteSettingsSchema =
  z.object({
    environment: z.string(),
    settings: jsonObjectSchema,
  });
