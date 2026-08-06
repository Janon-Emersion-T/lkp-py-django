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
