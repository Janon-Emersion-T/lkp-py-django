import type {
  LucideIcon,
} from "lucide-react";

interface CrmKpiCardProps {
  label: string;
  value: string;
  description: string;
  icon: LucideIcon;
  attention?: boolean;
}

export function CrmKpiCard({
  label,
  value,
  description,
  icon: Icon,
  attention = false,
}: CrmKpiCardProps) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
            {label}
          </p>

          <p
            className={
              attention
                ? "mt-3 text-3xl font-bold tracking-tight text-amber-700 dark:text-amber-400"
                : "mt-3 text-3xl font-bold tracking-tight text-slate-950 dark:text-white"
            }
          >
            {value}
          </p>
        </div>

        <span
          className={
            attention
              ? "grid h-11 w-11 place-items-center rounded-xl bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300"
              : "grid h-11 w-11 place-items-center rounded-xl bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300"
          }
        >
          <Icon size={20} />
        </span>
      </div>

      <p className="mt-4 text-xs leading-5 text-slate-500 dark:text-slate-400">
        {description}
      </p>
    </article>
  );
}
