import { createRoute } from "@tanstack/react-router";
import { Route as rootRoute } from "./__root";
import { LoginForm } from "@/features/auth/login-form";

export const Route = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: () => (
    <main className="flex min-h-screen items-center justify-center px-6 py-12">
      <LoginForm />
    </main>
  ),
});
