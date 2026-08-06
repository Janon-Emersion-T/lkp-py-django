import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  createNavigationItem,
  createNavigationMenu,
  getNavigationMenu,
  getNavigationMenus,
  getPublicNavigationMenu,
  reorderNavigationItems,
  updateNavigationItem,
  updateNavigationMenu,
} from "./api";
import type {
  NavigationFilters,
  NavigationMenuItemPayload,
  NavigationMenuPayload,
  NavigationReorderItem,
} from "./types";

const navigationRootKey = [
  "navigation",
] as const;

export const navigationQueryKeys = {
  all: navigationRootKey,

  menus: (
    filters: NavigationFilters,
  ) => [
    ...navigationRootKey,
    "menus",
    filters,
  ] as const,

  menu: (
    menuId: string,
  ) => [
    ...navigationRootKey,
    "menu",
    menuId,
  ] as const,

  publicMenu: (
    slug: string,
  ) => [
    ...navigationRootKey,
    "public-menu",
    slug,
  ] as const,
};

export function useNavigationMenus(
  filters: NavigationFilters,
) {
  return useQuery({
    queryKey:
      navigationQueryKeys.menus(
        filters,
      ),
    queryFn: () =>
      getNavigationMenus(filters),
    staleTime: 30_000,
  });
}

export function useNavigationMenu(
  menuId: string | null,
) {
  return useQuery({
    queryKey: navigationQueryKeys.menu(
      menuId ?? "not-selected",
    ),
    queryFn: () => {
      if (!menuId) {
        throw new Error(
          "A navigation menu ID is required.",
        );
      }

      return getNavigationMenu(menuId);
    },
    enabled: Boolean(menuId),
    staleTime: 15_000,
  });
}

export function usePublicNavigationMenu(
  slug: string | null,
  enabled: boolean,
) {
  return useQuery({
    queryKey:
      navigationQueryKeys.publicMenu(
        slug ?? "not-selected",
      ),
    queryFn: () => {
      if (!slug) {
        throw new Error(
          "A navigation menu slug is required.",
        );
      }

      return getPublicNavigationMenu(slug);
    },
    enabled:
      enabled && Boolean(slug),
    staleTime: 10_000,
  });
}

export function useCreateNavigationMenu() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn:
      createNavigationMenu,
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey:
          navigationQueryKeys.all,
      });
    },
  });
}

export function useUpdateNavigationMenu() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      menuId,
      payload,
    }: {
      menuId: string;
      payload: NavigationMenuPayload;
    }) =>
      updateNavigationMenu(
        menuId,
        payload,
      ),
    onSuccess: async (
      updatedMenu,
    ) => {
      queryClient.setQueryData(
        navigationQueryKeys.menu(
          updatedMenu.id,
        ),
        updatedMenu,
      );

      await queryClient.invalidateQueries({
        queryKey:
          navigationQueryKeys.all,
      });
    },
  });
}

export function useCreateNavigationItem() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      menuId,
      payload,
    }: {
      menuId: string;
      payload:
        NavigationMenuItemPayload;
    }) =>
      createNavigationItem(
        menuId,
        payload,
      ),
    onSuccess: async (
      _item,
      variables,
    ) => {
      await queryClient.invalidateQueries({
        queryKey:
          navigationQueryKeys.menu(
            variables.menuId,
          ),
      });

      await queryClient.invalidateQueries({
        queryKey:
          navigationQueryKeys.all,
      });
    },
  });
}

export function useUpdateNavigationItem(
  menuId: string | null,
) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      itemId,
      payload,
    }: {
      itemId: string;
      payload:
        NavigationMenuItemPayload;
    }) =>
      updateNavigationItem(
        itemId,
        payload,
      ),
    onSuccess: async () => {
      if (menuId) {
        await queryClient.invalidateQueries({
          queryKey:
            navigationQueryKeys.menu(
              menuId,
            ),
        });
      }

      await queryClient.invalidateQueries({
        queryKey:
          navigationQueryKeys.all,
      });
    },
  });
}

export function useReorderNavigationItems() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      menuId,
      items,
    }: {
      menuId: string;
      items: NavigationReorderItem[];
    }) =>
      reorderNavigationItems(
        menuId,
        items,
      ),
    onSuccess: async (
      updatedMenu,
    ) => {
      queryClient.setQueryData(
        navigationQueryKeys.menu(
          updatedMenu.id,
        ),
        updatedMenu,
      );

      await queryClient.invalidateQueries({
        queryKey:
          navigationQueryKeys.all,
      });
    },
  });
}
