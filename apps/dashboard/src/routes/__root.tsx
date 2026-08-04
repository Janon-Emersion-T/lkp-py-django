import { Outlet, createRootRoute } from "@tanstack/react-router";

export const Route = createRootRoute({
  component: () => (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(214,163,95,0.18),transparent_30%),linear-gradient(180deg,#f8fafc_0%,#eef2ff_100%)]">
      <Outlet />
    </div>
  ),
});
