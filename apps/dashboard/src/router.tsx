import {
  createRootRoute,
  createRoute,
  createRouter,
  Navigate,
  Outlet,
} from "@tanstack/react-router";

import { DashboardLayout } from "./layouts/dashboard-layout";
import { LoginPage } from "./routes/auth/login";
import { DashboardPage } from "./routes/dashboard";
import { CrmPage } from "./routes/crm";
import { ClientsPage } from "./routes/clients";
import { QuotationsPage } from "./routes/quotations";
import { ProjectsPage } from "./routes/projects";
import { TasksPage } from "./routes/tasks";
import { NotFoundPage } from "./routes/errors/not-found";
import { SettingsPage } from "./routes/settings";
import { UsersPage } from "./routes/users";

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
