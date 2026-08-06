export const navigationLocations = [
  "header_primary",
  "header_secondary",
  "footer_primary",
  "footer_secondary",
  "footer_legal",
  "mobile",
  "dashboard",
  "client_portal",
  "custom",
] as const;

export type NavigationLocation =
  (typeof navigationLocations)[number];

export const navigationLinkTypes = [
  "internal",
  "external",
  "route",
  "cms_page",
  "service",
  "package",
  "industry",
  "insight",
  "case_study",
  "careers",
  "contact",
  "quote",
  "custom",
] as const;

export type NavigationLinkType =
  (typeof navigationLinkTypes)[number];

export const navigationVisibilityValues = [
  "everyone",
  "guests",
  "authenticated",
  "staff",
  "superuser",
] as const;

export type NavigationVisibility =
  (typeof navigationVisibilityValues)[number];

export const navigationOrderingValues = [
  "sort_order",
  "-sort_order",
  "name",
  "-name",
  "location",
  "-location",
  "created_at",
  "-created_at",
  "updated_at",
  "-updated_at",
] as const;

export type NavigationOrdering =
  (typeof navigationOrderingValues)[number];

export interface NavigationMenuItem {
  id: string;
  menu_id: string;
  parent_id: string | null;
  label: string;
  link_type: NavigationLinkType;
  url: string;
  resolved_url: string;
  route_name: string;
  route_parameters: Record<string, unknown>;
  cms_page_id: string | null;
  service_id: string | null;
  package_id: string | null;
  industry_id: string | null;
  insight_id: string | null;
  case_study_id: string | null;
  visibility: NavigationVisibility;
  icon: string;
  css_class: string;
  target_blank: boolean;
  rel_attribute: string;
  is_active: boolean;
  is_featured: boolean;
  sort_order: number;
  depth: number;
  metadata: Record<string, unknown>;
  children: NavigationMenuItem[];
}

export interface NavigationMenu {
  id: string;
  name: string;
  slug: string;
  location: NavigationLocation;
  description: string;
  is_active: boolean;
  is_public: boolean;
  sort_order: number;
  metadata: Record<string, unknown>;
  item_count: number;
  items: NavigationMenuItem[];
}

export interface PublicNavigationMenuItem {
  id: string;
  parent_id: string | null;
  label: string;
  link_type: NavigationLinkType;
  url: string;
  icon: string;
  css_class: string;
  target_blank: boolean;
  rel_attribute: string;
  is_featured: boolean;
  sort_order: number;
  metadata: Record<string, unknown>;
  children: PublicNavigationMenuItem[];
}

export interface PublicNavigationMenu {
  id: string;
  name: string;
  slug: string;
  location: NavigationLocation;
  description: string;
  metadata: Record<string, unknown>;
  items: PublicNavigationMenuItem[];
}

export interface NavigationMenuPayload {
  name: string;
  slug: string;
  location: NavigationLocation;
  description: string;
  is_active: boolean;
  is_public: boolean;
  sort_order: number;
  metadata: Record<string, unknown>;
}

export interface NavigationMenuItemPayload {
  parent_id: string | null;
  label: string;
  link_type: NavigationLinkType;
  url: string;
  route_name: string;
  route_parameters: Record<string, unknown>;
  cms_page_id: string | null;
  service_id: string | null;
  package_id: string | null;
  industry_id: string | null;
  insight_id: string | null;
  case_study_id: string | null;
  visibility: NavigationVisibility;
  icon: string;
  css_class: string;
  target_blank: boolean;
  rel_attribute: string;
  is_active: boolean;
  is_featured: boolean;
  sort_order: number;
  metadata: Record<string, unknown>;
}

export interface NavigationReorderItem {
  id: string;
  parent_id: string | null;
  sort_order: number;
}

export interface NavigationFilters {
  search: string;
  location: NavigationLocation | "";
  isActive: boolean | null;
  isPublic: boolean | null;
  ordering: NavigationOrdering;
}
