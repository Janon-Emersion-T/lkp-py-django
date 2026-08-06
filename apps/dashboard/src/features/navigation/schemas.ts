import {
  z,
} from "zod";

import {
  navigationLinkTypes,
  navigationLocations,
  navigationVisibilityValues,
  type NavigationMenuItem,
  type PublicNavigationMenuItem,
} from "./types";

const metadataSchema = z.record(
  z.string(),
  z.unknown(),
);

export const navigationMenuItemSchema:
z.ZodType<NavigationMenuItem> = z.lazy(
  () =>
    z.object({
      id: z.string().uuid(),
      menu_id: z.string().uuid(),
      parent_id:
        z.string().uuid().nullable(),
      label: z.string(),
      link_type: z.enum(
        navigationLinkTypes,
      ),
      url: z.string(),
      resolved_url: z.string(),
      route_name: z.string(),
      route_parameters: metadataSchema,
      cms_page_id:
        z.string().uuid().nullable(),
      service_id:
        z.string().uuid().nullable(),
      package_id:
        z.string().uuid().nullable(),
      industry_id:
        z.string().uuid().nullable(),
      insight_id:
        z.string().uuid().nullable(),
      case_study_id:
        z.string().uuid().nullable(),
      visibility: z.enum(
        navigationVisibilityValues,
      ),
      icon: z.string(),
      css_class: z.string(),
      target_blank: z.boolean(),
      rel_attribute: z.string(),
      is_active: z.boolean(),
      is_featured: z.boolean(),
      sort_order: z.number().int(),
      depth: z.number().int(),
      metadata: metadataSchema,
      children: z.array(
        navigationMenuItemSchema,
      ),
    }),
);

export const navigationMenuSchema =
  z.object({
    id: z.string().uuid(),
    name: z.string(),
    slug: z.string(),
    location: z.enum(
      navigationLocations,
    ),
    description: z.string(),
    is_active: z.boolean(),
    is_public: z.boolean(),
    sort_order: z.number().int(),
    metadata: metadataSchema,
    item_count: z.number().int(),
    items: z.array(
      navigationMenuItemSchema,
    ),
  });

export const publicNavigationItemSchema:
z.ZodType<PublicNavigationMenuItem> =
  z.lazy(() =>
    z.object({
      id: z.string().uuid(),
      parent_id:
        z.string().uuid().nullable(),
      label: z.string(),
      link_type: z.enum(
        navigationLinkTypes,
      ),
      url: z.string(),
      icon: z.string(),
      css_class: z.string(),
      target_blank: z.boolean(),
      rel_attribute: z.string(),
      is_featured: z.boolean(),
      sort_order: z.number().int(),
      metadata: metadataSchema,
      children: z.array(
        publicNavigationItemSchema,
      ),
    }),
  );

export const publicNavigationMenuSchema =
  z.object({
    id: z.string().uuid(),
    name: z.string(),
    slug: z.string(),
    location: z.enum(
      navigationLocations,
    ),
    description: z.string(),
    metadata: metadataSchema,
    items: z.array(
      publicNavigationItemSchema,
    ),
  });

export const navigationMenuPayloadSchema =
  z.object({
    name: z.string().trim().min(
      1,
      "Menu name is required.",
    ),
    slug: z.string().trim().min(
      1,
      "Menu slug is required.",
    ),
    location: z.enum(
      navigationLocations,
    ),
    description: z.string(),
    is_active: z.boolean(),
    is_public: z.boolean(),
    sort_order: z.number().int(),
    metadata: metadataSchema,
  });

export const navigationItemPayloadSchema =
  z.object({
    parent_id:
      z.string().uuid().nullable(),
    label: z.string().trim().min(
      1,
      "Item label is required.",
    ),
    link_type: z.enum(
      navigationLinkTypes,
    ),
    url: z.string(),
    route_name: z.string(),
    route_parameters: metadataSchema,
    cms_page_id:
      z.string().uuid().nullable(),
    service_id:
      z.string().uuid().nullable(),
    package_id:
      z.string().uuid().nullable(),
    industry_id:
      z.string().uuid().nullable(),
    insight_id:
      z.string().uuid().nullable(),
    case_study_id:
      z.string().uuid().nullable(),
    visibility: z.enum(
      navigationVisibilityValues,
    ),
    icon: z.string(),
    css_class: z.string(),
    target_blank: z.boolean(),
    rel_attribute: z.string(),
    is_active: z.boolean(),
    is_featured: z.boolean(),
    sort_order: z.number().int(),
    metadata: metadataSchema,
  });
