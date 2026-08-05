import * as Dialog from "@radix-ui/react-dialog";
import { Outlet, useNavigate } from "@tanstack/react-router";
import {
  PanelLeftClose,
  PanelLeftOpen,
  X,
} from "lucide-react";
import { useEffect, useState } from "react";

import { DashboardHeader } from "../components/layout/dashboard-header";
import { SidebarNav } from "../components/navigation/sidebar-nav";
import { Button } from "../components/ui/button";
import { useAuth } from "../features/auth/use-auth";
import { useSidebarState } from "../hooks/use-sidebar-state";
import { cn } from "../lib/utils";

export function DashboardLayout() {
  const navigate = useNavigate();
  const { user, isLoading, isAuthenticated, logout } = useAuth();
  const { isCollapsed, toggleSidebar } = useSidebarState();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      void navigate({ to: "/login" });
    }
  }, [isAuthenticated, isLoading, navigate]);

  async function handleLogout() {
    await logout();
    await navigate({ to: "/login" });
  }

  if (isLoading) {
    return (
      <main className="grid min-h-screen place-items-center bg-slate-950 text-white">
        <p className="text-sm font-medium">
          Loading dashboard...
        </p>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-950">
      <aside
        className={cn(
          "fixed inset-y-0 left-0 z-40 hidden border-r border-slate-200 bg-white transition-[width] duration-200 lg:flex lg:flex-col",
          isCollapsed ? "w-20" : "w-64",
        )}
      >
        <div
          className={cn(
            "flex h-16 shrink-0 items-center border-b border-slate-200",
            isCollapsed
              ? "justify-center px-3"
              : "justify-between px-5",
          )}
        >
          <div
            className={cn(
              "min-w-0",
              isCollapsed && "hidden",
            )}
          >
            <p className="truncate font-bold text-blue-800">
              LKProfessionals
            </p>

            <p className="truncate text-xs text-slate-500">
              Management Platform
            </p>
          </div>

          {isCollapsed && (
            <span
              aria-label="LKProfessionals"
              className="grid h-9 w-9 place-items-center rounded-md bg-blue-700 text-sm font-bold text-white"
            >
              LKP
            </span>
          )}
        </div>

        <div className="min-h-0 flex-1 overflow-y-auto">
          <SidebarNav collapsed={isCollapsed} />
        </div>

        <div className="border-t border-slate-200 p-3">
          <Button
            variant="ghost"
            size={isCollapsed ? "icon" : "sm"}
            className={cn(
              isCollapsed ? "w-full" : "w-full justify-start",
            )}
            aria-label={
              isCollapsed
                ? "Expand sidebar"
                : "Collapse sidebar"
            }
            title={
              isCollapsed
                ? "Expand sidebar"
                : "Collapse sidebar"
            }
            onClick={toggleSidebar}
          >
            {isCollapsed ? (
              <PanelLeftOpen size={18} />
            ) : (
              <>
                <PanelLeftClose size={18} />
                Collapse sidebar
              </>
            )}
          </Button>
        </div>
      </aside>

      <Dialog.Root
        open={mobileMenuOpen}
        onOpenChange={setMobileMenuOpen}
      >
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 z-40 bg-slate-950/60 lg:hidden" />

          <Dialog.Content className="fixed inset-y-0 left-0 z-50 flex w-72 flex-col bg-white shadow-xl lg:hidden">
            <div className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 px-5">
              <div>
                <Dialog.Title className="font-bold text-blue-800">
                  LKProfessionals
                </Dialog.Title>

                <Dialog.Description className="text-xs text-slate-500">
                  Management Platform
                </Dialog.Description>
              </div>

              <Dialog.Close asChild>
                <Button
                  variant="ghost"
                  size="icon"
                  aria-label="Close navigation"
                >
                  <X size={20} />
                </Button>
              </Dialog.Close>
            </div>

            <div className="min-h-0 flex-1 overflow-y-auto">
              <SidebarNav
                onNavigate={() => setMobileMenuOpen(false)}
              />
            </div>
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      <div
        className={cn(
          "min-w-0 transition-[padding] duration-200",
          isCollapsed ? "lg:pl-20" : "lg:pl-64",
        )}
      >
        <DashboardHeader
          user={user}
          onOpenNavigation={() => setMobileMenuOpen(true)}
          onLogout={handleLogout}
        />

        <main className="min-w-0 p-4 sm:p-6 lg:p-8">
          <div className="mx-auto w-full max-w-screen-2xl">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
