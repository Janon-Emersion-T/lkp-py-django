import {
  CircleDollarSign,
} from "lucide-react";

import {
  formatCurrencyAmount,
} from "../formatters";
import type {
  CurrencyAmount,
} from "../types";

interface CurrencyListProps {
  rows: CurrencyAmount[];
  emptyMessage: string;
}

export function CurrencyList({
  rows,
  emptyMessage,
}: CurrencyListProps) {
  if (rows.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center dark:border-slate-700">
        <CircleDollarSign
          size={22}
          className="mx-auto text-slate-300 dark:text-slate-600"
        />

        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          {emptyMessage}
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {rows.map((row) => (
        <div
          key={row.currency}
          className="flex items-center justify-between gap-4 rounded-lg border border-slate-200 px-4 py-3 dark:border-slate-700"
        >
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            {row.currency}
          </span>

          <span className="text-sm font-semibold text-slate-950 dark:text-white">
            {formatCurrencyAmount(
              row.amount,
              row.currency,
            )}
          </span>
        </div>
      ))}
    </div>
  );
}
