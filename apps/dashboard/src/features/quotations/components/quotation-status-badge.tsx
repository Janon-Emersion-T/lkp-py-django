import {
  cn,
} from "../../../lib/utils";
import {
  quotationStatusLabels,
} from "../formatters";
import type {
  QuotationStatus,
} from "../types";

const statusClasses: Record<
  QuotationStatus,
  string
> = {
  draft:
    "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300",
  sent:
    "bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300",
  viewed:
    "bg-cyan-50 text-cyan-700 dark:bg-cyan-950/60 dark:text-cyan-300",
  accepted:
    "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
  rejected:
    "bg-red-50 text-red-700 dark:bg-red-950/60 dark:text-red-300",
  expired:
    "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300",
  cancelled:
    "bg-violet-50 text-violet-700 dark:bg-violet-950/60 dark:text-violet-300",
};

export function QuotationStatusBadge({
  status,
}: {
  status: QuotationStatus;
}) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-1 text-xs font-semibold",
        statusClasses[status],
      )}
    >
      {quotationStatusLabels[status]}
    </span>
  );
}
