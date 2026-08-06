import {
  Link,
  useRouterState,
} from "@tanstack/react-router";
import {
  ChevronRight,
  Home,
} from "lucide-react";

import {
  getShellRouteMetadata,
} from "../route-metadata";

export function ShellBreadcrumbs() {
  const pathname = useRouterState({
    select: (state) => state.location.pathname,
  });

  const metadata = getShellRouteMetadata(pathname);

  if (pathname === "/dashboard") {
    return (
      <nav
        aria-label="Breadcrumb"
        className="flex min-w-0 items-center gap-2 text-xs text-slate-500 dark:text-slate-400"
      >
        <Home
          size={14}
          aria-hidden="true"
        />

        <span className="truncate font-medium text-slate-700 dark:text-slate-200">
          Dashboard
        </span>
      </nav>
    );
  }

  return (
    <nav
      aria-label="Breadcrumb"
      className="flex min-w-0 items-center gap-2 text-xs text-slate-500 dark:text-slate-400"
    >
      <Link
        to="/dashboard"
        className="flex shrink-0 items-center gap-1.5 transition-colors hover:text-slate-950 dark:hover:text-white"
      >
        <Home
          size={14}
          aria-hidden="true"
        />

        <span className="hidden sm:inline">
          Dashboard
        </span>
      </Link>

      <ChevronRight
        size={13}
        className="shrink-0 text-slate-300 dark:text-slate-600"
        aria-hidden="true"
      />

      <span className="truncate font-medium text-slate-700 dark:text-slate-200">
        {metadata?.breadcrumb ?? "Workspace"}
      </span>
    </nav>
  );
}
