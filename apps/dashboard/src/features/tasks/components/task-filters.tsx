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
  taskPriorityLabels,
  taskStatusLabels,
} from "../formatters";
import {
  taskOrderingOptions,
  taskPriorities,
  taskStatuses,
  type TaskFilters,
  type TaskOrdering,
  type TaskPriority,
  type TaskStatus,
} from "../types";

const orderingLabels: Record<
  TaskOrdering,
  string
> = {
  sort_order: "Board order",
  "-sort_order": "Reverse board order",
  title: "Title A–Z",
  "-title": "Title Z–A",
  status: "Status A–Z",
  "-status": "Status Z–A",
  priority: "Priority ascending",
  "-priority": "Priority descending",
  start_date: "Earliest start",
  "-start_date": "Latest start",
  due_date: "Earliest due date",
  "-due_date": "Latest due date",
  progress: "Lowest progress",
  "-progress": "Highest progress",
  created_at: "Oldest created",
  "-created_at": "Newest created",
  updated_at: "Oldest updated",
  "-updated_at": "Recently updated",
};

interface TaskFiltersProps {
  filters: TaskFilters;
  onChange: (
    filters: TaskFilters,
  ) => void;
}

export function TaskFiltersBar({
  filters,
  onChange,
}: TaskFiltersProps) {
  function update(
    changes: Partial<TaskFilters>,
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
      pageSize: 100,
      search: "",
      status: "",
      priority: "",
      projectId: "",
      milestoneId: "",
      assigneeId: "",
      ordering: "sort_order",
    });
  }

  return (
    <section className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-[minmax(260px,1.7fr)_1fr_1fr_1fr_auto]">
        <label className="relative">
          <span className="sr-only">
            Search tasks
          </span>

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
            placeholder="Search title, project or description"
            className="pl-9 dark:border-slate-700 dark:bg-slate-950 dark:text-white"
          />
        </label>

        <select
          value={filters.status}
          aria-label="Filter tasks by status"
          onChange={(event) => {
            update({
              status:
                event.target.value as
                  | TaskStatus
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All statuses
          </option>

          {taskStatuses.map((status) => (
            <option
              key={status}
              value={status}
            >
              {taskStatusLabels[status]}
            </option>
          ))}
        </select>

        <select
          value={filters.priority}
          aria-label="Filter tasks by priority"
          onChange={(event) => {
            update({
              priority:
                event.target.value as
                  | TaskPriority
                  | "",
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All priorities
          </option>

          {taskPriorities.map(
            (priority) => (
              <option
                key={priority}
                value={priority}
              >
                {
                  taskPriorityLabels[
                    priority
                  ]
                }
              </option>
            ),
          )}
        </select>

        <select
          value={filters.ordering}
          aria-label="Order tasks"
          onChange={(event) => {
            update({
              ordering:
                event.target.value as TaskOrdering,
            });
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          {taskOrderingOptions.map(
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
          onClick={reset}
          className="dark:border-slate-700 dark:text-slate-200"
        >
          <RotateCcw size={16} />
          Reset
        </Button>
      </div>
    </section>
  );
}
