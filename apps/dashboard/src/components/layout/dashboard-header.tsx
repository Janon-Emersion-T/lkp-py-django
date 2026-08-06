import {
  Menu,
} from "lucide-react";

import type {
  CurrentUser,
} from "../../lib/api";
import {
  GlobalSearch,
} from "../../features/shell/components/global-search";
import {
  NotificationsMenu,
} from "../../features/shell/components/notifications-menu";
import {
  ShellBreadcrumbs,
} from "../../features/shell/components/shell-breadcrumbs";
import {
  ThemeSwitcher,
} from "../../features/shell/components/theme-switcher";
import {
  Button,
} from "../ui/button";
import {
  UserMenu,
} from "./user-menu";

interface DashboardHeaderProps {
  user: CurrentUser;
  onOpenNavigation: () => void;
  onLogout: () => Promise<void>;
}

export function DashboardHeader({
  user,
  onOpenNavigation,
  onLogout,
}: DashboardHeaderProps) {
  return (
    <header className="sticky top-0 z-30 border-b border-slate-200 bg-white/95 backdrop-blur-xl dark:border-slate-800 dark:bg-slate-950/95">
      <div className="flex h-16 items-center gap-2 px-4 sm:px-6">
        <Button
          variant="ghost"
          size="icon"
          className="shrink-0 lg:hidden dark:text-slate-300"
          aria-label="Open navigation"
          onClick={onOpenNavigation}
        >
          <Menu size={20} />
        </Button>

        <div className="min-w-0">
          <ShellBreadcrumbs />
        </div>

        <div className="ml-auto flex shrink-0 items-center gap-1 sm:gap-2">
          <GlobalSearch />
          <ThemeSwitcher />
          <NotificationsMenu />

          <div className="mx-1 hidden h-6 w-px bg-slate-200 sm:block dark:bg-slate-700" />

          <UserMenu
            user={user}
            onLogout={onLogout}
          />
        </div>
      </div>
    </header>
  );
}
