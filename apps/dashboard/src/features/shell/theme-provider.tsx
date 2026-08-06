import {
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import {
  ThemeContext,
  type ResolvedTheme,
  type ThemePreference,
} from "./theme-context";

const THEME_STORAGE_KEY = "lkp_dashboard_theme";

interface ThemeProviderProps {
  children: ReactNode;
}

function getStoredPreference(): ThemePreference {
  const storedPreference = localStorage.getItem(THEME_STORAGE_KEY);

  if (
    storedPreference === "light" ||
    storedPreference === "dark" ||
    storedPreference === "system"
  ) {
    return storedPreference;
  }

  return "system";
}

function getSystemTheme(): ResolvedTheme {
  return window.matchMedia("(prefers-color-scheme: dark)").matches
    ? "dark"
    : "light";
}

function resolveTheme(
  preference: ThemePreference,
): ResolvedTheme {
  return preference === "system"
    ? getSystemTheme()
    : preference;
}

function applyTheme(theme: ResolvedTheme) {
  const root = document.documentElement;

  root.classList.toggle("dark", theme === "dark");
  root.style.colorScheme = theme;
}

export function ThemeProvider({
  children,
}: ThemeProviderProps) {
  const [preference, setPreferenceState] =
    useState<ThemePreference>(getStoredPreference);

  const [resolvedTheme, setResolvedTheme] =
    useState<ResolvedTheme>(() => resolveTheme(preference));

  useEffect(() => {
    const mediaQuery = window.matchMedia(
      "(prefers-color-scheme: dark)",
    );

    function synchronizeTheme() {
      const nextTheme = resolveTheme(preference);

      setResolvedTheme(nextTheme);
      applyTheme(nextTheme);
    }

    synchronizeTheme();

    if (preference === "system") {
      mediaQuery.addEventListener("change", synchronizeTheme);
    }

    return () => {
      mediaQuery.removeEventListener("change", synchronizeTheme);
    };
  }, [preference]);

  function setPreference(
    nextPreference: ThemePreference,
  ) {
    localStorage.setItem(
      THEME_STORAGE_KEY,
      nextPreference,
    );

    setPreferenceState(nextPreference);
  }

  const value = useMemo(
    () => ({
      preference,
      resolvedTheme,
      setPreference,
    }),
    [preference, resolvedTheme],
  );

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}
