import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import {
  ChevronDown,
  LogOut,
  Settings,
  UserRound,
} from "lucide-react";

import type { CurrentUser } from "../../lib/api";
import { Button } from "../ui/button";

interface UserMenuProps {
  user: CurrentUser;
  onLogout: () => Promise<void>;
}

function getDisplayName(user: CurrentUser) {
  return (
    [user.first_name, user.last_name]
      .filter(Boolean)
      .join(" ") || user.email
  );
}

function getInitials(user: CurrentUser) {
  const initials = [user.first_name, user.last_name]
    .filter(Boolean)
    .map((name) => name?.charAt(0).toUpperCase())
    .join("");

  return initials || user.email.charAt(0).toUpperCase();
}

export function UserMenu({
  user,
  onLogout,
}: UserMenuProps) {
  const displayName = getDisplayName(user);
  const initials = getInitials(user);

  return (
    <DropdownMenu.Root>
      <DropdownMenu.Trigger asChild>
        <Button
          variant="ghost"
          className="h-auto max-w-64 gap-3 px-2 py-1.5"
          aria-label="Open user menu"
        >
          <span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-blue-700 text-sm font-semibold text-white">
            {initials}
          </span>

          <span className="hidden min-w-0 text-left sm:block">
            <span className="block truncate text-sm font-medium text-slate-950">
              {displayName}
            </span>

            <span className="block truncate text-xs text-slate-500">
              {user.is_staff ? "Administrator" : user.email}
            </span>
          </span>

          <ChevronDown
            size={16}
            className="hidden shrink-0 text-slate-500 sm:block"
          />
        </Button>
      </DropdownMenu.Trigger>

      <DropdownMenu.Portal>
        <DropdownMenu.Content
          align="end"
          sideOffset={8}
          className="z-50 min-w-64 rounded-lg border border-slate-200 bg-white p-1.5 shadow-lg"
        >
          <div className="px-3 py-2">
            <p className="truncate text-sm font-medium text-slate-950">
              {displayName}
            </p>

            <p className="truncate text-xs text-slate-500">
              {user.email}
            </p>
          </div>

          <DropdownMenu.Separator className="my-1 h-px bg-slate-200" />

          <DropdownMenu.Item
            disabled
            className="flex cursor-not-allowed items-center gap-3 rounded-md px-3 py-2 text-sm text-slate-400 outline-none"
          >
            <UserRound size={16} />
            Profile
            <span className="ml-auto text-xs">Soon</span>
          </DropdownMenu.Item>

          <DropdownMenu.Item
            disabled
            className="flex cursor-not-allowed items-center gap-3 rounded-md px-3 py-2 text-sm text-slate-400 outline-none"
          >
            <Settings size={16} />
            Account settings
            <span className="ml-auto text-xs">Soon</span>
          </DropdownMenu.Item>

          <DropdownMenu.Separator className="my-1 h-px bg-slate-200" />

          <DropdownMenu.Item
            onSelect={() => {
              void onLogout();
            }}
            className="flex cursor-pointer items-center gap-3 rounded-md px-3 py-2 text-sm text-red-700 outline-none transition-colors focus:bg-red-50"
          >
            <LogOut size={16} />
            Sign out
          </DropdownMenu.Item>
        </DropdownMenu.Content>
      </DropdownMenu.Portal>
    </DropdownMenu.Root>
  );
}
