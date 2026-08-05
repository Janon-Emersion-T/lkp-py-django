import {
  Bot,
  BriefcaseBusiness,
  Building2,
  CircleDollarSign,
  FolderKanban,
  LayoutDashboard,
  Settings,
  ShieldCheck,
  UserRoundCog,
  Users,
  type LucideIcon,
} from "lucide-react";

export interface DashboardNavigationItem {
  label: string;
  icon: LucideIcon;
  to?: "/dashboard" | "/users" | "/settings";
  available: boolean;
}

export interface DashboardNavigationGroup {
  label: string;
  items: DashboardNavigationItem[];
}

export const dashboardNavigation: DashboardNavigationGroup[] = [
  {
    label: "Overview",
    items: [
      {
        label: "Dashboard",
        to: "/dashboard",
        icon: LayoutDashboard,
        available: true,
      },
    ],
  },
  {
    label: "Operations",
    items: [
      {
        label: "CRM",
        icon: BriefcaseBusiness,
        available: false,
      },
      {
        label: "Projects",
        icon: FolderKanban,
        available: false,
      },
    ],
  },
  {
    label: "Administration",
    items: [
      {
        label: "Users",
        to: "/users",
        icon: Users,
        available: false,
      },
      {
        label: "Roles & Permissions",
        icon: ShieldCheck,
        available: false,
      },
      {
        label: "Settings",
        to: "/settings",
        icon: Settings,
        available: false,
      },
    ],
  },
  {
    label: "Finance",
    items: [
      {
        label: "Finance",
        icon: CircleDollarSign,
        available: false,
      },
    ],
  },
  {
    label: "Digital Platform",
    items: [
      {
        label: "Website CMS",
        icon: Building2,
        available: false,
      },
      {
        label: "Client Portal",
        icon: UserRoundCog,
        available: false,
      },
      {
        label: "AI Integration",
        icon: Bot,
        available: false,
      },
    ],
  },
];
