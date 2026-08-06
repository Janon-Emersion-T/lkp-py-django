import {
  RotateCcw,
  Search,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  Input,
} from "../../../components/ui/input";
import {
  settingEnvironmentLabels,
  settingValueTypeLabels,
} from "../formatters";
import {
  settingEnvironments,
  settingOrderingValues,
  settingValueTypes,
  type SettingEnvironment,
  type SettingOrdering,
  type SettingValueType,
  type WebsiteSettingFilters,
  type WebsiteSettingGroup,
} from "../types";

function booleanFilterValue(
  value: boolean | null,
): string {
  if (value === null) {
    return "";
  }

  return value ? "true" : "false";
}

function parseBooleanFilter(
  value: string,
): boolean | null {
  if (value === "") {
    return null;
  }

  return value === "true";
}

function parseValueType(
  value: string,
): SettingValueType | "" {
  if (value === "") {
    return "";
  }

  if (
    settingValueTypes.includes(
      value as SettingValueType,
    )
  ) {
    return value as SettingValueType;
  }

  return "";
}

function parseEnvironment(
  value: string,
): SettingEnvironment | "" {
  if (value === "") {
    return "";
  }

  if (
    settingEnvironments.includes(
      value as SettingEnvironment,
    )
  ) {
    return value as SettingEnvironment;
  }

  return "";
}

function parseOrdering(
  value: string,
): SettingOrdering {
  if (
    settingOrderingValues.includes(
      value as SettingOrdering,
    )
  ) {
    return value as SettingOrdering;
  }

  return "sort_order";
}

export function SettingsFilters({
  filters,
  groups,
  onChange,
}: {
  filters: WebsiteSettingFilters;
  groups: WebsiteSettingGroup[];
  onChange: (
    filters: WebsiteSettingFilters,
  ) => void;
}) {
  function update(
    changes: Partial<WebsiteSettingFilters>,
  ) {
    onChange({
      ...filters,
      ...changes,
    });
  }

  function reset() {
    onChange({
      search: "",
      groupId: "",
      valueType: "",
      environment: "",
      isPublic: null,
      isEditable: null,
      isActive: null,
      ordering: "sort_order",
    });
  }

  return (
    <section className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 md:grid-cols-2 xl:grid-cols-4 dark:border-slate-800 dark:bg-slate-900">
      <label className="relative">
        <Search
          size={16}
          className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
        />

        <Input
          value={filters.search}
          onChange={(event) => {
            update({
              search: event.target.value,
            });
          }}
          placeholder="Search settings"
          className="pl-9 dark:border-slate-700 dark:bg-slate-950"
        />
      </label>

      <select
        value={filters.groupId}
        onChange={(event) => {
          update({
            groupId: event.target.value,
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All groups
        </option>

        {groups.map((group) => (
          <option
            key={group.id}
            value={group.id}
          >
            {group.name}
          </option>
        ))}
      </select>

      <select
        value={filters.valueType}
        onChange={(event) => {
          update({
            valueType: parseValueType(
              event.target.value,
            ),
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All value types
        </option>

        {settingValueTypes.map(
          (valueType) => (
            <option
              key={valueType}
              value={valueType}
            >
              {
                settingValueTypeLabels[
                  valueType
                ]
              }
            </option>
          ),
        )}
      </select>

      <select
        value={filters.environment}
        onChange={(event) => {
          update({
            environment: parseEnvironment(
              event.target.value,
            ),
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All environments
        </option>

        {settingEnvironments.map(
          (environment) => (
            <option
              key={environment}
              value={environment}
            >
              {
                settingEnvironmentLabels[
                  environment
                ]
              }
            </option>
          ),
        )}
      </select>

      <select
        value={booleanFilterValue(
          filters.isPublic,
        )}
        onChange={(event) => {
          update({
            isPublic: parseBooleanFilter(
              event.target.value,
            ),
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All public states
        </option>
        <option value="true">
          Public
        </option>
        <option value="false">
          Private
        </option>
      </select>

      <select
        value={booleanFilterValue(
          filters.isEditable,
        )}
        onChange={(event) => {
          update({
            isEditable:
              parseBooleanFilter(
                event.target.value,
              ),
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All editable states
        </option>
        <option value="true">
          Editable
        </option>
        <option value="false">
          Locked
        </option>
      </select>

      <select
        value={booleanFilterValue(
          filters.isActive,
        )}
        onChange={(event) => {
          update({
            isActive: parseBooleanFilter(
              event.target.value,
            ),
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="">
          All active states
        </option>
        <option value="true">
          Active
        </option>
        <option value="false">
          Inactive
        </option>
      </select>

      <select
        value={filters.ordering}
        onChange={(event) => {
          update({
            ordering: parseOrdering(
              event.target.value,
            ),
          });
        }}
        className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
      >
        <option value="sort_order">
          Sort order
        </option>
        <option value="-sort_order">
          Reverse sort order
        </option>
        <option value="key">
          Key A–Z
        </option>
        <option value="-key">
          Key Z–A
        </option>
        <option value="label">
          Label A–Z
        </option>
        <option value="-label">
          Label Z–A
        </option>
        <option value="value_type">
          Value type
        </option>
        <option value="environment">
          Environment
        </option>
        <option value="-updated_at">
          Recently updated
        </option>
        <option value="-created_at">
          Recently created
        </option>
      </select>

      <Button
        variant="outline"
        onClick={reset}
        className="dark:border-slate-700"
      >
        <RotateCcw size={16} />
        Reset filters
      </Button>
    </section>
  );
}
