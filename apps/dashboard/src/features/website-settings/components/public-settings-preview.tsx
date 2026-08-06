import {
  Globe2,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  usePublicWebsiteSettings,
} from "../hooks";

export function PublicSettingsPreview({
  environment,
  open,
  onClose,
}: {
  environment: string;
  open: boolean;
  onClose: () => void;
}) {
  const query =
    usePublicWebsiteSettings(
      environment,
      open,
    );

  if (!open) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close public settings preview"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-3xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
              <Globe2 size={14} />
              Public settings
            </p>

            <h2 className="font-semibold text-slate-950 dark:text-white">
              {environment}
              {" environment"}
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
          >
            <X size={18} />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {query.isLoading && (
            <div className="h-80 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
          )}

          {query.isError && (
            <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {query.error.message}
            </p>
          )}

          {query.data && (
            <pre className="overflow-x-auto rounded-xl border border-slate-200 bg-slate-950 p-5 text-xs leading-6 text-slate-200 dark:border-slate-700">
              {JSON.stringify(
                query.data.settings,
                null,
                2,
              )}
            </pre>
          )}
        </div>
      </aside>
    </>
  );
}
