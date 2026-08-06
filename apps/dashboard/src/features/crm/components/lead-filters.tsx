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
  leadSourceLabels,
  leadStatusLabels,
} from "../formatters";
import {
  leadSources,
  leadStatuses,
  type LeadFilters,
  type LeadOrdering,
  type LeadSource,
  type LeadStatus,
} from "../types";

const orderingOptions: readonly {
  value: LeadOrdering;
  label: string;
}[] = [
  {
    value: "-created_at",
    label: "Newest created",
  },
  {
    value: "created_at",
    label: "Oldest created",
  },
  {
    value: "-updated_at",
    label: "Recently updated",
  },
  {
    value: "name",
    label: "Name A–Z",
  },
  {
    value: "-lead_score",
    label: "Highest score",
  },
  {
    value: "-estimated_value",
    label: "Highest estimated value",
  },
  {
    value: "next_follow_up_at",
    label: "Next follow-up",
  },
];

interface LeadFiltersProps {
  filters: LeadFilters;
  onChange: (
    nextFilters: LeadFilters,
  ) => void;
}

export function LeadFiltersBar({
  filters,
  onChange,
}: LeadFiltersProps) {
  function updateFilter(
    changes: Partial<LeadFilters>,
  ) {
    onChange({
      ...filters,
      ...changes,
      page: 1,
    });
  }

  function resetFilters() {
    onChange({
      page: 1,
      pageSize: 25,
      search: "",
      status: "",
      source: "",
      country: "",
      ordering: "-created_at",
    });
  }

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-[minmax(240px,1.6fr)_1fr_1fr_1fr_1fr_auto]">
        <label className="relative">
          <span className="sr-only">
            Search leads
          </span>

          <Search
            size={16}
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <Input
            value={filters.search}
            onChange={(event) => {
              updateFilter({
                search: event.target.value,
              });
            }}
            placeholder="Search name, company, email or phone"
            className="pl-9 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
          />
        </label>

        <select
          aria-label="Filter by status"
          value={filters.status}
          onChange={(event) => {
            updateFilter({
              status:
                event.target.value as
                  | LeadStatus
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All statuses
          </option>

          {leadStatuses.map((status) => (
            <option
              key={status}
              value={status}
            >
              {leadStatusLabels[status]}
            </option>
          ))}
        </select>

        <select
          aria-label="Filter by source"
          value={filters.source}
          onChange={(event) => {
            updateFilter({
              source:
                event.target.value as
                  | LeadSource
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All sources
          </option>

          {leadSources.map((source) => (
            <option
              key={source}
              value={source}
            >
              {leadSourceLabels[source]}
            </option>
          ))}
        </select>

        <Input
          value={filters.country}
          onChange={(event) => {
            updateFilter({
              country: event.target.value,
            });
          }}
          placeholder="Country"
          aria-label="Filter by country"
          className="dark:border-slate-700 dark:bg-slate-950 dark:text-white"
        />

        <select
          aria-label="Order leads"
          value={filters.ordering}
          onChange={(event) => {
            updateFilter({
              ordering:
                event.target.value as LeadOrdering,
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          {orderingOptions.map((option) => (
            <option
              key={option.value}
              value={option.value}
            >
              {option.label}
            </option>
          ))}
        </select>

        <Button
          variant="outline"
          onClick={resetFilters}
          className="dark:border-slate-700 dark:text-slate-200"
        >
          <RotateCcw size={16} />
          Reset
        </Button>
      </div>
    </section>
  );
}
