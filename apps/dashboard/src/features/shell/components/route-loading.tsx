import {
  LoaderCircle,
} from "lucide-react";

export function RouteLoading() {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-label="Loading dashboard workspace"
      className="flex min-h-[60vh] items-center justify-center px-6 py-16"
    >
      <div className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-8 text-center shadow-sm dark:border-slate-800 dark:bg-slate-900">
        <div className="mx-auto flex size-12 items-center justify-center rounded-xl bg-blue-50 text-blue-600 dark:bg-blue-950/40 dark:text-blue-300">
          <LoaderCircle
            size={24}
            className="animate-spin"
          />
        </div>

        <h2 className="mt-5 text-base font-semibold text-slate-950 dark:text-white">
          Loading workspace
        </h2>

        <p className="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">
          The requested dashboard module is being loaded.
        </p>

        <div className="mt-6 space-y-3">
          <div className="h-3 animate-pulse rounded-full bg-slate-100 dark:bg-slate-800" />
          <div className="mx-auto h-3 w-4/5 animate-pulse rounded-full bg-slate-100 dark:bg-slate-800" />
          <div className="mx-auto h-3 w-3/5 animate-pulse rounded-full bg-slate-100 dark:bg-slate-800" />
        </div>
      </div>
    </div>
  );
}
