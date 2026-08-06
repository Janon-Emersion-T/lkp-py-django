import {
  CalendarDays,
  RefreshCw,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  Input,
} from "../../../components/ui/input";
import type {
  DashboardPeriodPreset,
} from "../types";

const periodOptions: readonly {
  value: DashboardPeriodPreset;
  label: string;
}[] = [
  {
    value: "today",
    label: "Today",
  },
  {
    value: "this_week",
    label: "This week",
  },
  {
    value: "this_month",
    label: "This month",
  },
  {
    value: "this_quarter",
    label: "This quarter",
  },
  {
    value: "this_year",
    label: "This year",
  },
  {
    value: "last_7_days",
    label: "Last 7 days",
  },
  {
    value: "last_30_days",
    label: "Last 30 days",
  },
  {
    value: "last_90_days",
    label: "Last 90 days",
  },
  {
    value: "custom",
    label: "Custom range",
  },
];

interface DashboardPeriodFilterProps {
  preset: DashboardPeriodPreset;
  dateFrom: string;
  dateTo: string;
  isFetching: boolean;
  onPresetChange: (
    preset: DashboardPeriodPreset,
  ) => void;
  onDateFromChange: (value: string) => void;
  onDateToChange: (value: string) => void;
  onRefresh: () => void;
}

export function DashboardPeriodFilter({
  preset,
  dateFrom,
  dateTo,
  isFetching,
  onPresetChange,
  onDateFromChange,
  onDateToChange,
  onRefresh,
}: DashboardPeriodFilterProps) {
  const isCustom = preset === "custom";

  return (
    <div className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white p-3 shadow-sm sm:flex-row sm:items-end dark:border-slate-800 dark:bg-slate-900">
      <label className="min-w-44">
        <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
          Reporting period
        </span>

        <div className="relative">
          <CalendarDays
            size={16}
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <select
            value={preset}
            onChange={(event) => {
              onPresetChange(
                event.target.value as DashboardPeriodPreset,
              );
            }}
            className="h-10 w-full appearance-none rounded-md border border-slate-200 bg-white pl-9 pr-8 text-sm text-slate-800 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
          >
            {periodOptions.map((option) => (
              <option
                key={option.value}
                value={option.value}
              >
                {option.label}
              </option>
            ))}
          </select>
        </div>
      </label>

      {isCustom && (
        <>
          <label>
            <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              From
            </span>

            <Input
              type="date"
              value={dateFrom}
              onChange={(event) => {
                onDateFromChange(event.target.value);
              }}
              className="dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            />
          </label>

          <label>
            <span className="mb-1.5 block text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
              To
            </span>

            <Input
              type="date"
              value={dateTo}
              min={dateFrom}
              onChange={(event) => {
                onDateToChange(event.target.value);
              }}
              className="dark:border-slate-700 dark:bg-slate-950 dark:text-white"
            />
          </label>
        </>
      )}

      <Button
        variant="outline"
        onClick={onRefresh}
        disabled={
          isFetching ||
          (
            isCustom &&
            (
              !dateFrom ||
              !dateTo ||
              dateTo < dateFrom
            )
          )
        }
        className="sm:ml-auto dark:border-slate-700 dark:text-slate-200"
      >
        <RefreshCw
          size={16}
          className={
            isFetching
              ? "animate-spin"
              : undefined
          }
        />

        {isFetching
          ? "Refreshing"
          : "Refresh"}
      </Button>
    </div>
  );
}
