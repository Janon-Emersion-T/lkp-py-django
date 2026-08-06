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

export function CmsLoadingState() {
  return (
    <div className="h-80 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
  );
}

export function CmsErrorState({
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
    <div className="rounded-xl border border-red-200 bg-red-50 p-6 dark:border-red-900 dark:bg-red-950/30">
      <div className="flex items-start gap-4">
        <AlertTriangle
          size={22}
          className="text-red-700 dark:text-red-300"
        />

        <div>
          <h2 className="font-semibold text-red-950 dark:text-red-100">
            {forbidden
              ? "CMS access is restricted"
              : "CMS content could not be loaded"}
          </h2>

          <p className="mt-2 text-sm text-red-800 dark:text-red-300">
            {forbidden
              ? "Your account does not have permission to view this content module."
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
    </div>
  );
}
