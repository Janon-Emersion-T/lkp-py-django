import { Link } from "@tanstack/react-router";
import {
  LayoutDashboard,
  Settings,
  Users,
} from "lucide-react";

import { cn } from "../../lib/utils";

const navigation = [
  {
    label: "Dashboard",
    to: "/dashboard",
    icon: LayoutDashboard,
  },
  {
    label: "Users",
    to: "/users",
    icon: Users,
  },
  {
    label: "Settings",
    to: "/settings",
    icon: Settings,
  },
] as const;

interface SidebarNavProps {
  onNavigate?: () => void;
}

export function SidebarNav({ onNavigate }: SidebarNavProps) {
  return (
    <nav className="space-y-2 p-4">
      {navigation.map((item) => {
        const Icon = item.icon;

        return (
          <Link
            key={item.to}
            to={item.to}
            onClick={onNavigate}
            className="flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100 hover:text-slate-950"
            activeProps={{
              className: cn(
                "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium",
                "bg-blue-50 text-blue-800",
              ),
            }}
          >
            <Icon size={18} />
            {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
