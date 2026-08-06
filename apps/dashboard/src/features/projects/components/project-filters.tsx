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
  projectPriorityLabels,
  projectStatusLabels,
} from "../formatters";
import {
  projectOrderingOptions,
  projectPriorities,
  projectStatuses,
  type ProjectFilters,
  type ProjectOrdering,
  type ProjectPriority,
  type ProjectStatus,
} from "../types";

const orderingLabels: Record<
  ProjectOrdering,
  string
> = {
  "-created_at": "Newest created",
  created_at: "Oldest created",
  project_code: "Project code A–Z",
  "-project_code": "Project code Z–A",
  title: "Title A–Z",
  "-title": "Title Z–A",
  status: "Status A–Z",
  "-status": "Status Z–A",
  priority: "Priority ascending",
  "-priority": "Priority descending",
  budget: "Lowest budget",
  "-budget": "Highest budget",
  progress: "Lowest progress",
  "-progress": "Highest progress",
  start_date: "Earliest start",
  "-start_date": "Latest start",
  deadline: "Earliest deadline",
  "-deadline": "Latest deadline",
  updated_at: "Oldest updated",
  "-updated_at": "Recently updated",
};

interface ProjectFiltersProps {
  filters: ProjectFilters;
  onChange: (
    filters: ProjectFilters,
  ) => void;
}

export function ProjectFiltersBar({
  filters,
  onChange,
}: ProjectFiltersProps) {
  function updateFilter(
    changes: Partial<ProjectFilters>,
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
      priority: "",
      clientId: "",
      projectManagerId: "",
      ordering: "-created_at",
    });
  }

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-[minmax(260px,1.7fr)_1fr_1fr_1fr_auto]">
        <label className="relative">
          <span className="sr-only">
            Search projects
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
            placeholder="Search code, title, client or description"
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
                  | ProjectStatus
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All statuses
          </option>

          {projectStatuses.map(
            (status) => (
              <option
                key={status}
                value={status}
              >
                {
                  projectStatusLabels[
                    status
                  ]
                }
              </option>
            ),
          )}
        </select>

        <select
          value={filters.priority}
          aria-label="Filter by priority"
          onChange={(event) => {
            updateFilter({
              priority:
                event.target.value as
                  | ProjectPriority
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All priorities
          </option>

          {projectPriorities.map(
            (priority) => (
              <option
                key={priority}
                value={priority}
              >
                {
                  projectPriorityLabels[
                    priority
                  ]
                }
              </option>
            ),
          )}
        </select>

        <select
          value={filters.ordering}
          aria-label="Order projects"
          onChange={(event) => {
            updateFilter({
              ordering:
                event.target.value as ProjectOrdering,
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm text-slate-800 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          {projectOrderingOptions.map(
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
