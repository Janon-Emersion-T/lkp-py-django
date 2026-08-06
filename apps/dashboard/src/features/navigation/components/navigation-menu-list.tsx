import {
  ChevronRight,
  Eye,
  EyeOff,
  Globe2,
  Lock,
  Menu,
} from "lucide-react";

import {
  navigationLocationLabels,
} from "../formatters";
import type {
  NavigationMenu,
} from "../types";

export function NavigationMenuList({
  menus,
  selectedMenuId,
  onSelect,
}: {
  menus: NavigationMenu[];
  selectedMenuId: string | null;
  onSelect: (menuId: string) => void;
}) {
  if (menus.length === 0) {
    return (
      <section className="rounded-xl border border-dashed border-slate-300 bg-white p-10 text-center dark:border-slate-700 dark:bg-slate-900">
        <Menu
          size={28}
          className="mx-auto text-slate-400"
        />

        <p className="mt-3 font-medium text-slate-700 dark:text-slate-300">
          No navigation menus found.
        </p>
      </section>
    );
  }

  return (
    <div className="space-y-3">
      {menus.map((menu) => {
        const selected =
          menu.id === selectedMenuId;

        return (
          <button
            key={menu.id}
            type="button"
            onClick={() => {
              onSelect(menu.id);
            }}
            className={
              selected
                ? "w-full rounded-xl border border-blue-300 bg-blue-50 p-4 text-left shadow-sm dark:border-blue-800 dark:bg-blue-950/30"
                : "w-full rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:border-blue-300 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-blue-800"
            }
          >
            <div className="flex items-start gap-3">
              <span className="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                <Menu size={18} />
              </span>

              <div className="min-w-0 flex-1">
                <div className="flex items-start justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate font-semibold text-slate-950 dark:text-white">
                      {menu.name}
                    </p>

                    <p className="mt-1 truncate text-xs text-slate-500">
                      /{menu.slug}
                    </p>
                  </div>

                  <ChevronRight
                    size={17}
                    className="shrink-0 text-slate-400"
                  />
                </div>

                <p className="mt-3 text-xs font-medium text-slate-500 dark:text-slate-400">
                  {
                    navigationLocationLabels[
                      menu.location
                    ]
                  }
                  {" · "}
                  {menu.item_count} items
                </p>

                <div className="mt-3 flex flex-wrap gap-3 text-xs">
                  <span
                    className={
                      menu.is_active
                        ? "inline-flex items-center gap-1 text-emerald-700 dark:text-emerald-400"
                        : "inline-flex items-center gap-1 text-slate-500"
                    }
                  >
                    {menu.is_active
                      ? <Eye size={13} />
                      : <EyeOff size={13} />}
                    {menu.is_active
                      ? "Active"
                      : "Inactive"}
                  </span>

                  <span
                    className={
                      menu.is_public
                        ? "inline-flex items-center gap-1 text-blue-700 dark:text-blue-400"
                        : "inline-flex items-center gap-1 text-slate-500"
                    }
                  >
                    {menu.is_public
                      ? <Globe2 size={13} />
                      : <Lock size={13} />}
                    {menu.is_public
                      ? "Public"
                      : "Private"}
                  </span>
                </div>
              </div>
            </div>
          </button>
        );
      })}
    </div>
  );
}
