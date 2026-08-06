import {
  useEffect,
  useState,
} from "react";
import {
  useForm,
  useWatch,
} from "react-hook-form";
import {
  Save,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  Input,
} from "../../../components/ui/input";
import {
  formatJson,
  parseJsonObject,
  parseJsonValue,
  settingEnvironmentLabels,
  settingValueTypeLabels,
} from "../formatters";
import {
  useCreateWebsiteSetting,
  useUpdateWebsiteSetting,
} from "../hooks";
import {
  websiteSettingPayloadSchema,
} from "../schemas";
import {
  settingEnvironments,
  settingValueTypes,
  type SettingEnvironment,
  type SettingValueType,
  type WebsiteSetting,
  type WebsiteSettingGroup,
} from "../types";

interface SettingFormValues {
  group_id: string;
  key: string;
  label: string;
  description: string;
  value_type: SettingValueType;
  environment: SettingEnvironment;
  value: string;
  json_value: string;
  media_asset_id: string;
  default_value: string;
  validation_rules: string;
  is_public: boolean;
  is_editable: boolean;
  is_required: boolean;
  is_active: boolean;
  sort_order: number;
}

const defaults: SettingFormValues = {
  group_id: "",
  key: "",
  label: "",
  description: "",
  value_type: "string",
  environment: "global",
  value: "",
  json_value: "{}",
  media_asset_id: "",
  default_value: "",
  validation_rules: "{}",
  is_public: false,
  is_editable: true,
  is_required: false,
  is_active: true,
  sort_order: 0,
};

export function SettingForm({
  setting,
  groups,
  suggestedGroupId,
  open,
  onClose,
}: {
  setting: WebsiteSetting | null;
  groups: WebsiteSettingGroup[];
  suggestedGroupId: string;
  open: boolean;
  onClose: () => void;
}) {
  const [
    formError,
    setFormError,
  ] = useState("");

  const form =
    useForm<SettingFormValues>({
      defaultValues: defaults,
    });

  const createMutation =
    useCreateWebsiteSetting();

  const updateMutation =
    useUpdateWebsiteSetting();

  const selectedValueType =
    useWatch({
      control: form.control,
      name: "value_type",
    });

  const booleanValue =
    useWatch({
      control: form.control,
      name: "value",
    });

  useEffect(() => {
    if (!open) {
      return;
    }

    form.reset(
      setting
        ? {
          group_id:
            setting.group_id,
          key: setting.key,
          label: setting.label,
          description:
            setting.description,
          value_type:
            setting.value_type,
          environment:
            setting.environment,
          value: setting.value,
          json_value: formatJson(
            setting.json_value,
          ),
          media_asset_id:
            setting.media_asset_id
            ?? "",
          default_value:
            setting.default_value,
          validation_rules:
            formatJson(
              setting.validation_rules,
            ),
          is_public:
            setting.is_public,
          is_editable:
            setting.is_editable,
          is_required:
            setting.is_required,
          is_active:
            setting.is_active,
          sort_order:
            setting.sort_order,
        }
        : {
          ...defaults,
          group_id:
            suggestedGroupId
            || groups[0]?.id
            || "",
        },
    );
  }, [
    form,
    groups,
    open,
    setting,
    suggestedGroupId,
  ]);

  if (!open) {
    return null;
  }

  function closeForm() {
    setFormError("");
    onClose();
  }

  async function submit(
    values: SettingFormValues,
  ) {
    setFormError("");

    try {
      const jsonValue =
        values.value_type === "json"
          ? parseJsonValue(
            values.json_value,
            "JSON value",
          )
          : {};

      const payload =
        websiteSettingPayloadSchema
          .parse({
            group_id:
              values.group_id,
            key: values.key,
            label: values.label,
            description:
              values.description,
            value_type:
              values.value_type,
            environment:
              values.environment,
            value: values.value,
            json_value: jsonValue,
            media_asset_id:
              values.media_asset_id
                .trim()
              || null,
            default_value:
              values.default_value,
            validation_rules:
              parseJsonObject(
                values.validation_rules,
                "Validation rules",
              ),
            is_public:
              values.is_public,
            is_editable:
              values.is_editable,
            is_required:
              values.is_required,
            is_active:
              values.is_active,
            sort_order: Number(
              values.sort_order,
            ),
          });

      if (setting) {
        await updateMutation.mutateAsync({
          settingId: setting.id,
          payload,
        });
      } else {
        await createMutation.mutateAsync(
          payload,
        );
      }

      closeForm();
    } catch (error) {
      setFormError(
        error instanceof Error
          ? error.message
          : "The website setting could not be saved.",
      );
    }
  }

  const pending =
    createMutation.isPending
    || updateMutation.isPending;

  return (
    <>
      <button
        type="button"
        onClick={closeForm}
        aria-label="Close setting form"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-2xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <h2 className="font-semibold text-slate-950 dark:text-white">
            {setting
              ? "Edit website setting"
              : "Create website setting"}
          </h2>

          <Button
            variant="ghost"
            size="icon"
            onClick={closeForm}
          >
            <X size={18} />
          </Button>
        </header>

        <form
          onSubmit={form.handleSubmit(
            submit,
          )}
          className="flex flex-1 flex-col overflow-hidden"
        >
          <div className="grid flex-1 gap-5 overflow-y-auto p-5 md:grid-cols-2">
            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Group
              </span>

              <select
                {...form.register(
                  "group_id",
                )}
                className="mt-2 h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              >
                {groups.map((group) => (
                  <option
                    key={group.id}
                    value={group.id}
                  >
                    {group.name}
                  </option>
                ))}
              </select>
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Environment
              </span>

              <select
                {...form.register(
                  "environment",
                )}
                className="mt-2 h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              >
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
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Key
              </span>

              <Input
                {...form.register(
                  "key",
                  {
                    required: true,
                  },
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Label
              </span>

              <Input
                {...form.register(
                  "label",
                  {
                    required: true,
                  },
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block md:col-span-2">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Description
              </span>

              <textarea
                {...form.register(
                  "description",
                )}
                rows={4}
                className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Value type
              </span>

              <select
                {...form.register(
                  "value_type",
                )}
                className="mt-2 h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              >
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
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Sort order
              </span>

              <Input
                type="number"
                {...form.register(
                  "sort_order",
                  {
                    valueAsNumber: true,
                  },
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            {selectedValueType === "json" ? (
              <label className="block md:col-span-2">
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  JSON value
                </span>

                <textarea
                  {...form.register(
                    "json_value",
                  )}
                  rows={8}
                  spellCheck={false}
                  className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 font-mono text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
                />
              </label>
            ) : selectedValueType === "media" ? (
              <label className="block md:col-span-2">
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  Media asset UUID
                </span>

                <Input
                  {...form.register(
                    "media_asset_id",
                  )}
                  className="mt-2 dark:border-slate-700 dark:bg-slate-950"
                />
              </label>
            ) : selectedValueType === "boolean" ? (
              <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 md:col-span-2 dark:border-slate-700">
                <input
                  type="checkbox"
                  checked={
                    booleanValue === "true"
                  }
                  onChange={(event) => {
                    form.setValue(
                      "value",
                      String(
                        event.target.checked,
                      ),
                    );
                  }}
                />

                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  Enabled
                </span>
              </label>
            ) : (
              <label className="block md:col-span-2">
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  Value
                </span>

                {selectedValueType
                  === "text"
                  ? (
                    <textarea
                      {...form.register(
                        "value",
                      )}
                      rows={6}
                      className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
                    />
                  )
                  : (
                    <Input
                      type={
                        selectedValueType
                        === "email"
                          ? "email"
                          : selectedValueType
                            === "url"
                            ? "url"
                            : selectedValueType
                              === "color"
                              ? "color"
                              : selectedValueType
                                === "integer"
                                || selectedValueType
                                  === "decimal"
                                ? "number"
                                : "text"
                      }
                      step={
                        selectedValueType
                        === "decimal"
                          ? "any"
                          : undefined
                      }
                      {...form.register(
                        "value",
                      )}
                      className="mt-2 dark:border-slate-700 dark:bg-slate-950"
                    />
                  )}
              </label>
            )}

            <label className="block md:col-span-2">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Default value
              </span>

              <Input
                {...form.register(
                  "default_value",
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block md:col-span-2">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Validation rules JSON
              </span>

              <textarea
                {...form.register(
                  "validation_rules",
                )}
                rows={6}
                spellCheck={false}
                className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 font-mono text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              />
            </label>

            <div className="grid gap-3 sm:grid-cols-2 md:col-span-2">
              {[
                [
                  "is_public",
                  "Public",
                ],
                [
                  "is_editable",
                  "Editable",
                ],
                [
                  "is_required",
                  "Required",
                ],
                [
                  "is_active",
                  "Active",
                ],
              ].map(([field, label]) => (
                <label
                  key={field}
                  className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700"
                >
                  <input
                    type="checkbox"
                    {...form.register(
                      field as
                        | "is_public"
                        | "is_editable"
                        | "is_required"
                        | "is_active",
                    )}
                  />

                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                    {label}
                  </span>
                </label>
              ))}
            </div>

            {formError && (
              <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800 md:col-span-2 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
                {formError}
              </p>
            )}
          </div>

          <footer className="flex justify-end gap-3 border-t border-slate-200 p-4 dark:border-slate-800">
            <Button
              type="button"
              variant="outline"
              onClick={closeForm}
            >
              Cancel
            </Button>

            <Button
              type="submit"
              disabled={pending}
            >
              <Save size={16} />
              {pending
                ? "Saving..."
                : "Save setting"}
            </Button>
          </footer>
        </form>
      </aside>
    </>
  );
}
