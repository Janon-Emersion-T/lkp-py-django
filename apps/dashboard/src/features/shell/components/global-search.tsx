import * as Dialog from "@radix-ui/react-dialog";
import {
  ArrowRight,
  Search,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";

const upcomingSearchAreas = [
  "Clients and contacts",
  "Leads and opportunities",
  "Quotations and projects",
  "Tasks and finance records",
  "Website content",
] as const;

export function GlobalSearch() {
  return (
    <Dialog.Root>
      <Dialog.Trigger asChild>
        <Button
          variant="ghost"
          className="hidden h-9 w-64 justify-start gap-2 border border-slate-200 bg-slate-50 px-3 text-slate-500 hover:bg-slate-100 xl:flex dark:border-slate-700 dark:bg-slate-800 dark:text-slate-400 dark:hover:bg-slate-700"
          aria-label="Open global search"
        >
          <Search
            size={16}
            aria-hidden="true"
          />

          <span className="truncate text-sm">
            Search the workspace
          </span>

          <kbd className="ml-auto rounded border border-slate-200 bg-white px-1.5 py-0.5 text-[10px] font-medium text-slate-400 dark:border-slate-600 dark:bg-slate-900">
            /
          </kbd>
        </Button>
      </Dialog.Trigger>

      <Dialog.Trigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="xl:hidden dark:text-slate-300"
          aria-label="Open global search"
        >
          <Search size={18} />
        </Button>
      </Dialog.Trigger>

      <Dialog.Portal>
        <Dialog.Overlay className="fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-sm" />

        <Dialog.Content className="fixed left-1/2 top-[12%] z-50 w-[calc(100%-2rem)] max-w-2xl -translate-x-1/2 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-2xl dark:border-slate-700 dark:bg-slate-900">
          <Dialog.Title className="sr-only">
            Global search
          </Dialog.Title>

          <Dialog.Description className="sr-only">
            Search across the LKProfessionals management platform.
          </Dialog.Description>

          <div className="flex items-center gap-3 border-b border-slate-200 px-4 dark:border-slate-700">
            <Search
              size={20}
              className="shrink-0 text-slate-400"
            />

            <input
              type="search"
              disabled
              placeholder="Global search will be connected feature-by-feature"
              className="h-14 min-w-0 flex-1 bg-transparent text-sm text-slate-950 outline-none placeholder:text-slate-400 disabled:cursor-not-allowed dark:text-white"
            />

            <Dialog.Close asChild>
              <Button
                variant="ghost"
                size="icon"
                aria-label="Close global search"
                className="dark:text-slate-300"
              >
                <X size={18} />
              </Button>
            </Dialog.Close>
          </div>

          <div className="p-5">
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Search coverage roadmap
            </p>

            <div className="mt-3 space-y-2">
              {upcomingSearchAreas.map((area) => (
                <div
                  key={area}
                  className="flex items-center gap-3 rounded-lg border border-slate-200 px-4 py-3 text-sm text-slate-600 dark:border-slate-700 dark:text-slate-300"
                >
                  <ArrowRight
                    size={15}
                    className="shrink-0 text-slate-400"
                  />

                  <span>{area}</span>

                  <span className="ml-auto text-xs font-medium text-slate-400">
                    Planned
                  </span>
                </div>
              ))}
            </div>

            <p className="mt-4 text-xs leading-5 text-slate-500 dark:text-slate-400">
              The shell is ready. Search providers will be registered as each
              business feature is integrated.
            </p>
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
