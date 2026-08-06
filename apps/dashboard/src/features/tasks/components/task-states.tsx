import {
  AlertTriangle,
  RefreshCw,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  ApiError,
} from "../../../lib/http";

export function TaskLoadingState() {
  return (
    <div className="grid min-w-[1200px] grid-cols-5 gap-4">
      {Array.from({
        length: 5,
      }).map((_, column) => (
        <div
          key={column}
          className="rounded-xl bg-slate-100 p-3 dark:bg-slate-800"
        >
          <div className="h-5 w-24 animate-pulse rounded bg-slate-200 dark:bg-slate-700" />

          <div className="mt-4 space-y-3">
            {Array.from({
              length: 3,
            }).map((__, card) => (
              <div
                key={card}
                className="h-36 animate-pulse rounded-xl bg-white dark:bg-slate-900"
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

export function TaskErrorState({
  error,
  onRetry,
}: {
  error: Error;
  onRetry: () => void;
}) {
  const forbidden =
    error instanceof ApiError
    && error.status === 403;

  return (
    <section className="rounded-xl border border-red-200 bg-red-50 p-6 dark:border-red-900 dark:bg-red-950/30">
      <div className="flex items-start gap-4">
        <AlertTriangle
          size={22}
          className="text-red-700 dark:text-red-300"
        />

        <div>
          <h2 className="font-semibold text-red-950 dark:text-red-100">
            {forbidden
              ? "Task access is restricted"
              : "Tasks could not be loaded"}
          </h2>

          <p className="mt-2 text-sm text-red-800 dark:text-red-300">
            {forbidden
              ? "Your account requires the tasks.view_task permission."
              : error.message}
          </p>

          {!forbidden && (
            <Button
              variant="outline"
              onClick={onRetry}
              className="mt-4"
            >
              <RefreshCw size={16} />
              Retry
            </Button>
          )}
        </div>
      </div>
    </section>
  );
}
