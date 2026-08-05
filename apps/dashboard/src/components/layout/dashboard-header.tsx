import {
  Bell,
  Menu,
  Search,
} from "lucide-react";

import type { CurrentUser } from "../../lib/api";
import { Button } from "../ui/button";
import { UserMenu } from "./user-menu";

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
    <header className="sticky top-0 z-30 flex h-16 items-center gap-2 border-b border-slate-200 bg-white/95 px-4 backdrop-blur sm:px-6">
      <Button
        variant="ghost"
        size="icon"
        className="lg:hidden"
        aria-label="Open navigation"
        onClick={onOpenNavigation}
      >
        <Menu size={20} />
      </Button>

      <div className="hidden min-w-0 md:block">
        <p className="text-xs font-medium uppercase tracking-wider text-slate-400">
          LKProfessionals
        </p>

        <p className="truncate text-sm font-semibold text-slate-900">
          Management Dashboard
        </p>
      </div>

      <div className="ml-auto flex items-center gap-1 sm:gap-2">
        <Button
          variant="ghost"
          size="icon"
          aria-label="Search — coming soon"
          title="Search — coming soon"
          disabled
        >
          <Search size={18} />
        </Button>

        <Button
          variant="ghost"
          size="icon"
          aria-label="Notifications — coming soon"
          title="Notifications — coming soon"
          disabled
        >
          <Bell size={18} />
        </Button>

        <UserMenu
          user={user}
          onLogout={onLogout}
        />
      </div>
    </header>
  );
}
