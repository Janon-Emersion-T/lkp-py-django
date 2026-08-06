import {
  MenuSquare,
  FileStack,
  Bot,
  BriefcaseBusiness,
  Building2,
  CircleDollarSign,
  FolderKanban,
  FileText,
  LayoutDashboard,
  Settings,
  ShieldCheck,
  UserRoundCog,
  Users,
  type LucideIcon,
  ListChecks,
} from "lucide-react";

export interface DashboardNavigationItem {
  label: string;
  icon: LucideIcon;
  to?: "/dashboard" | "/crm" | "/clients" | "/quotations" | "/projects" | "/tasks" | "/finance" | "/cms" | "/navigation" | "/users" | "/settings";
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
        to: "/crm",
        icon: BriefcaseBusiness,
        available: true,
      },
      {
        label: "Clients",
        to: "/clients",
        icon: Users,
        available: true,
      },
      {
        label: "Quotations",
        to: "/quotations",
        icon: FileText,
        available: true,
      },
      {
        label: "Projects",
        to: "/projects",
        icon: FolderKanban,
        available: true,
      },
      {
        label: "Tasks",
        to: "/tasks",
        icon: ListChecks,
        available: true,
      },
      {
        label: "Finance",
        to: "/finance",
        icon: CircleDollarSign,
        available: true,
      },
      {
        label: "CMS",
        to: "/cms",
        icon: FileStack,
        available: true,
      },
      {
        label: "Navigation",
        to: "/navigation",
        icon: MenuSquare,
        available: true,
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
