import {
  taskStatusLabels,
} from "../formatters";
import {
  taskStatuses,
  type Task,
  type TaskStatus,
} from "../types";
import {
  TaskCard,
} from "./task-card";

const visibleColumns = taskStatuses.filter(
  (status) => status !== "cancelled",
);

export function TaskKanbanBoard({
  tasks,
  onSelect,
}: {
  tasks: Task[];
  onSelect: (taskId: string) => void;
}) {
  const grouped = visibleColumns.reduce<
    Record<TaskStatus, Task[]>
  >(
    (result, status) => ({
      ...result,
      [status]: tasks
        .filter(
          (task) =>
            task.status === status,
        )
        .sort(
          (left, right) =>
            left.sort_order
            - right.sort_order,
        ),
    }),
    {
      todo: [],
      in_progress: [],
      testing: [],
      review: [],
      completed: [],
      cancelled: [],
    },
  );

  return (
    <section className="overflow-x-auto pb-3">
      <div className="grid min-w-[1500px] grid-cols-5 gap-4">
        {visibleColumns.map((status) => (
          <section
            key={status}
            className="rounded-xl bg-slate-100/70 p-3 dark:bg-slate-800/50"
          >
            <header className="mb-3 flex items-center justify-between gap-3 px-1">
              <h2 className="text-sm font-semibold text-slate-800 dark:text-slate-200">
                {taskStatusLabels[status]}
              </h2>

              <span className="rounded-full bg-white px-2 py-0.5 text-xs font-semibold text-slate-600 shadow-sm dark:bg-slate-900 dark:text-slate-300">
                {grouped[status].length}
              </span>
            </header>

            <div className="space-y-3">
              {grouped[status].map(
                (task) => (
                  <TaskCard
                    key={task.id}
                    task={task}
                    onSelect={onSelect}
                  />
                ),
              )}

              {grouped[status].length
                === 0 && (
                <p className="rounded-lg border border-dashed border-slate-300 px-3 py-8 text-center text-xs text-slate-400 dark:border-slate-700">
                  No tasks
                </p>
              )}
            </div>
          </section>
        ))}
      </div>
    </section>
  );
}
