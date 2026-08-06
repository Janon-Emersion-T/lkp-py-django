import {
  Banknote,
  CircleDollarSign,
  Landmark,
  Receipt,
  Scale,
  TrendingDown,
  TrendingUp,
} from "lucide-react";

import {
  formatCurrency,
} from "../formatters";
import {
  useFinanceSummary,
} from "../hooks";

export function FinanceOverview() {
  const summaryQuery =
    useFinanceSummary();

  if (summaryQuery.isLoading) {
    return (
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {Array.from({
          length: 7,
        }).map((_, index) => (
          <div
            key={index}
            className="h-36 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800"
          />
        ))}
      </div>
    );
  }

  if (summaryQuery.isError) {
    return (
      <div className="rounded-xl border border-red-200 bg-red-50 p-5 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
        {summaryQuery.error
          instanceof Error
          ? summaryQuery.error.message
          : "Finance summary could not be loaded."}
      </div>
    );
  }

  const summary = summaryQuery.data;

  if (!summary) {
    return null;
  }

  const metrics = [
    {
      label: "Total assets",
      value: summary.total_assets,
      icon: Landmark,
    },
    {
      label: "Liabilities",
      value: summary.total_liabilities,
      icon: Scale,
    },
    {
      label: "Equity",
      value: summary.total_equity,
      icon: Banknote,
    },
    {
      label: "Total income",
      value: summary.total_income,
      icon: TrendingUp,
    },
    {
      label: "Total expenses",
      value: summary.total_expenses,
      icon: TrendingDown,
    },
    {
      label: "Profit",
      value: summary.profit,
      icon: CircleDollarSign,
    },
    {
      label: "Receivables",
      value: summary.receivables,
      icon: Receipt,
    },
  ];

  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {metrics.map((metric) => {
        const Icon = metric.icon;

        return (
          <article
            key={metric.label}
            className="rounded-xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-900"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
                  {metric.label}
                </p>

                <p className="mt-3 text-2xl font-bold tracking-tight text-slate-950 dark:text-white">
                  {formatCurrency(
                    metric.value,
                  )}
                </p>
              </div>

              <span className="grid h-11 w-11 place-items-center rounded-xl bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300">
                <Icon size={20} />
              </span>
            </div>
          </article>
        );
      })}
    </div>
  );
}
