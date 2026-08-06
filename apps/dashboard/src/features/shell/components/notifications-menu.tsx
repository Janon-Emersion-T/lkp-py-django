import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import {
  Bell,
  CheckCheck,
  Info,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";

export function NotificationsMenu() {
  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Open notifications"
          title="Notifications"
          className="relative text-slate-600 dark:text-slate-300"
        >
          <Bell size={18} />

          <span
            aria-hidden="true"
            className="absolute right-2 top-2 h-1.5 w-1.5 rounded-full bg-blue-600 ring-2 ring-white dark:ring-slate-900"
          />
        </Button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          align="end"
          sideOffset={8}
          className="z-50 w-[calc(100vw-2rem)] max-w-96 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-xl dark:border-slate-700 dark:bg-slate-900"
        >
          <div className="flex items-center justify-between border-b border-slate-200 px-4 py-3 dark:border-slate-700">
            <div>
              <DropdownMenu.Label className="text-sm font-semibold text-slate-950 dark:text-white">
                Notifications
              </DropdownMenu.Label>

              <p className="mt-0.5 text-xs text-slate-500 dark:text-slate-400">
                Operational alerts and assignments
              </p>
            </div>

            <CheckCheck
              size={17}
              className="text-slate-400"
              aria-hidden="true"
            />
          </div>

          <div className="p-2">
            <div className="flex gap-3 rounded-lg bg-blue-50 p-3 dark:bg-blue-950/40">
              <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300">
                <Info size={17} />
              </span>

              <div className="min-w-0">
                <p className="text-sm font-medium text-slate-900 dark:text-slate-100">
                  Notification centre ready
                </p>

                <p className="mt-1 text-xs leading-5 text-slate-600 dark:text-slate-400">
                  Live notification APIs will be connected in the administration
                  integration milestone.
                </p>
              </div>
            </div>
          </div>

          <div className="border-t border-slate-200 px-4 py-3 text-center dark:border-slate-700">
            <span className="text-xs font-medium text-slate-400">
              No unread operational notifications
            </span>
          </div>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
