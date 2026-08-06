import type {
  LucideIcon,
} from "lucide-react";
import type {
  ReactNode,
} from "react";

interface MetricPanelProps {
  title: string;
  description: string;
  icon: LucideIcon;
  children: ReactNode;
}

export function MetricPanel({
  title,
  description,
  icon: Icon,
  children,
}: MetricPanelProps) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <header className="flex items-start gap-3 border-b border-slate-200 px-5 py-4 dark:border-slate-800">
        <span className="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300">
          <Icon
            size={18}
            aria-hidden="true"
          />
        </span>

        <div className="min-w-0">
          <h2 className="font-semibold text-slate-950 dark:text-white">
            {title}
          </h2>

          <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">
            {description}
          </p>
        </div>
      </header>

      <div className="p-5">
        {children}
      </div>
    </section>
  );
}

interface MetricRowProps {
  label: string;
  value: string;
  attention?: boolean;
}

export function MetricRow({
  label,
  value,
  attention = false,
}: MetricRowProps) {
  return (
    <div className="flex items-center justify-between gap-4 border-b border-slate-100 py-3 first:pt-0 last:border-b-0 last:pb-0 dark:border-slate-800">
      <span className="text-sm text-slate-600 dark:text-slate-400">
        {label}
      </span>

      <span
        className={
          attention
            ? "text-sm font-semibold text-amber-700 dark:text-amber-400"
            : "text-sm font-semibold text-slate-950 dark:text-white"
        }
      >
        {value}
      </span>
    </div>
  );
}
