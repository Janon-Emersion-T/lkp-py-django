import {
  RotateCcw,
  Search,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  Input,
} from "../../../components/ui/input";
import type {
  CmsContentType,
  CmsFilters,
} from "../types";

export function CmsFiltersBar({
  type,
  filters,
  onChange,
}: {
  type: CmsContentType;
  filters: CmsFilters;
  onChange: (
    filters: CmsFilters,
  ) => void;
}) {
  function update(
    changes: Partial<CmsFilters>,
  ) {
    onChange({
      ...filters,
      ...changes,
      page: 1,
    });
  }

  function reset() {
    onChange({
      page: 1,
      pageSize: 25,
      search: "",
      status: "",
      featured: null,
      active: null,
      ordering: "-updated_at",
    });
  }

  return (
    <div className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 md:grid-cols-2 xl:grid-cols-[minmax(260px,1.7fr)_1fr_1fr_1fr_auto] dark:border-slate-800 dark:bg-slate-900">
      <label className="relative">
        <Search
          size={16}
          className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
        />

        <Input
          value={filters.search}
          onChange={(event) => {
            update({
              search: event.target.value,
            });
          }}
          placeholder="Search content"
          className="pl-9 dark:border-slate-700 dark:bg-slate-950"
        />
      </label>

      <select
        value={filters.status}
        onChange={(event) => {
          update({
            status: event.target.value,
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All statuses
        </option>
        <option value="draft">
          Draft
        </option>
        <option value="scheduled">
          Scheduled
        </option>
        <option value="published">
          Published
        </option>
        <option value="archived">
          Archived
        </option>
      </select>

      <select
        value={
          filters.featured === null
            ? ""
            : String(filters.featured)
        }
        disabled={type === "pages"}
        onChange={(event) => {
          update({
            featured:
              event.target.value === ""
                ? null
                : event.target.value
                  === "true",
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm disabled:opacity-50 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All featured states
        </option>
        <option value="true">
          Featured
        </option>
        <option value="false">
          Not featured
        </option>
      </select>

      <select
        value={
          filters.active === null
            ? ""
            : String(filters.active)
        }
        disabled={type === "pages"}
        onChange={(event) => {
          update({
            active:
              event.target.value === ""
                ? null
                : event.target.value
                  === "true",
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm disabled:opacity-50 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All active states
        </option>
        <option value="true">
          Active
        </option>
        <option value="false">
          Inactive
        </option>
      </select>

      <Button
        variant="outline"
        onClick={reset}
        className="dark:border-slate-700"
      >
        <RotateCcw size={16} />
        Reset
      </Button>
    </div>
  );
}
