import type {
  ShellRouteMetadata,
} from "./types/navigation";

export const shellRouteMetadata = [
  {
    path: "/dashboard",
    title: "Executive Dashboard",
    breadcrumb: "Dashboard",
    description: "Enterprise performance and operational overview.",
  },
  {
    path: "/crm",
    title: "CRM Leads",
    breadcrumb: "CRM",
    description: "Lead pipeline, follow-ups, ownership, and conversion management.",
  },
  {
    path: "/clients",
    title: "Clients",
    breadcrumb: "Clients",
    description: "Client organisations, contacts, websites, and commercial settings.",
  },
  {
    path: "/quotations",
    title: "Quotations",
    breadcrumb: "Quotations",
    description: "Sales quotations, recipients, validity, pricing, and acceptance.",
  },
  {
    path: "/projects",
    title: "Projects",
    breadcrumb: "Projects",
    description: "Project execution, milestones, teams, budgets, and delivery progress.",
  },
  {
    path: "/tasks",
    title: "Tasks and Kanban",
    breadcrumb: "Tasks",
    description: "Task execution, Kanban status, assignees, deadlines, checklists, and time tracking.",
  },
  {
    path: "/finance",
    title: "Finance",
    breadcrumb: "Finance",
    description: "Accounts, transactions, invoices, payments, expenses, receivables, and profitability.",
  },
  {
    path: "/cms",
    title: "CMS Content Hub",
    breadcrumb: "CMS",
    description: "Website pages, services, packages, industries, insights, case studies, and testimonials.",
  },
  {
    path: "/navigation",
    title: "Navigation Management",
    breadcrumb: "Navigation",
    description: "Website menus, nested links, locations, visibility, hierarchy, ordering, and public previews.",
  },
  {
    path: "/website-settings",
    title: "Website Settings",
    breadcrumb: "Website Settings",
    description: "Grouped, typed, environment-specific website configuration and public runtime values.",
  },
  {
    path: "/users",
    title: "Users",
    breadcrumb: "Users",
    description: "User accounts, roles, permissions, and access controls.",
  },
  {
    path: "/settings",
    title: "Settings",
    breadcrumb: "Settings",
    description: "Company, platform, security, and integration settings.",
  },
] as const satisfies readonly ShellRouteMetadata[];

export function getShellRouteMetadata(
  pathname: string,
): ShellRouteMetadata | undefined {
  const exactMatch = shellRouteMetadata.find(
    (route) => route.path === pathname,
  );

  if (exactMatch) {
    return exactMatch;
  }

  return [...shellRouteMetadata]
    .sort((left, right) => right.path.length - left.path.length)
    .find((route) => pathname.startsWith(`${route.path}/`));
}
