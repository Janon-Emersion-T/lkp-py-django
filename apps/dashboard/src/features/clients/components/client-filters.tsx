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
  clientStatusLabels,
  clientTypeLabels,
} from "../formatters";
import {
  clientOrderingOptions,
  clientStatuses,
  clientTypes,
  type ClientFilters,
  type ClientOrdering,
  type ClientStatus,
  type ClientType,
} from "../types";

const orderingLabels: Record<
  ClientOrdering,
  string
> = {
  company_name: "Company A–Z",
  "-company_name": "Company Z–A",
  client_code: "Client code A–Z",
  "-client_code": "Client code Z–A",
  created_at: "Oldest created",
  "-created_at": "Newest created",
  updated_at: "Oldest updated",
  "-updated_at": "Recently updated",
  country: "Country A–Z",
  "-country": "Country Z–A",
  industry: "Industry A–Z",
  "-industry": "Industry Z–A",
};

interface ClientFiltersProps {
  filters: ClientFilters;
  onChange: (
    filters: ClientFilters,
  ) => void;
}

export function ClientFiltersBar({
  filters,
  onChange,
}: ClientFiltersProps) {
  function updateFilter(
    changes: Partial<ClientFilters>,
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
      clientType: "",
      country: "",
      industry: "",
      ordering: "company_name",
    });
  }

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-[minmax(240px,1.5fr)_1fr_1fr_1fr_1fr_1fr_auto]">
        <label className="relative">
          <span className="sr-only">
            Search clients
          </span>

          <Search
            size={16}
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <Input
            value={filters.search}
            onChange={(event) => {
              updateFilter({
                search:
                  event.target.value,
              });
            }}
            placeholder="Search company, code, email or phone"
            className="pl-9 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
          />
        </label>

        <select
          value={filters.status}
          aria-label="Filter by status"
          onChange={(event) => {
            updateFilter({
              status:
                event.target.value as
                  | ClientStatus
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All statuses
          </option>

          {clientStatuses.map(
            (status) => (
              <option
                key={status}
                value={status}
              >
                {
                  clientStatusLabels[
                    status
                  ]
                }
              </option>
            ),
          )}
        </select>

        <select
          value={filters.clientType}
          aria-label="Filter by client type"
          onChange={(event) => {
            updateFilter({
              clientType:
                event.target.value as
                  | ClientType
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All types
          </option>

          {clientTypes.map(
            (clientType) => (
              <option
                key={clientType}
                value={clientType}
              >
                {
                  clientTypeLabels[
                    clientType
                  ]
                }
              </option>
            ),
          )}
        </select>

        <Input
          value={filters.country}
          onChange={(event) => {
            updateFilter({
              country:
                event.target.value,
            });
          }}
          placeholder="Country"
          aria-label="Filter by country"
          className="dark:border-slate-700 dark:bg-slate-950 dark:text-white"
        />

        <Input
          value={filters.industry}
          onChange={(event) => {
            updateFilter({
              industry:
                event.target.value,
            });
          }}
          placeholder="Industry"
          aria-label="Filter by industry"
          className="dark:border-slate-700 dark:bg-slate-950 dark:text-white"
        />

        <select
          value={filters.ordering}
          aria-label="Order clients"
          onChange={(event) => {
            updateFilter({
              ordering:
                event.target.value as ClientOrdering,
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          {clientOrderingOptions.map(
            (ordering) => (
              <option
                key={ordering}
                value={ordering}
              >
                {
                  orderingLabels[
                    ordering
                  ]
                }
              </option>
            ),
          )}
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
