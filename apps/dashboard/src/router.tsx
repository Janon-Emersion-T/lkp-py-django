import {
  lazy,
  Suspense,
  type ComponentType,
  type LazyExoticComponent,
} from "react";
import {
  createRootRoute,
  createRoute,
  createRouter,
  Navigate,
  Outlet,
} from "@tanstack/react-router";

import { RouteLoading } from "./features/shell/components/route-loading";
import { DashboardLayout } from "./layouts/dashboard-layout";
import { LoginPage } from "./routes/auth/login";
import { NotFoundPage } from "./routes/errors/not-found";

type RoutePageComponent = LazyExoticComponent<
  ComponentType<Record<string, never>>
>;

function withRouteSuspense(Component: RoutePageComponent) {
  return function LazyRoutePage() {
    return (
      <Suspense fallback={<RouteLoading />}>
        <Component />
      </Suspense>
    );
  };
}

const DashboardPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/dashboard");

    return {
      default: module.DashboardPage,
    };
  }),
);

const CrmPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/crm");

    return {
      default: module.CrmPage,
    };
  }),
);

const ClientsPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/clients");

    return {
      default: module.ClientsPage,
    };
  }),
);

const QuotationsPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/quotations");

    return {
      default: module.QuotationsPage,
    };
  }),
);

const ProjectsPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/projects");

    return {
      default: module.ProjectsPage,
    };
  }),
);

const TasksPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/tasks");

    return {
      default: module.TasksPage,
    };
  }),
);

const FinancePage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/finance");

    return {
      default: module.FinancePage,
    };
  }),
);

const CmsPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/cms");

    return {
      default: module.CmsPage,
    };
  }),
);

const NavigationPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/navigation");

    return {
      default: module.NavigationPage,
    };
  }),
);

const ServicesCatalogPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/services-catalog");

    return {
      default: module.ServicesCatalogPage,
    };
  }),
);

const PackagesCatalogPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/packages-catalog");

    return {
      default: module.PackagesCatalogPage,
    };
  }),
);

const MediaLibraryPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/media-library");

    return {
      default: module.MediaLibraryPage,
    };
  }),
);

const PublicWebsiteSnapshotsPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/public-website-snapshots");

    return {
      default: module.PublicWebsiteSnapshotsPage,
    };
  }),
);

const WebsiteSettingsPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/website-settings");

    return {
      default: module.WebsiteSettingsPage,
    };
  }),
);

const TeamManagementPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/team-management");

    return {
      default: module.TeamManagementPage,
    };
  }),
);

const UsersPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/users");

    return {
      default: module.UsersPage,
    };
  }),
);

const SettingsPage = withRouteSuspense(
  lazy(async () => {
    const module = await import("./routes/settings");

    return {
      default: module.SettingsPage,
    };
  }),
);

const rootRoute = createRootRoute({
  component: () => <Outlet />,
  notFoundComponent: NotFoundPage,
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: () => <Navigate to="/dashboard" />,
});

const loginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/login",
  component: LoginPage,
});

const dashboardLayoutRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: "dashboard-layout",
  component: DashboardLayout,
});

const dashboardRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/dashboard",
  component: DashboardPage,
});

const crmRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/crm",
  component: CrmPage,
});

const clientsRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/clients",
  component: ClientsPage,
});

const quotationsRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/quotations",
  component: QuotationsPage,
});

const projectsRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/projects",
  component: ProjectsPage,
});

const tasksRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/tasks",
  component: TasksPage,
});

const financeRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/finance",
  component: FinancePage,
});

const cmsRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/cms",
  component: CmsPage,
});

const servicesCatalogRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/services-catalog",
  component: ServicesCatalogPage,
});

const packagesCatalogRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/packages-catalog",
  component: PackagesCatalogPage,
});

const mediaLibraryRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/media-library",
  component: MediaLibraryPage,
});

const navigationRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/navigation",
  component: NavigationPage,
});

const publicWebsiteSnapshotsRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/public-website-snapshots",
  component: PublicWebsiteSnapshotsPage,
});

const websiteSettingsRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/website-settings",
  component: WebsiteSettingsPage,
});

const teamManagementRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/team-management",
  component: TeamManagementPage,
});

const usersRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/users",
  component: UsersPage,
});

const settingsRoute = createRoute({
  getParentRoute: () => dashboardLayoutRoute,
  path: "/settings",
  component: SettingsPage,
});

const routeTree = rootRoute.addChildren([
  indexRoute,
  loginRoute,
  dashboardLayoutRoute.addChildren([
    dashboardRoute,
    crmRoute,
    clientsRoute,
    quotationsRoute,
    projectsRoute,
    tasksRoute,
    financeRoute,
    cmsRoute,
    servicesCatalogRoute,
    packagesCatalogRoute,
    mediaLibraryRoute,
    navigationRoute,
    publicWebsiteSnapshotsRoute,
    websiteSettingsRoute,
    teamManagementRoute,
    usersRoute,
    settingsRoute,
  ]),
]);

export const router = createRouter({
  routeTree,
});

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}
