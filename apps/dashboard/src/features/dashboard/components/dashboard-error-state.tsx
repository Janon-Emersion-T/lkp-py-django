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

interface DashboardErrorStateProps {
  error: Error;
  onRetry: () => void;
}

export function DashboardErrorState({
  error,
  onRetry,
}: DashboardErrorStateProps) {
  const isForbidden =
    error instanceof ApiError &&
    error.status === 403;

  return (
    <section className="rounded-xl border border-red-200 bg-red-50 p-6 dark:border-red-900 dark:bg-red-950/30">
      <div className="flex items-start gap-4">
        <span className="grid h-11 w-11 shrink-0 place-items-center rounded-xl bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300">
          <AlertTriangle size={21} />
        </span>

        <div className="min-w-0">
          <h2 className="font-semibold text-red-950 dark:text-red-100">
            {isForbidden
              ? "Dashboard access is restricted"
              : "Executive report could not be loaded"}
          </h2>

          <p className="mt-2 text-sm leading-6 text-red-800 dark:text-red-300">
            {isForbidden
              ? "Your account requires the dashboard_reporting.view permission to access enterprise reporting."
              : error.message}
          </p>

          {!isForbidden && (
            <Button
              variant="outline"
              className="mt-4 border-red-300 text-red-800 hover:bg-red-100 dark:border-red-800 dark:text-red-300 dark:hover:bg-red-950"
              onClick={onRetry}
            >
              <RefreshCw size={16} />
              Try again
            </Button>
          )}
        </div>
      </div>
    </section>
  );
}
