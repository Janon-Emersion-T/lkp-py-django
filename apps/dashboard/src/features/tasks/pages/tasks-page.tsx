import {
  CheckCircle2,
  ClockAlert,
  ListChecks,
  RefreshCw,
  Timer,
} from "lucide-react";
import {
  useDeferredValue,
  useMemo,
  useState,
} from "react";

import {
  PageHeader,
} from "../../../components/layout/page-header";
import {
  Button,
} from "../../../components/ui/button";
import {
  TaskFiltersBar,
} from "../components/task-filters";
import {
  TaskKanbanBoard,
} from "../components/task-kanban-board";
import {
  TaskDetailPanel,
} from "../components/task-detail-panel";
import {
  TaskErrorState,
  TaskLoadingState,
} from "../components/task-states";
import {
  formatCount,
  formatHours,
  isTaskOverdue,
} from "../formatters";
import {
  useTasks,
} from "../hooks";
import type {
  TaskFilters,
} from "../types";

const initialFilters: TaskFilters = {
  page: 1,
  pageSize: 100,
  search: "",
  status: "",
  priority: "",
  projectId: "",
  milestoneId: "",
  assigneeId: "",
  ordering: "sort_order",
};

export function TasksPage() {
  const [
    filters,
    setFilters,
  ] = useState<TaskFilters>(
    initialFilters,
  );

  const [
    selectedTaskId,
    setSelectedTaskId,
  ] = useState<string | null>(null);

  const deferredSearch =
    useDeferredValue(filters.search);

  const taskQuery = useTasks({
    ...filters,
    search: deferredSearch,
  });

  const metrics = useMemo(() => {
    const tasks =
      taskQuery.data?.items ?? [];

    const actualHours = tasks.reduce(
      (total, task) =>
        total
        + Number(task.actual_hours),
      0,
    );

    return {
      open: tasks.filter(
        (task) =>
          task.status !== "completed"
          && task.status !== "cancelled",
      ).length,
      completed: tasks.filter(
        (task) =>
          task.status === "completed",
      ).length,
      overdue: tasks.filter(
        (task) =>
          isTaskOverdue(
            task.due_date,
            task.status,
          ),
      ).length,
      actualHours,
    };
  }, [taskQuery.data]);

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Delivery execution"
          title="Tasks and Kanban"
          description="Track task status, priorities, progress, assignees, deadlines, checklists, comments, dependencies, watchers, and logged time."
        />

        <Button
          variant="outline"
          onClick={() => {
            void taskQuery.refetch();
          }}
          disabled={taskQuery.isFetching}
          className="self-start dark:border-slate-700 dark:text-slate-200"
        >
          <RefreshCw
            size={16}
            className={
              taskQuery.isFetching
                ? "animate-spin"
                : undefined
            }
          />
          Refresh tasks
        </Button>
      </div>

      {taskQuery.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[
            {
              label: "Total tasks",
              value: formatCount(
                taskQuery.data
                  .pagination
                  .total_items,
              ),
              description:
                "All tasks matching the active filters",
              icon: ListChecks,
              attention: false,
            },
            {
              label: "Open on board",
              value: formatCount(
                metrics.open,
              ),
              description:
                "Tasks still moving through delivery",
              icon: Timer,
              attention: false,
            },
            {
              label: "Completed",
              value: formatCount(
                metrics.completed,
              ),
              description:
                "Completed tasks in the loaded board",
              icon: CheckCircle2,
              attention: false,
            },
            {
              label: "Overdue",
              value: formatCount(
                metrics.overdue,
              ),
              description: `${formatHours(
                String(metrics.actualHours),
              )} logged across loaded tasks`,
              icon: ClockAlert,
              attention:
                metrics.overdue > 0,
            },
          ].map((metric) => {
            const Icon = metric.icon;

            return (
              <article
                key={metric.label}
                className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900"
              >
                <div className="flex justify-between gap-4">
                  <div>
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      {metric.label}
                    </p>

                    <p
                      className={
                        metric.attention
                          ? "mt-3 text-3xl font-bold text-amber-700 dark:text-amber-400"
                          : "mt-3 text-3xl font-bold text-slate-950 dark:text-white"
                      }
                    >
                      {metric.value}
                    </p>
                  </div>

                  <Icon
                    size={22}
                    className={
                      metric.attention
                        ? "text-amber-600"
                        : "text-blue-600"
                    }
                  />
                </div>

                <p className="mt-4 text-xs text-slate-500 dark:text-slate-400">
                  {metric.description}
                </p>
              </article>
            );
          })}
        </div>
      )}

      <TaskFiltersBar
        filters={filters}
        onChange={setFilters}
      />

      <div className="overflow-hidden">
        {taskQuery.isLoading && (
          <div className="overflow-x-auto">
            <TaskLoadingState />
          </div>
        )}

        {taskQuery.isError && (
          <TaskErrorState
            error={
              taskQuery.error
              instanceof Error
                ? taskQuery.error
                : new Error(
                  "An unknown task error occurred.",
                )
            }
            onRetry={() => {
              void taskQuery.refetch();
            }}
          />
        )}

        {taskQuery.data && (
          <TaskKanbanBoard
            tasks={taskQuery.data.items}
            onSelect={setSelectedTaskId}
          />
        )}
      </div>

      {taskQuery.data
        && taskQuery.data.pagination
          .total_pages > 1 && (
        <p className="rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800 dark:border-amber-900 dark:bg-amber-950/30 dark:text-amber-300">
          The Kanban board currently shows page{" "}
          {
            taskQuery.data.pagination
              .page
          }{" "}
          of{" "}
          {
            taskQuery.data.pagination
              .total_pages
          }.
          Narrow the filters to manage a smaller operational board.
        </p>
      )}

      <TaskDetailPanel
        taskId={selectedTaskId}
        onClose={() => {
          setSelectedTaskId(null);
        }}
      />
    </section>
  );
}
