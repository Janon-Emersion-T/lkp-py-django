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

export function CrmLoadingState() {
  return (
    <div className="space-y-3">
      {Array.from({
        length: 6,
      }).map((_, index) => (
        <div
          key={index}
          className="h-20 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800"
        />
      ))}
    </div>
  );
}

export function CrmErrorState({
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
        <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300">
          <AlertTriangle size={20} />
        </span>

        <div>
          <h2 className="font-semibold text-red-950 dark:text-red-100">
            {forbidden
              ? "CRM access is restricted"
              : "CRM records could not be loaded"}
          </h2>

          <p className="mt-2 text-sm leading-6 text-red-800 dark:text-red-300">
            {forbidden
              ? "Your account requires the crm.view_lead permission."
              : error.message}
          </p>

          {!forbidden && (
            <Button
              variant="outline"
              onClick={onRetry}
              className="mt-4 border-red-300 text-red-800 hover:bg-red-100 dark:border-red-800 dark:text-red-300"
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
