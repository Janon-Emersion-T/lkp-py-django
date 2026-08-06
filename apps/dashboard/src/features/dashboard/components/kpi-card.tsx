import type {
  LucideIcon,
} from "lucide-react";

import {
  cn,
} from "../../../lib/utils";

interface KpiCardProps {
  label: string;
  value: string;
  description: string;
  icon: LucideIcon;
  status?: "default" | "positive" | "attention";
}

const statusClasses = {
  default: {
    icon: "bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300",
    accent: "bg-blue-600",
  },
  positive: {
    icon: "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300",
    accent: "bg-emerald-600",
  },
  attention: {
    icon: "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300",
    accent: "bg-amber-500",
  },
} as const;

export function KpiCard({
  label,
  value,
  description,
  icon: Icon,
  status = "default",
}: KpiCardProps) {
  const classes = statusClasses[status];

  return (
    <article className="relative overflow-hidden rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div
        className={cn(
          "absolute inset-x-0 top-0 h-0.5",
          classes.accent,
        )}
      />

      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
            {label}
          </p>

          <p className="mt-3 text-3xl font-bold tracking-tight text-slate-950 dark:text-white">
            {value}
          </p>
        </div>

        <span
          className={cn(
            "grid h-11 w-11 shrink-0 place-items-center rounded-xl",
            classes.icon,
          )}
        >
          <Icon
            size={21}
            aria-hidden="true"
          />
        </span>
      </div>

      <p className="mt-4 text-xs leading-5 text-slate-500 dark:text-slate-400">
        {description}
      </p>
    </article>
  );
}
