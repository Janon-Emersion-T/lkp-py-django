import {
  cn,
} from "../../../lib/utils";
import {
  clientStatusLabels,
  clientTypeLabels,
} from "../formatters";
import type {
  ClientStatus,
  ClientType,
} from "../types";

const statusClasses: Record<
  ClientStatus,
  string
> = {
  prospect:
    "bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300",
  active:
    "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
  inactive:
    "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400",
  suspended:
    "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300",
  archived:
    "bg-violet-50 text-violet-700 dark:bg-violet-950/60 dark:text-violet-300",
};

export function ClientStatusBadge({
  status,
}: {
  status: ClientStatus;
}) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-1 text-xs font-semibold",
        statusClasses[status],
      )}
    >
      {clientStatusLabels[status]}
    </span>
  );
}

export function ClientTypeBadge({
  clientType,
}: {
  clientType: ClientType;
}) {
  return (
    <span className="text-xs font-medium text-slate-500 dark:text-slate-400">
      {clientTypeLabels[clientType]}
    </span>
  );
}
