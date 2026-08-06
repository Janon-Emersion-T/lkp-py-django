import {
  ChevronRight,
  FolderCog,
  Pencil,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import type {
  WebsiteSettingGroup,
} from "../types";

export function SettingGroupList({
  groups,
  selectedGroupId,
  onSelect,
  onEdit,
}: {
  groups: WebsiteSettingGroup[];
  selectedGroupId: string;
  onSelect: (groupId: string) => void;
  onEdit: (
    group: WebsiteSettingGroup,
  ) => void;
}) {
  if (groups.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-white p-10 text-center dark:border-slate-700 dark:bg-slate-900">
        <FolderCog
          size={28}
          className="mx-auto text-slate-400"
        />

        <p className="mt-3 font-medium text-slate-700 dark:text-slate-300">
          No setting groups found.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {groups.map((group) => {
        const selected =
          selectedGroupId
          === group.id;

        return (
          <article
            key={group.id}
            className={
              selected
                ? "rounded-xl border border-blue-300 bg-blue-50 p-4 dark:border-blue-800 dark:bg-blue-950/30"
                : "rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900"
            }
          >
            <div className="flex items-start gap-3">
              <button
                type="button"
                onClick={() => {
                  onSelect(group.id);
                }}
                className="min-w-0 flex-1 text-left"
              >
                <p className="font-semibold text-slate-950 dark:text-white">
                  {group.name}
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  /{group.slug}
                  {" · "}
                  {group.setting_count}
                  {" settings"}
                </p>

                <p className="mt-2 line-clamp-2 text-sm text-slate-600 dark:text-slate-300">
                  {group.description}
                </p>
              </button>

              <Button
                variant="ghost"
                size="icon"
                onClick={() => {
                  onEdit(group);
                }}
                aria-label="Edit group"
              >
                <Pencil size={15} />
              </Button>

              <ChevronRight
                size={17}
                className="mt-2 text-slate-400"
              />
            </div>
          </article>
        );
      })}
    </div>
  );
}
