import {
  cn,
} from "../../../lib/utils";

const statusClasses: Record<
  string,
  string
> = {
  draft:
    "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300",
  published:
    "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
  scheduled:
    "bg-violet-50 text-violet-700 dark:bg-violet-950/60 dark:text-violet-300",
  archived:
    "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300",
  inactive:
    "bg-red-50 text-red-700 dark:bg-red-950/60 dark:text-red-300",
};

export function ContentStatusBadge({
  status,
}: {
  status: string;
}) {
  const label = status
    .replaceAll("_", " ")
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase(),
    );

  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-1 text-xs font-semibold",
        statusClasses[status]
        ?? statusClasses.draft,
      )}
    >
      {label}
    </span>
  );
}
