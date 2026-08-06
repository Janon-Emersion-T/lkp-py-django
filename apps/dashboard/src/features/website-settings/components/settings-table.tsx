import {
  ChevronRight,
  Eye,
  EyeOff,
  Lock,
  Pencil,
  Unlock,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  getSettingDisplayValue,
  settingEnvironmentLabels,
  settingValueTypeLabels,
} from "../formatters";
import type {
  WebsiteSetting,
} from "../types";

export function SettingsTable({
  settings,
  onEdit,
}: {
  settings: WebsiteSetting[];
  onEdit: (
    setting: WebsiteSetting,
  ) => void;
}) {
  if (settings.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-white p-12 text-center dark:border-slate-700 dark:bg-slate-900">
        <p className="font-medium text-slate-700 dark:text-slate-300">
          No settings matched the filters.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <table className="w-full min-w-[1100px]">
        <thead className="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500 dark:bg-slate-800/70">
          <tr>
            <th className="px-5 py-3">
              Setting
            </th>
            <th className="px-5 py-3">
              Group
            </th>
            <th className="px-5 py-3">
              Type
            </th>
            <th className="px-5 py-3">
              Environment
            </th>
            <th className="px-5 py-3">
              Value
            </th>
            <th className="px-5 py-3">
              Controls
            </th>
            <th className="w-12 px-3 py-3" />
          </tr>
        </thead>

        <tbody>
          {settings.map((setting) => (
            <tr
              key={setting.id}
              className="border-t border-slate-200 dark:border-slate-800"
            >
              <td className="max-w-sm px-5 py-4">
                <button
                  type="button"
                  onClick={() => {
                    onEdit(setting);
                  }}
                  className="text-left"
                >
                  <p className="font-semibold text-slate-950 hover:text-blue-700 dark:text-white">
                    {setting.label}
                  </p>

                  <p className="mt-1 font-mono text-xs text-slate-500">
                    {setting.key}
                  </p>

                  {setting.description && (
                    <p className="mt-2 line-clamp-2 text-sm text-slate-600 dark:text-slate-300">
                      {
                        setting.description
                      }
                    </p>
                  )}
                </button>
              </td>

              <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                {setting.group_name}
              </td>

              <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                {
                  settingValueTypeLabels[
                    setting.value_type
                  ]
                }
              </td>

              <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                {
                  settingEnvironmentLabels[
                    setting.environment
                  ]
                }
              </td>

              <td className="max-w-sm px-5 py-4">
                <pre className="max-h-24 overflow-hidden whitespace-pre-wrap break-all font-mono text-xs text-slate-700 dark:text-slate-300">
                  {getSettingDisplayValue(
                    setting,
                  )}
                </pre>
              </td>

              <td className="px-5 py-4">
                <div className="flex flex-wrap gap-3 text-xs">
                  <span
                    className={
                      setting.is_public
                        ? "inline-flex items-center gap-1 text-blue-700 dark:text-blue-400"
                        : "inline-flex items-center gap-1 text-slate-500"
                    }
                  >
                    {setting.is_public
                      ? <Eye size={13} />
                      : <EyeOff size={13} />}
                    {setting.is_public
                      ? "Public"
                      : "Private"}
                  </span>

                  <span
                    className={
                      setting.is_editable
                        ? "inline-flex items-center gap-1 text-emerald-700 dark:text-emerald-400"
                        : "inline-flex items-center gap-1 text-amber-700 dark:text-amber-400"
                    }
                  >
                    {setting.is_editable
                      ? <Unlock size={13} />
                      : <Lock size={13} />}
                    {setting.is_editable
                      ? "Editable"
                      : "Locked"}
                  </span>
                </div>
              </td>

              <td className="px-3 py-4">
                <Button
                  variant="ghost"
                  size="icon"
                  disabled={
                    !setting.is_editable
                  }
                  onClick={() => {
                    onEdit(setting);
                  }}
                  aria-label="Edit setting"
                >
                  {setting.is_editable
                    ? <Pencil size={15} />
                    : <ChevronRight
                      size={15}
                    />}
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
