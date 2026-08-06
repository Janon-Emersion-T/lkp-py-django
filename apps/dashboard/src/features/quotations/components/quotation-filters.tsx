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
  quotationStatusLabels,
} from "../formatters";
import {
  quotationOrderingOptions,
  quotationStatuses,
  type QuotationFilters,
  type QuotationOrdering,
  type QuotationStatus,
} from "../types";

const orderingLabels: Record<
  QuotationOrdering,
  string
> = {
  "-created_at": "Newest created",
  created_at: "Oldest created",
  quotation_number:
    "Quotation number A–Z",
  "-quotation_number":
    "Quotation number Z–A",
  issue_date: "Oldest issue date",
  "-issue_date": "Newest issue date",
  expiry_date: "Earliest expiry",
  "-expiry_date": "Latest expiry",
  total_amount: "Lowest value",
  "-total_amount": "Highest value",
  status: "Status A–Z",
  "-status": "Status Z–A",
  updated_at: "Oldest updated",
  "-updated_at": "Recently updated",
};

interface QuotationFiltersProps {
  filters: QuotationFilters;
  onChange: (
    filters: QuotationFilters,
  ) => void;
}

export function QuotationFiltersBar({
  filters,
  onChange,
}: QuotationFiltersProps) {
  function updateFilter(
    changes: Partial<QuotationFilters>,
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
      clientId: "",
      currency: "",
      ordering: "-created_at",
    });
  }

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-[minmax(260px,1.7fr)_1fr_1fr_1fr_auto]">
        <label className="relative">
          <span className="sr-only">
            Search quotations
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
            placeholder="Search number, title, subject or client"
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
                  | QuotationStatus
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All statuses
          </option>

          {quotationStatuses.map(
            (status) => (
              <option
                key={status}
                value={status}
              >
                {
                  quotationStatusLabels[
                    status
                  ]
                }
              </option>
            ),
          )}
        </select>

        <Input
          value={filters.currency}
          maxLength={3}
          onChange={(event) => {
            updateFilter({
              currency:
                event.target.value
                  .toUpperCase(),
            });
          }}
          placeholder="Currency"
          aria-label="Filter by currency"
          className="uppercase dark:border-slate-700 dark:bg-slate-950 dark:text-white"
        />

        <select
          value={filters.ordering}
          aria-label="Order quotations"
          onChange={(event) => {
            updateFilter({
              ordering:
                event.target.value as QuotationOrdering,
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          {quotationOrderingOptions.map(
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
