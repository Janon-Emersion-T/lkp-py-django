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
import {
  navigationLocationLabels,
} from "../formatters";
import {
  navigationLocations,
  type NavigationFilters,
  type NavigationLocation,
  type NavigationOrdering,
} from "../types";

export function NavigationFiltersBar({
  filters,
  onChange,
}: {
  filters: NavigationFilters;
  onChange: (
    filters: NavigationFilters,
  ) => void;
}) {
  function update(
    changes: Partial<NavigationFilters>,
  ) {
    onChange({
      ...filters,
      ...changes,
    });
  }

  function reset() {
    onChange({
      search: "",
      location: "",
      isActive: null,
      isPublic: null,
      ordering: "sort_order",
    });
  }

  return (
    <section className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 md:grid-cols-2 xl:grid-cols-[minmax(240px,1.6fr)_1fr_1fr_1fr_1fr_auto] dark:border-slate-800 dark:bg-slate-900">
      <label className="relative">
        <Search
          size={16}
          className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
        />

        <Input
          value={filters.search}
          onChange={(event) => {
            update({
              search:
                event.target.value,
            });
          }}
          placeholder="Search menus"
          className="pl-9 dark:border-slate-700 dark:bg-slate-950"
        />
      </label>

      <select
        value={filters.location}
        onChange={(event) => {
          update({
            location:
              event.target.value as
                | NavigationLocation
                | "",
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All locations
        </option>

        {navigationLocations.map(
          (location) => (
            <option
              key={location}
              value={location}
            >
              {
                navigationLocationLabels[
                  location
                ]
              }
            </option>
          ),
        )}
      </select>

      <select
        value={
          filters.isActive === null
            ? ""
            : String(filters.isActive)
        }
        onChange={(event) => {
          update({
            isActive:
              event.target.value === ""
                ? null
                : event.target.value
                  === "true",
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
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

      <select
        value={
          filters.isPublic === null
            ? ""
            : String(filters.isPublic)
        }
        onChange={(event) => {
          update({
            isPublic:
              event.target.value === ""
                ? null
                : event.target.value
                  === "true",
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All public states
        </option>
        <option value="true">
          Public
        </option>
        <option value="false">
          Private
        </option>
      </select>

      <select
        value={filters.ordering}
        onChange={(event) => {
          update({
            ordering:
              event.target.value as NavigationOrdering,
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="sort_order">
          Sort order
        </option>
        <option value="name">
          Name A–Z
        </option>
        <option value="-name">
          Name Z–A
        </option>
        <option value="location">
          Location
        </option>
        <option value="-updated_at">
          Recently updated
        </option>
        <option value="-created_at">
          Recently created
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
    </section>
  );
}
