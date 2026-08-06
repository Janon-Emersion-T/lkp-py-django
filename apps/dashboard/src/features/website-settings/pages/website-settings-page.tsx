import {
  Eye,
  FolderPlus,
  Plus,
  RefreshCw,
  Settings2,
} from "lucide-react";
import {
  useDeferredValue,
  useState,
} from "react";

import {
  PageHeader,
} from "../../../components/layout/page-header";
import {
  Button,
} from "../../../components/ui/button";
import {
  PublicSettingsPreview,
} from "../components/public-settings-preview";
import {
  SettingForm,
} from "../components/setting-form";
import {
  SettingGroupForm,
} from "../components/setting-group-form";
import {
  SettingGroupList,
} from "../components/setting-group-list";
import {
  SettingsFilters,
} from "../components/settings-filters";
import {
  SettingsTable,
} from "../components/settings-table";
import {
  useSettingGroups,
  useWebsiteSettings,
} from "../hooks";
import type {
  WebsiteSetting,
  WebsiteSettingFilters,
  WebsiteSettingGroup,
} from "../types";

const initialFilters:
WebsiteSettingFilters = {
  search: "",
  groupId: "",
  valueType: "",
  environment: "",
  isPublic: null,
  isEditable: null,
  isActive: null,
  ordering: "sort_order",
};

export function WebsiteSettingsPage() {
  const [
    filters,
    setFilters,
  ] = useState(initialFilters);

  const [
    selectedGroupId,
    setSelectedGroupId,
  ] = useState("");

  const [
    groupFormOpen,
    setGroupFormOpen,
  ] = useState(false);

  const [
    editingGroup,
    setEditingGroup,
  ] = useState<WebsiteSettingGroup | null>(
    null,
  );

  const [
    settingFormOpen,
    setSettingFormOpen,
  ] = useState(false);

  const [
    editingSetting,
    setEditingSetting,
  ] = useState<WebsiteSetting | null>(
    null,
  );

  const [
    previewOpen,
    setPreviewOpen,
  ] = useState(false);

  const [
    previewEnvironment,
    setPreviewEnvironment,
  ] = useState("production");

  const deferredSearch =
    useDeferredValue(filters.search);

  const groupsQuery =
    useSettingGroups();

  const settingsQuery =
    useWebsiteSettings({
      ...filters,
      search: deferredSearch,
      groupId:
        selectedGroupId
        || filters.groupId,
    });

  const groups =
    groupsQuery.data ?? [];

  const settings =
    settingsQuery.data ?? [];

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Global website configuration"
          title="Website Settings"
          description="Manage grouped, typed, environment-specific website values, public exposure, editability, validation rules, media references, and runtime configuration."
        />

        <div className="flex flex-wrap gap-2">
          <Button
            variant="outline"
            onClick={() => {
              void groupsQuery.refetch();
              void settingsQuery.refetch();
            }}
            className="dark:border-slate-700"
          >
            <RefreshCw
              size={16}
              className={
                groupsQuery.isFetching
                || settingsQuery.isFetching
                  ? "animate-spin"
                  : undefined
              }
            />
            Refresh
          </Button>

          <Button
            variant="outline"
            onClick={() => {
              setPreviewOpen(true);
            }}
          >
            <Eye size={16} />
            Public preview
          </Button>

          <Button
            variant="outline"
            onClick={() => {
              setEditingGroup(null);
              setGroupFormOpen(true);
            }}
          >
            <FolderPlus size={16} />
            New group
          </Button>

          <Button
            onClick={() => {
              setEditingSetting(null);
              setSettingFormOpen(true);
            }}
            disabled={groups.length === 0}
          >
            <Plus size={16} />
            New setting
          </Button>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[
          [
            "Groups",
            groups.length,
          ],
          [
            "Settings",
            settings.length,
          ],
          [
            "Public",
            settings.filter(
              (setting) =>
                setting.is_public,
            ).length,
          ],
          [
            "Editable",
            settings.filter(
              (setting) =>
                setting.is_editable,
            ).length,
          ],
        ].map(([label, value]) => (
          <article
            key={label}
            className="rounded-xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900"
          >
            <p className="text-sm text-slate-500">
              {label}
            </p>

            <p className="mt-3 text-3xl font-bold text-slate-950 dark:text-white">
              {value}
            </p>
          </article>
        ))}
      </div>

      <SettingsFilters
        filters={filters}
        groups={groups}
        onChange={(nextFilters) => {
          setFilters(nextFilters);

          if (
            nextFilters.groupId
            !== selectedGroupId
          ) {
            setSelectedGroupId(
              nextFilters.groupId,
            );
          }
        }}
      />

      <div className="grid gap-6 xl:grid-cols-[330px_minmax(0,1fr)]">
        <aside>
          {groupsQuery.isLoading ? (
            <div className="h-80 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
          ) : groupsQuery.isError ? (
            <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {groupsQuery.error.message}
            </p>
          ) : (
            <SettingGroupList
              groups={groups}
              selectedGroupId={
                selectedGroupId
              }
              onSelect={(groupId) => {
                setSelectedGroupId(
                  groupId,
                );

                setFilters(
                  (current) => ({
                    ...current,
                    groupId,
                  }),
                );
              }}
              onEdit={(group) => {
                setEditingGroup(group);
                setGroupFormOpen(true);
              }}
            />
          )}
        </aside>

        <main>
          {settingsQuery.isLoading ? (
            <div className="h-96 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
          ) : settingsQuery.isError ? (
            <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {settingsQuery.error.message}
            </p>
          ) : (
            <SettingsTable
              settings={settings}
              onEdit={(setting) => {
                setEditingSetting(
                  setting,
                );
                setSettingFormOpen(
                  true,
                );
              }}
            />
          )}
        </main>
      </div>

      <section className="flex flex-wrap items-center gap-3 rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
        <Settings2
          size={18}
          className="text-slate-400"
        />

        <p className="text-sm text-slate-600 dark:text-slate-300">
          Public preview environment
        </p>

        <select
          value={previewEnvironment}
          onChange={(event) => {
            setPreviewEnvironment(
              event.target.value,
            );
          }}
          className="h-9 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="development">
            Development
          </option>
          <option value="staging">
            Staging
          </option>
          <option value="production">
            Production
          </option>
        </select>
      </section>

      <SettingGroupForm
        group={editingGroup}
        open={groupFormOpen}
        onClose={() => {
          setGroupFormOpen(false);
          setEditingGroup(null);
        }}
      />

      <SettingForm
        setting={editingSetting}
        groups={groups}
        suggestedGroupId={
          selectedGroupId
        }
        open={settingFormOpen}
        onClose={() => {
          setSettingFormOpen(false);
          setEditingSetting(null);
        }}
      />

      <PublicSettingsPreview
        environment={
          previewEnvironment
        }
        open={previewOpen}
        onClose={() => {
          setPreviewOpen(false);
        }}
      />
    </section>
  );
}
