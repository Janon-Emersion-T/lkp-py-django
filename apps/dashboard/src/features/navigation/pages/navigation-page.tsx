import {
  Eye,
  Menu,
  Pencil,
  Plus,
  RefreshCw,
} from "lucide-react";
import {
  useDeferredValue,
  useMemo,
  useState,
} from "react";

import {
  PageHeader,
} from "../../../components/layout/page-header";
import {
  Button,
} from "../../../components/ui/button";
import {
  NavigationFiltersBar,
} from "../components/navigation-filters";
import {
  NavigationItemForm,
} from "../components/navigation-item-form";
import {
  NavigationMenuForm,
} from "../components/navigation-menu-form";
import {
  NavigationMenuList,
} from "../components/navigation-menu-list";
import {
  NavigationPublicPreview,
} from "../components/navigation-public-preview";
import {
  NavigationTree,
} from "../components/navigation-tree";
import {
  flattenNavigationItems,
  navigationLocationLabels,
} from "../formatters";
import {
  useNavigationMenu,
  useNavigationMenus,
  useReorderNavigationItems,
} from "../hooks";
import type {
  NavigationFilters,
  NavigationMenu,
  NavigationMenuItem,
  NavigationReorderItem,
} from "../types";

const initialFilters:
NavigationFilters = {
  search: "",
  location: "",
  isActive: null,
  isPublic: null,
  ordering: "sort_order",
};

function buildReorderPayload(
  items: NavigationMenuItem[],
): NavigationReorderItem[] {
  return items.flatMap((item) => [
    {
      id: item.id,
      parent_id: item.parent_id,
      sort_order: item.sort_order,
    },
    ...buildReorderPayload(
      item.children,
    ),
  ]);
}

function findSiblingCollection(
  roots: NavigationMenuItem[],
  item: NavigationMenuItem,
): NavigationMenuItem[] | null {
  if (item.parent_id === null) {
    return roots;
  }

  const parent =
    flattenNavigationItems(
      roots,
    ).find(
      (candidate) =>
        candidate.id
        === item.parent_id,
    );

  return parent?.children ?? null;
}

export function NavigationPage() {
  const [
    filters,
    setFilters,
  ] = useState(initialFilters);

  const [
    selectedMenuId,
    setSelectedMenuId,
  ] = useState<string | null>(null);

  const [
    menuFormOpen,
    setMenuFormOpen,
  ] = useState(false);

  const [
    editingMenu,
    setEditingMenu,
  ] = useState<NavigationMenu | null>(
    null,
  );

  const [
    itemFormOpen,
    setItemFormOpen,
  ] = useState(false);

  const [
    editingItem,
    setEditingItem,
  ] = useState<NavigationMenuItem | null>(
    null,
  );

  const [
    suggestedParentId,
    setSuggestedParentId,
  ] = useState<string | null>(null);

  const [
    previewOpen,
    setPreviewOpen,
  ] = useState(false);

  const [
    operationError,
    setOperationError,
  ] = useState("");

  const deferredSearch =
    useDeferredValue(filters.search);

  const menusQuery =
    useNavigationMenus({
      ...filters,
      search: deferredSearch,
    });

  const menuQuery =
    useNavigationMenu(
      selectedMenuId,
    );

  const reorderMutation =
    useReorderNavigationItems();

  const selectedMenu =
    menuQuery.data ?? null;

  const menuStats = useMemo(() => {
    const menus =
      menusQuery.data ?? [];

    return {
      total: menus.length,
      active: menus.filter(
        (menu) => menu.is_active,
      ).length,
      public: menus.filter(
        (menu) => menu.is_public,
      ).length,
      items: menus.reduce(
        (total, menu) =>
          total + menu.item_count,
        0,
      ),
    };
  }, [menusQuery.data]);

  function openCreateMenu() {
    setEditingMenu(null);
    setMenuFormOpen(true);
  }

  function openEditMenu() {
    if (!selectedMenu) {
      return;
    }

    setEditingMenu(selectedMenu);
    setMenuFormOpen(true);
  }

  function openCreateItem(
    parentId: string | null,
  ) {
    setEditingItem(null);
    setSuggestedParentId(parentId);
    setItemFormOpen(true);
  }

  function openEditItem(
    item: NavigationMenuItem,
  ) {
    setEditingItem(item);
    setSuggestedParentId(null);
    setItemFormOpen(true);
  }

  async function moveItem(
    item: NavigationMenuItem,
    direction: "up" | "down",
  ) {
    if (!selectedMenu) {
      return;
    }

    setOperationError("");

    try {
      const siblings =
        findSiblingCollection(
          selectedMenu.items,
          item,
        );

      if (!siblings) {
        throw new Error(
          "The sibling collection could not be resolved.",
        );
      }

      const currentIndex =
        siblings.findIndex(
          (candidate) =>
            candidate.id === item.id,
        );

      const targetIndex =
        direction === "up"
          ? currentIndex - 1
          : currentIndex + 1;

      if (
        currentIndex < 0
        || targetIndex < 0
        || targetIndex
          >= siblings.length
      ) {
        return;
      }

      const reordered =
        [...siblings];

      [
        reordered[currentIndex],
        reordered[targetIndex],
      ] = [
        reordered[targetIndex],
        reordered[currentIndex],
      ];

      const orderById = new Map(
        reordered.map(
          (candidate, index) => [
            candidate.id,
            index,
          ],
        ),
      );

      const payload =
        buildReorderPayload(
          selectedMenu.items,
        ).map((entry) => ({
          ...entry,
          sort_order:
            orderById.has(entry.id)
              ? orderById.get(
                entry.id,
              ) ?? entry.sort_order
              : entry.sort_order,
        }));

      await reorderMutation.mutateAsync({
        menuId: selectedMenu.id,
        items: payload,
      });
    } catch (error) {
      setOperationError(
        error instanceof Error
          ? error.message
          : "The navigation order could not be updated.",
      );
    }
  }

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Website structure"
          title="Navigation Management"
          description="Manage website menus, locations, public visibility, nested items, linked content, audience visibility, hierarchy, and display order."
        />

        <div className="flex flex-wrap gap-2">
          <Button
            variant="outline"
            onClick={() => {
              void menusQuery.refetch();

              if (selectedMenuId) {
                void menuQuery.refetch();
              }
            }}
            className="dark:border-slate-700"
          >
            <RefreshCw
              size={16}
              className={
                menusQuery.isFetching
                  || menuQuery.isFetching
                  ? "animate-spin"
                  : undefined
              }
            />
            Refresh
          </Button>

          <Button
            onClick={openCreateMenu}
          >
            <Plus size={16} />
            Create menu
          </Button>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[
          [
            "Menus",
            menuStats.total,
          ],
          [
            "Active menus",
            menuStats.active,
          ],
          [
            "Public menus",
            menuStats.public,
          ],
          [
            "Total items",
            menuStats.items,
          ],
        ].map(([label, value]) => (
          <article
            key={label}
            className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900"
          >
            <p className="text-sm text-slate-500 dark:text-slate-400">
              {label}
            </p>

            <p className="mt-3 text-3xl font-bold text-slate-950 dark:text-white">
              {value}
            </p>
          </article>
        ))}
      </div>

      <NavigationFiltersBar
        filters={filters}
        onChange={setFilters}
      />

      {menusQuery.isError && (
        <p className="rounded-xl border border-red-200 bg-red-50 p-5 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
          {menusQuery.error.message}
        </p>
      )}

      <div className="grid gap-6 xl:grid-cols-[360px_minmax(0,1fr)]">
        <aside>
          {menusQuery.isLoading ? (
            <div className="h-80 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
          ) : (
            <NavigationMenuList
              menus={
                menusQuery.data ?? []
              }
              selectedMenuId={
                selectedMenuId
              }
              onSelect={
                setSelectedMenuId
              }
            />
          )}
        </aside>

        <main>
          {!selectedMenuId && (
            <section className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-20 text-center dark:border-slate-700 dark:bg-slate-900">
              <Menu
                size={30}
                className="mx-auto text-slate-400"
              />

              <h2 className="mt-4 font-semibold text-slate-950 dark:text-white">
                Select a navigation menu
              </h2>

              <p className="mt-2 text-sm text-slate-500">
                Choose a menu to inspect and manage its hierarchy.
              </p>
            </section>
          )}

          {menuQuery.isLoading && (
            <div className="h-96 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
          )}

          {menuQuery.isError && (
            <p className="rounded-xl border border-red-200 bg-red-50 p-5 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {menuQuery.error.message}
            </p>
          )}

          {selectedMenu && (
            <div className="space-y-5">
              <section className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
                <div className="flex flex-col gap-4 lg:flex-row lg:items-start">
                  <div>
                    <h2 className="text-xl font-bold text-slate-950 dark:text-white">
                      {selectedMenu.name}
                    </h2>

                    <p className="mt-1 text-sm text-slate-500">
                      /{selectedMenu.slug}
                      {" · "}
                      {
                        navigationLocationLabels[
                          selectedMenu.location
                        ]
                      }
                    </p>

                    {selectedMenu.description && (
                      <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-600 dark:text-slate-300">
                        {
                          selectedMenu.description
                        }
                      </p>
                    )}
                  </div>

                  <div className="flex flex-wrap gap-2 lg:ml-auto">
                    <Button
                      variant="outline"
                      onClick={openEditMenu}
                    >
                      <Pencil size={16} />
                      Edit menu
                    </Button>

                    <Button
                      variant="outline"
                      disabled={
                        !selectedMenu.is_public
                        || !selectedMenu.is_active
                      }
                      onClick={() => {
                        setPreviewOpen(true);
                      }}
                    >
                      <Eye size={16} />
                      Public preview
                    </Button>

                    <Button
                      onClick={() => {
                        openCreateItem(null);
                      }}
                    >
                      <Plus size={16} />
                      Add root item
                    </Button>
                  </div>
                </div>
              </section>

              {operationError && (
                <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
                  {operationError}
                </p>
              )}

              {reorderMutation.isPending && (
                <p className="rounded-xl border border-blue-200 bg-blue-50 p-3 text-sm text-blue-800 dark:border-blue-900 dark:bg-blue-950/30 dark:text-blue-300">
                  Updating navigation order…
                </p>
              )}

              <NavigationTree
                items={selectedMenu.items}
                onEdit={openEditItem}
                onAddChild={(item) => {
                  openCreateItem(item.id);
                }}
                onMove={moveItem}
              />
            </div>
          )}
        </main>
      </div>

      <NavigationMenuForm
        menu={editingMenu}
        open={menuFormOpen}
        onClose={() => {
          setMenuFormOpen(false);
        }}
        onSaved={(savedMenu) => {
          setSelectedMenuId(
            savedMenu.id,
          );
        }}
      />

      {selectedMenu && (
        <NavigationItemForm
          menu={selectedMenu}
          item={editingItem}
          suggestedParentId={
            suggestedParentId
          }
          open={itemFormOpen}
          onClose={() => {
            setItemFormOpen(false);
            setEditingItem(null);
            setSuggestedParentId(null);
          }}
        />
      )}

      <NavigationPublicPreview
        slug={
          selectedMenu?.slug ?? null
        }
        open={previewOpen}
        onClose={() => {
          setPreviewOpen(false);
        }}
      />
    </section>
  );
}
