import {
  CalendarClock,
  CheckSquare2,
  Clock3,
  MessageSquare,
  UserRound,
} from "lucide-react";

import {
  formatDate,
  formatHours,
  formatUserName,
  isTaskOverdue,
} from "../formatters";
import type {
  Task,
} from "../types";
import {
  TaskPriorityBadge,
} from "./task-badges";
import {
  TaskProgress,
} from "./task-progress";

export function TaskCard({
  task,
  onSelect,
}: {
  task: Task;
  onSelect: (taskId: string) => void;
}) {
  const overdue = isTaskOverdue(
    task.due_date,
    task.status,
  );

  const completedChecklist =
    task.checklist_items.filter(
      (item) => item.is_completed,
    ).length;

  return (
    <button
      type="button"
      onClick={() => {
        onSelect(task.id);
      }}
      className="w-full rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:border-blue-300 hover:shadow-md dark:border-slate-700 dark:bg-slate-900 dark:hover:border-blue-700"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="font-semibold leading-5 text-slate-950 dark:text-white">
            {task.title}
          </h3>

          {task.project_title && (
            <p className="mt-1 truncate text-xs text-slate-500 dark:text-slate-400">
              {task.project_title}
            </p>
          )}
        </div>

        <TaskPriorityBadge
          priority={task.priority}
        />
      </div>

      {task.labels.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-1.5">
          {task.labels
            .slice(0, 3)
            .map((label) => (
              <span
                key={label}
                className="rounded-full bg-slate-100 px-2 py-0.5 text-[11px] font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"
              >
                {label}
              </span>
            ))}
        </div>
      )}

      <div className="mt-4">
        <TaskProgress
          progress={task.progress}
        />
      </div>

      <div className="mt-4 flex items-center gap-3 border-t border-slate-100 pt-3 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
        <span className="flex min-w-0 items-center gap-1.5">
          <UserRound size={13} />
          <span className="truncate">
            {formatUserName(
              task.assignee,
            )}
          </span>
        </span>

        <span
          className={
            overdue
              ? "ml-auto flex shrink-0 items-center gap-1.5 font-semibold text-amber-700 dark:text-amber-400"
              : "ml-auto flex shrink-0 items-center gap-1.5"
          }
        >
          <CalendarClock size={13} />
          {formatDate(task.due_date)}
        </span>
      </div>

      <div className="mt-3 flex items-center gap-4 text-[11px] text-slate-400">
        <span className="flex items-center gap-1">
          <CheckSquare2 size={12} />
          {completedChecklist}/
          {task.checklist_items.length}
        </span>

        <span className="flex items-center gap-1">
          <MessageSquare size={12} />
          {task.comments.length}
        </span>

        <span className="flex items-center gap-1">
          <Clock3 size={12} />
          {formatHours(
            task.actual_hours,
          )}
        </span>
      </div>
    </button>
  );
}
