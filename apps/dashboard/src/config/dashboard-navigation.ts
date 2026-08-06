import {
  DatabaseZap,
  Settings2,
  MenuSquare,
  FileStack,
  Bot,
  BriefcaseBusiness,
  Building2,
  CircleDollarSign,
  FolderKanban,
  FileText,
  LayoutDashboard,
  Images,
  Settings,
  ShieldCheck,
  UserRoundCog,
  Users,
  UsersRound,
  type LucideIcon,
  ListChecks,
  PackageOpen,
  Landmark,
  BookOpenText,
} from "lucide-react";

export interface DashboardNavigationItem {
  label: string;
  icon: LucideIcon;
  to?:
    | "/dashboard"
    | "/crm"
    | "/clients"
    | "/quotations"
    | "/projects"
    | "/tasks"
    | "/finance"
    | "/cms"
    | "/services-catalog"
    | "/packages-catalog"
    | "/industries-catalog"
    | "/insights"
    | "/case-studies"
    | "/media-library"
    | "/navigation"
    | "/public-website-snapshots"
    | "/website-settings"
    | "/team-management"
    | "/users"
    | "/settings";
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
        label: "Services Catalog",
        to: "/services-catalog",
        icon: FileStack,
        available: true,
      },
      {
        label: "Packages Catalog",
        to: "/packages-catalog",
        icon: PackageOpen,
        available: true,
      },
      {
        label: "Industries Catalog",
        to: "/industries-catalog",
        icon: Landmark,
        available: true,
      },
      {
        label: "Insights",
        to: "/insights",
        icon: BookOpenText,
        available: true,
      },
      {
        label: "Case Studies",
        to: "/case-studies",
        icon: BriefcaseBusiness,
        available: true,
      },
      {
        label: "Media Library",
        to: "/media-library",
        icon: Images,
        available: true,
      },
      {
        label: "Navigation",
        to: "/navigation",
        icon: MenuSquare,
        available: true,
      },
      {
        label: "Website Snapshots",
        to: "/public-website-snapshots",
        icon: DatabaseZap,
        available: true,
      },
      {
        label: "Website Settings",
        to: "/website-settings",
        icon: Settings2,
        available: true,
      },
    ],
  },
  {
    label: "Administration",
    items: [
      {
        label: "Team Management",
        to: "/team-management",
        icon: UsersRound,
        available: true,
      },
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
