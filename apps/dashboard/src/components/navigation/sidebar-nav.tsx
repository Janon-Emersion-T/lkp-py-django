import { Link } from "@tanstack/react-router";
import { LockKeyhole } from "lucide-react";

import { dashboardNavigation } from "../../config/dashboard-navigation";
import { cn } from "../../lib/utils";

interface SidebarNavProps {
  collapsed?: boolean;
  onNavigate?: () => void;
}

export function SidebarNav({
  collapsed = false,
  onNavigate,
}: SidebarNavProps) {
  return (
    <nav
      aria-label="Dashboard navigation"
      className="space-y-6 px-3 py-4"
    >
      {dashboardNavigation.map((group) => (
        <section key={group.label}>
          {!collapsed && (
            <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wider text-slate-400 dark:text-slate-500">
              {group.label}
            </p>
          )}

          <div className="space-y-1">
            {group.items.map((item) => {
              const Icon = item.icon;

              if (!item.available || !item.to) {
                return (
                  <div
                    key={item.label}
                    aria-disabled="true"
                    title={collapsed ? `${item.label} — Coming soon` : undefined}
                    className={cn(
                      "flex cursor-not-allowed items-center rounded-md px-3 py-2 text-sm font-medium text-slate-400 dark:text-slate-600",
                      collapsed ? "justify-center" : "gap-3",
                    )}
                  >
                    <Icon
                      size={18}
                      aria-hidden="true"
                      className="shrink-0"
                    />

                    {!collapsed && (
                      <>
                        <span className="min-w-0 flex-1 truncate">
                          {item.label}
                        </span>

                        <LockKeyhole
                          size={13}
                          aria-label="Coming soon"
                          className="shrink-0 text-slate-300"
                        />
                      </>
                    )}
                  </div>
                );
              }

              return (
                <Link
                  key={item.to}
                  to={item.to}
                  onClick={onNavigate}
                  title={collapsed ? item.label : undefined}
                  className={cn(
                    "flex items-center rounded-md px-3 py-2 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-100 hover:text-slate-950 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white",
                    collapsed ? "justify-center" : "gap-3",
                  )}
                  activeProps={{
                    className: cn(
                      "flex items-center rounded-md px-3 py-2 text-sm font-medium",
                      "bg-blue-50 text-blue-800 dark:bg-blue-950/60 dark:text-blue-300",
                      collapsed ? "justify-center" : "gap-3",
                    ),
                  }}
                >
                  <Icon
                    size={18}
                    aria-hidden="true"
                    className="shrink-0"
                  />

                  {!collapsed && (
                    <span className="truncate">{item.label}</span>
                  )}
                </Link>
              );
            })}
          </div>
        </section>
      ))}
    </nav>
  );
}
