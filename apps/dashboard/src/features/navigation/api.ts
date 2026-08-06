import {
  z,
} from "zod";

import {
  apiRequest,
} from "../../lib/http";
import {
  navigationMenuItemSchema,
  navigationMenuSchema,
  publicNavigationMenuSchema,
} from "./schemas";
import type {
  NavigationFilters,
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuItemPayload,
  NavigationMenuPayload,
  NavigationReorderItem,
  PublicNavigationMenu,
} from "./types";

function buildMenuQuery(
  filters: NavigationFilters,
): string {
  const params = new URLSearchParams();

  const search = filters.search.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.location) {
    params.set(
      "location",
      filters.location,
    );
  }

  if (filters.isActive !== null) {
    params.set(
      "is_active",
      String(filters.isActive),
    );
  }

  if (filters.isPublic !== null) {
    params.set(
      "is_public",
      String(filters.isPublic),
    );
  }

  params.set(
    "ordering",
    filters.ordering,
  );

  return params.toString();
}

export async function getNavigationMenus(
  filters: NavigationFilters,
): Promise<NavigationMenu[]> {
  const response = await apiRequest<unknown>(
    `/navigation/menus?${buildMenuQuery(
      filters,
    )}`,
  );

  return z.array(
    navigationMenuSchema,
  ).parse(response);
}

export async function getNavigationMenu(
  menuId: string,
): Promise<NavigationMenu> {
  const response = await apiRequest<unknown>(
    `/navigation/menus/${menuId}`,
  );

  return navigationMenuSchema.parse(
    response,
  );
}

export async function createNavigationMenu(
  payload: NavigationMenuPayload,
): Promise<NavigationMenu> {
  const response = await apiRequest<unknown>(
    "/navigation/menus",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return navigationMenuSchema.parse(
    response,
  );
}

export async function updateNavigationMenu(
  menuId: string,
  payload: NavigationMenuPayload,
): Promise<NavigationMenu> {
  const response = await apiRequest<unknown>(
    `/navigation/menus/${menuId}`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    },
  );

  return navigationMenuSchema.parse(
    response,
  );
}

export async function createNavigationItem(
  menuId: string,
  payload: NavigationMenuItemPayload,
): Promise<NavigationMenuItem> {
  const response = await apiRequest<unknown>(
    `/navigation/menus/${menuId}/items`,
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
  );

  return navigationMenuItemSchema.parse(
    response,
  );
}

export async function updateNavigationItem(
  itemId: string,
  payload: NavigationMenuItemPayload,
): Promise<NavigationMenuItem> {
  const response = await apiRequest<unknown>(
    `/navigation/items/${itemId}`,
    {
      method: "PUT",
      body: JSON.stringify(payload),
    },
  );

  return navigationMenuItemSchema.parse(
    response,
  );
}

export async function reorderNavigationItems(
  menuId: string,
  items: NavigationReorderItem[],
): Promise<NavigationMenu> {
  const response = await apiRequest<unknown>(
    `/navigation/menus/${menuId}/reorder`,
    {
      method: "POST",
      body: JSON.stringify({
        items,
      }),
    },
  );

  return navigationMenuSchema.parse(
    response,
  );
}

export async function getPublicNavigationMenu(
  slug: string,
): Promise<PublicNavigationMenu> {
  const response = await apiRequest<unknown>(
    `/navigation/public/menus/${encodeURIComponent(
      slug,
    )}`,
  );

  return publicNavigationMenuSchema.parse(
    response,
  );
}
