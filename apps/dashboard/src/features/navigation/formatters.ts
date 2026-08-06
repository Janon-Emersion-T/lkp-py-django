import type {
  NavigationLinkType,
  NavigationLocation,
  NavigationMenuItem,
  NavigationVisibility,
} from "./types";

export const navigationLocationLabels:
Record<NavigationLocation, string> = {
  header_primary: "Primary Header",
  header_secondary: "Secondary Header",
  footer_primary: "Primary Footer",
  footer_secondary: "Secondary Footer",
  footer_legal: "Legal Footer",
  mobile: "Mobile",
  dashboard: "Dashboard",
  client_portal: "Client Portal",
  custom: "Custom",
};

export const navigationLinkTypeLabels:
Record<NavigationLinkType, string> = {
  internal: "Internal URL",
  external: "External URL",
  route: "Named Route",
  cms_page: "CMS Page",
  service: "Service",
  package: "Package",
  industry: "Industry",
  insight: "Insight",
  case_study: "Case Study",
  careers: "Careers",
  contact: "Contact",
  quote: "Quote Request",
  custom: "Custom",
};

export const navigationVisibilityLabels:
Record<NavigationVisibility, string> = {
  everyone: "Everyone",
  guests: "Guests",
  authenticated: "Authenticated Users",
  staff: "Staff",
  superuser: "Superusers",
};

export function flattenNavigationItems(
  items: NavigationMenuItem[],
): NavigationMenuItem[] {
  return items.flatMap((item) => [
    item,
    ...flattenNavigationItems(
      item.children,
    ),
  ]);
}

export function formatJson(
  value: Record<string, unknown>,
): string {
  return JSON.stringify(
    value,
    null,
    2,
  );
}

export function parseJsonObject(
  value: string,
  fieldName: string,
): Record<string, unknown> {
  const normalized = value.trim();

  if (!normalized) {
    return {};
  }

  const parsed: unknown =
    JSON.parse(normalized);

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
