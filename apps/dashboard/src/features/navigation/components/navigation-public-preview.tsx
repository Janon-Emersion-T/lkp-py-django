import {
  ExternalLink,
  Globe2,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  usePublicNavigationMenu,
} from "../hooks";
import type {
  PublicNavigationMenuItem,
} from "../types";

function PreviewItems({
  items,
  depth = 0,
}: {
  items: PublicNavigationMenuItem[];
  depth?: number;
}) {
  return (
    <ul
      className={
        depth === 0
          ? "space-y-2"
          : "ml-5 mt-2 space-y-2 border-l border-slate-200 pl-4 dark:border-slate-700"
      }
    >
      {items.map((item) => (
        <li key={item.id}>
          <div className="flex items-center gap-2 rounded-lg bg-slate-50 px-3 py-2 text-sm dark:bg-slate-800">
            <span className="font-medium text-slate-800 dark:text-slate-200">
              {item.label}
            </span>

            {item.is_featured && (
              <span className="rounded-full bg-amber-50 px-2 py-0.5 text-[10px] font-semibold text-amber-700 dark:bg-amber-950/60 dark:text-amber-300">
                Featured
              </span>
            )}

            {item.target_blank && (
              <ExternalLink
                size={12}
                className="text-slate-400"
              />
            )}

            <span className="ml-auto max-w-56 truncate text-xs text-slate-500">
              {item.url}
            </span>
          </div>

          {item.children.length > 0 && (
            <PreviewItems
              items={item.children}
              depth={depth + 1}
            />
          )}
        </li>
      ))}
    </ul>
  );
}

export function NavigationPublicPreview({
  slug,
  open,
  onClose,
}: {
  slug: string | null;
  open: boolean;
  onClose: () => void;
}) {
  const query =
    usePublicNavigationMenu(
      slug,
      open,
    );

  if (!open) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close public preview"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-2xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
              <Globe2 size={14} />
              Public navigation
            </p>

            <h2 className="font-semibold text-slate-950 dark:text-white">
              Live menu preview
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
          >
            <X size={18} />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {query.isLoading && (
            <div className="h-80 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
          )}

          {query.isError && (
            <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {query.error.message}
            </p>
          )}

          {query.data && (
            <div>
              <h3 className="text-xl font-bold text-slate-950 dark:text-white">
                {query.data.name}
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                {query.data.location}
                {" · "}
                /{query.data.slug}
              </p>

              {query.data.description && (
                <p className="mt-4 text-sm leading-6 text-slate-600 dark:text-slate-300">
                  {
                    query.data.description
                  }
                </p>
              )}

              <div className="mt-6">
                <PreviewItems
                  items={query.data.items}
                />
              </div>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
