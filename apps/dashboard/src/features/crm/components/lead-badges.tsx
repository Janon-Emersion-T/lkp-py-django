import {
  cn,
} from "../../../lib/utils";
import {
  leadPriorityLabels,
  leadStatusLabels,
} from "../formatters";
import type {
  LeadPriority,
  LeadStatus,
} from "../types";

const statusClasses: Record<
  LeadStatus,
  string
> = {
  new: "bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300",
  contacted: "bg-cyan-50 text-cyan-700 dark:bg-cyan-950/60 dark:text-cyan-300",
  follow_up: "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300",
  proposal_sent: "bg-violet-50 text-violet-700 dark:bg-violet-950/60 dark:text-violet-300",
  negotiation: "bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300",
  won: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
  lost: "bg-red-50 text-red-700 dark:bg-red-950/60 dark:text-red-300",
  spam: "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400",
};

const priorityClasses: Record<
  LeadPriority,
  string
> = {
  low: "text-slate-500 dark:text-slate-400",
  normal: "text-blue-700 dark:text-blue-400",
  high: "text-amber-700 dark:text-amber-400",
  urgent: "text-red-700 dark:text-red-400",
};

export function LeadStatusBadge({
  status,
}: {
  status: LeadStatus;
}) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-1 text-xs font-semibold",
        statusClasses[status],
      )}
    >
      {leadStatusLabels[status]}
    </span>
  );
}

export function LeadPriorityBadge({
  priority,
}: {
  priority: LeadPriority;
}) {
  return (
    <span
      className={cn(
        "text-xs font-semibold",
        priorityClasses[priority],
      )}
    >
      {leadPriorityLabels[priority]}
    </span>
  );
}
