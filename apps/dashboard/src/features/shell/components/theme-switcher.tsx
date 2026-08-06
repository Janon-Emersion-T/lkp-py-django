import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import {
  Check,
  Laptop,
  Moon,
  Sun,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  useTheme,
} from "../hooks/use-theme";
import type {
  ThemePreference,
} from "../theme-context";

const themeOptions: readonly {
  value: ThemePreference;
  label: string;
  icon: typeof Sun;
}[] = [
  {
    value: "light",
    label: "Light",
    icon: Sun,
  },
  {
    value: "dark",
    label: "Dark",
    icon: Moon,
  },
  {
    value: "system",
    label: "System",
    icon: Laptop,
  },
];

export function ThemeSwitcher() {
  const {
    preference,
    resolvedTheme,
    setPreference,
  } = useTheme();

  const TriggerIcon =
    resolvedTheme === "dark"
      ? Moon
      : Sun;

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <Button
          variant="ghost"
          size="icon"
          aria-label="Change appearance"
          title="Change appearance"
          className="text-slate-600 dark:text-slate-300"
        >
          <TriggerIcon size={18} />
        </Button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          align="end"
          sideOffset={8}
          className="z-50 min-w-44 rounded-lg border border-slate-200 bg-white p-1.5 shadow-xl dark:border-slate-700 dark:bg-slate-900"
        >
          <DropdownMenu.Label className="px-3 py-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
            Appearance
          </DropdownMenu.Label>

          {themeOptions.map((option) => {
            const Icon = option.icon;
            const isActive = preference === option.value;

            return (
              <DropdownMenu.Item
                key={option.value}
                onSelect={() => setPreference(option.value)}
                className="flex cursor-pointer items-center gap-3 rounded-md px-3 py-2 text-sm text-slate-700 outline-none transition-colors focus:bg-slate-100 dark:text-slate-200 dark:focus:bg-slate-800"
              >
                <Icon size={16} />
                <span>{option.label}</span>

                {isActive && (
                  <Check
                    size={15}
                    className="ml-auto text-blue-700 dark:text-blue-400"
                  />
                )}
              </DropdownMenu.Item>
            );
          })}
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
