import type {
  LucideIcon,
} from "lucide-react";

export interface ShellRouteMetadata {
  path: string;
  title: string;
  breadcrumb: string;
  description?: string;
}

export interface NavigationItem {
  label: string;
  icon: LucideIcon;
  to?: string;
  available: boolean;
  badge?: string;
  requiredPermissions?: readonly string[];
}

export interface NavigationGroup {
  label: string;
  items: readonly NavigationItem[];
}
