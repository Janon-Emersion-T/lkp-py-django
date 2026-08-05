import { useCallback, useState } from "react";

const STORAGE_KEY = "lkp-dashboard-sidebar-collapsed";

function getInitialCollapsedState() {
  return window.localStorage.getItem(STORAGE_KEY) === "true";
}

export function useSidebarState() {
  const [isCollapsed, setIsCollapsed] = useState(
    getInitialCollapsedState,
  );

  const toggleSidebar = useCallback(() => {
    setIsCollapsed((currentState) => {
      const nextState = !currentState;

      window.localStorage.setItem(
        STORAGE_KEY,
        String(nextState),
      );

      return nextState;
    });
  }, []);

  return {
    isCollapsed,
    toggleSidebar,
  };
}
