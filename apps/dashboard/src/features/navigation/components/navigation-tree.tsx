import {
  ArrowDown,
  ArrowUp,
  ChevronDown,
  ChevronRight,
  ExternalLink,
  Eye,
  EyeOff,
  Pencil,
  Plus,
  Star,
} from "lucide-react";
import {
  useState,
} from "react";

import {
  Button,
} from "../../../components/ui/button";
import {
  navigationLinkTypeLabels,
  navigationVisibilityLabels,
} from "../formatters";
import type {
  NavigationMenuItem,
} from "../types";

function NavigationTreeNode({
  item,
  siblingIndex,
  siblingCount,
  onEdit,
  onAddChild,
  onMove,
}: {
  item: NavigationMenuItem;
  siblingIndex: number;
  siblingCount: number;
  onEdit: (
    item: NavigationMenuItem,
  ) => void;
  onAddChild: (
    item: NavigationMenuItem,
  ) => void;
  onMove: (
    item: NavigationMenuItem,
    direction: "up" | "down",
  ) => void;
}) {
  const [
    expanded,
    setExpanded,
  ] = useState(true);

  const hasChildren =
    item.children.length > 0;

  return (
    <div>
      <article className="rounded-xl border border-slate-200 bg-white p-3 shadow-sm dark:border-slate-700 dark:bg-slate-900">
        <div className="flex items-start gap-3">
          <button
            type="button"
            disabled={!hasChildren}
            onClick={() => {
              setExpanded(
                (current) => !current,
              );
            }}
            aria-label={
              expanded
                ? "Collapse children"
                : "Expand children"
            }
            className="mt-1 grid h-7 w-7 shrink-0 place-items-center rounded text-slate-400 hover:bg-slate-100 disabled:opacity-30 dark:hover:bg-slate-800"
          >
            {expanded
              ? <ChevronDown size={15} />
              : <ChevronRight size={15} />}
          </button>

          <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
              <p className="font-semibold text-slate-950 dark:text-white">
                {item.label}
              </p>

              {item.is_featured && (
                <Star
                  size={14}
                  className="text-amber-500"
                />
              )}

              {item.target_blank && (
                <ExternalLink
                  size={13}
                  className="text-slate-400"
                />
              )}
            </div>

            <p className="mt-1 truncate text-xs text-slate-500">
              {item.resolved_url
                || item.url
                || "No resolved URL"}
            </p>

            <div className="mt-2 flex flex-wrap gap-2 text-[11px]">
              <span className="rounded-full bg-blue-50 px-2 py-0.5 font-medium text-blue-700 dark:bg-blue-950/60 dark:text-blue-300">
                {
                  navigationLinkTypeLabels[
                    item.link_type
                  ]
                }
              </span>

              <span className="rounded-full bg-slate-100 px-2 py-0.5 font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                {
                  navigationVisibilityLabels[
                    item.visibility
                  ]
                }
              </span>

              <span
                className={
                  item.is_active
                    ? "inline-flex items-center gap-1 text-emerald-700 dark:text-emerald-400"
                    : "inline-flex items-center gap-1 text-slate-500"
                }
              >
                {item.is_active
                  ? <Eye size={12} />
                  : <EyeOff size={12} />}
                {item.is_active
                  ? "Active"
                  : "Inactive"}
              </span>

              <span className="text-slate-400">
                Order {item.sort_order}
              </span>
            </div>
          </div>

          <div className="flex shrink-0 flex-wrap justify-end gap-1">
            <Button
              variant="ghost"
              size="icon"
              disabled={siblingIndex === 0}
              onClick={() => {
                onMove(item, "up");
              }}
              aria-label="Move item up"
            >
              <ArrowUp size={15} />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              disabled={
                siblingIndex
                === siblingCount - 1
              }
              onClick={() => {
                onMove(item, "down");
              }}
              aria-label="Move item down"
            >
              <ArrowDown size={15} />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => {
                onAddChild(item);
              }}
              aria-label="Add child item"
            >
              <Plus size={15} />
            </Button>

            <Button
              variant="ghost"
              size="icon"
              onClick={() => {
                onEdit(item);
              }}
              aria-label="Edit item"
            >
              <Pencil size={15} />
            </Button>
          </div>
        </div>
      </article>

      {hasChildren && expanded && (
        <div className="ml-5 mt-3 space-y-3 border-l border-slate-200 pl-4 dark:border-slate-700">
          {item.children.map(
            (child, index) => (
              <NavigationTreeNode
                key={child.id}
                item={child}
                siblingIndex={index}
                siblingCount={
                  item.children.length
                }
                onEdit={onEdit}
                onAddChild={onAddChild}
                onMove={onMove}
              />
            ),
          )}
        </div>
      )}
    </div>
  );
}

export function NavigationTree({
  items,
  onEdit,
  onAddChild,
  onMove,
}: {
  items: NavigationMenuItem[];
  onEdit: (
    item: NavigationMenuItem,
  ) => void;
  onAddChild: (
    item: NavigationMenuItem,
  ) => void;
  onMove: (
    item: NavigationMenuItem,
    direction: "up" | "down",
  ) => void;
}) {
  if (items.length === 0) {
    return (
      <section className="rounded-xl border border-dashed border-slate-300 bg-white p-10 text-center dark:border-slate-700 dark:bg-slate-900">
        <p className="font-medium text-slate-700 dark:text-slate-300">
          This menu has no items.
        </p>
      </section>
    );
  }

  return (
    <div className="space-y-3">
      {items.map((item, index) => (
        <NavigationTreeNode
          key={item.id}
          item={item}
          siblingIndex={index}
          siblingCount={items.length}
          onEdit={onEdit}
          onAddChild={onAddChild}
          onMove={onMove}
        />
      ))}
    </div>
  );
}
