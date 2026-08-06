import type {
  SettingEnvironment,
  SettingValueType,
  WebsiteSetting,
} from "./types";

export const settingEnvironmentLabels:
Record<SettingEnvironment, string> = {
  global: "Global",
  development: "Development",
  staging: "Staging",
  production: "Production",
};

export const settingValueTypeLabels:
Record<SettingValueType, string> = {
  string: "String",
  text: "Long Text",
  integer: "Integer",
  decimal: "Decimal",
  boolean: "Boolean",
  json: "JSON",
  email: "Email",
  url: "URL",
  color: "Colour",
  media: "Media Asset",
};

export function formatJson(
  value: unknown,
): string {
  return JSON.stringify(
    value ?? {},
    null,
    2,
  );
}

export function parseJsonValue(
  value: string,
  fieldName: string,
): unknown {
  const normalized = value.trim();

  if (!normalized) {
    return {};
  }

  try {
    return JSON.parse(normalized);
  } catch {
    throw new Error(
      `${fieldName} contains invalid JSON.`,
    );
  }
}

export function parseJsonObject(
  value: string,
  fieldName: string,
): Record<string, unknown> {
  const parsed = parseJsonValue(
    value,
    fieldName,
  );

  if (
    typeof parsed !== "object"
    || parsed === null
    || Array.isArray(parsed)
  ) {
    throw new Error(
      `${fieldName} must be a JSON object.`,
    );
  }

  return parsed as Record<
    string,
    unknown
  >;
}

export function getSettingDisplayValue(
  setting: WebsiteSetting,
): string {
  if (setting.value_type === "boolean") {
    return setting.typed_value
      ? "Enabled"
      : "Disabled";
  }

  if (setting.value_type === "json") {
    return formatJson(
      setting.json_value,
    );
  }

  if (setting.value_type === "media") {
    return (
      setting.media_asset_id
      ?? "No media selected"
    );
  }

  if (
    setting.typed_value === null
    || setting.typed_value === undefined
  ) {
    return setting.value;
  }

  if (
    typeof setting.typed_value
    === "object"
  ) {
    return formatJson(
      setting.typed_value,
    );
  }

  return String(
    setting.typed_value,
  );
}
