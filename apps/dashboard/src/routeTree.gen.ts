import { Route as rootRoute } from "./routes/__root";
import { Route as indexRoute } from "./routes/index";

const index = indexRoute.update({
  getParentRoute: () => rootRoute,
  path: "/"
});

export const routeTree = rootRoute.addChildren([index]);

