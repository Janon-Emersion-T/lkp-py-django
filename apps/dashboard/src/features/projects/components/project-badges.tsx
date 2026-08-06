import {
  cn,
} from "../../../lib/utils";
import {
  projectPriorityLabels,
  projectStatusLabels,
} from "../formatters";
import type {
  ProjectPriority,
  ProjectStatus,
} from "../types";

const statusClasses: Record<
  ProjectStatus,
  string
> = {
  planning:
    "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
  development:
    "bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300",
  testing:
    "bg-cyan-50 text-cyan-700 dark:bg-cyan-950/60 dark:text-cyan-300",
  review:
    "bg-violet-50 text-violet-700 dark:bg-violet-950/60 dark:text-violet-300",
  completed:
    "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
  cancelled:
    "bg-red-50 text-red-700 dark:bg-red-950/60 dark:text-red-300",
};

const priorityClasses: Record<
  ProjectPriority,
  string
> = {
  low: "text-slate-500 dark:text-slate-400",
  normal: "text-blue-700 dark:text-blue-400",
  high: "text-amber-700 dark:text-amber-400",
  urgent: "text-red-700 dark:text-red-400",
};

export function ProjectStatusBadge({
  status,
}: {
  status: ProjectStatus;
}) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-1 text-xs font-semibold",
        statusClasses[status],
      )}
    >
      {projectStatusLabels[status]}
    </span>
  );
}

export function ProjectPriorityBadge({
  priority,
}: {
  priority: ProjectPriority;
}) {
  return (
    <span
      className={cn(
        "text-xs font-semibold",
        priorityClasses[priority],
      )}
    >
      {projectPriorityLabels[priority]}
    </span>
  );
}
