import * as Dialog from "@radix-ui/react-dialog";
import { Outlet, useNavigate } from "@tanstack/react-router";
import {
  LogOut,
  Menu,
  X,
} from "lucide-react";
import { useEffect, useState } from "react";

import { SidebarNav } from "../components/navigation/sidebar-nav";
import { Button } from "../components/ui/button";
import { useAuth } from "../features/auth/auth-context";

export function DashboardLayout() {
  const navigate = useNavigate();
  const { user, isLoading, isAuthenticated, logout } = useAuth();
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
        <p>Loading dashboard...</p>
      </main>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-950">
      <aside className="fixed inset-y-0 left-0 hidden w-64 border-r border-slate-200 bg-white lg:block">
        <div className="flex h-16 items-center border-b border-slate-200 px-6">
          <span className="font-bold text-blue-800">
            LKProfessionals
          </span>
        </div>

        <SidebarNav />
      </aside>

      <Dialog.Root
        open={mobileMenuOpen}
        onOpenChange={setMobileMenuOpen}
      >
        <Dialog.Portal>
          <Dialog.Overlay className="fixed inset-0 z-40 bg-slate-950/60 lg:hidden" />

          <Dialog.Content className="fixed inset-y-0 left-0 z-50 w-72 bg-white shadow-xl lg:hidden">
            <div className="flex h-16 items-center justify-between border-b border-slate-200 px-6">
              <Dialog.Title className="font-bold text-blue-800">
                LKProfessionals
              </Dialog.Title>

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

            <SidebarNav onNavigate={() => setMobileMenuOpen(false)} />
          </Dialog.Content>
        </Dialog.Portal>
      </Dialog.Root>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between border-b border-slate-200 bg-white px-4 sm:px-6">
          <Button
            variant="ghost"
            size="icon"
            className="lg:hidden"
            aria-label="Open navigation"
            onClick={() => setMobileMenuOpen(true)}
          >
            <Menu size={20} />
          </Button>

          <div className="ml-auto flex items-center gap-4">
            <div className="hidden text-right sm:block">
              <p className="text-sm font-medium text-slate-950">
                {user.email}
              </p>

              <p className="text-xs text-slate-500">
                {user.is_staff ? "Administrator" : "User"}
              </p>
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={handleLogout}
            >
              <LogOut size={16} />
              Sign out
            </Button>
          </div>
        </header>

        <main className="p-4 sm:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
