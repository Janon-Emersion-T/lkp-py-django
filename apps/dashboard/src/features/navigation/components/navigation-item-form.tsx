import {
  useEffect,
  useState,
} from "react";
import {
  useForm,
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
  flattenNavigationItems,
  formatJson,
  navigationLinkTypeLabels,
  navigationVisibilityLabels,
  parseJsonObject,
} from "../formatters";
import {
  useCreateNavigationItem,
  useUpdateNavigationItem,
} from "../hooks";
import {
  navigationItemPayloadSchema,
} from "../schemas";
import {
  navigationLinkTypes,
  navigationVisibilityValues,
  type NavigationMenu,
  type NavigationMenuItem,
  type NavigationMenuItemPayload,
} from "../types";

interface ItemFormValues {
  parent_id: string;
  label: string;
  link_type:
    NavigationMenuItemPayload["link_type"];
  url: string;
  route_name: string;
  route_parameters: string;
  cms_page_id: string;
  service_id: string;
  package_id: string;
  industry_id: string;
  insight_id: string;
  case_study_id: string;
  visibility:
    NavigationMenuItemPayload["visibility"];
  icon: string;
  css_class: string;
  target_blank: boolean;
  rel_attribute: string;
  is_active: boolean;
  is_featured: boolean;
  sort_order: number;
  metadata: string;
}

const defaults: ItemFormValues = {
  parent_id: "",
  label: "",
  link_type: "internal",
  url: "",
  route_name: "",
  route_parameters: "{}",
  cms_page_id: "",
  service_id: "",
  package_id: "",
  industry_id: "",
  insight_id: "",
  case_study_id: "",
  visibility: "everyone",
  icon: "",
  css_class: "",
  target_blank: false,
  rel_attribute: "",
  is_active: true,
  is_featured: false,
  sort_order: 0,
  metadata: "{}",
};

function nullableId(
  value: string,
): string | null {
  const normalized = value.trim();

  return normalized || null;
}

export function NavigationItemForm({
  menu,
  item,
  suggestedParentId,
  open,
  onClose,
}: {
  menu: NavigationMenu;
  item: NavigationMenuItem | null;
  suggestedParentId: string | null;
  open: boolean;
  onClose: () => void;
}) {
  const [
    formError,
    setFormError,
  ] = useState("");

  const createMutation =
    useCreateNavigationItem();

  const updateMutation =
    useUpdateNavigationItem(
      menu.id,
    );

  const form = useForm<ItemFormValues>({
    defaultValues: defaults,
  });

  const flattened =
    flattenNavigationItems(
      menu.items,
    );

  useEffect(() => {
    if (!open) {
      return;
    }

    form.reset(
      item
        ? {
          parent_id:
            item.parent_id ?? "",
          label: item.label,
          link_type:
            item.link_type,
          url: item.url,
          route_name:
            item.route_name,
          route_parameters:
            formatJson(
              item.route_parameters,
            ),
          cms_page_id:
            item.cms_page_id ?? "",
          service_id:
            item.service_id ?? "",
          package_id:
            item.package_id ?? "",
          industry_id:
            item.industry_id ?? "",
          insight_id:
            item.insight_id ?? "",
          case_study_id:
            item.case_study_id ?? "",
          visibility:
            item.visibility,
          icon: item.icon,
          css_class:
            item.css_class,
          target_blank:
            item.target_blank,
          rel_attribute:
            item.rel_attribute,
          is_active:
            item.is_active,
          is_featured:
            item.is_featured,
          sort_order:
            item.sort_order,
          metadata: formatJson(
            item.metadata,
          ),
        }
        : {
          ...defaults,
          parent_id:
            suggestedParentId ?? "",
        },
    );
  }, [
    form,
    item,
    open,
    suggestedParentId,
  ]);

  if (!open) {
    return null;
  }

  const pending =
    createMutation.isPending
    || updateMutation.isPending;

  function closeForm() {
    setFormError("");
    onClose();
  }

  async function submit(
    values: ItemFormValues,
  ) {
    setFormError("");

    try {
      const parentId =
        nullableId(values.parent_id);

      if (
        item
        && parentId === item.id
      ) {
        throw new Error(
          "A navigation item cannot be its own parent.",
        );
      }

      const payload =
        navigationItemPayloadSchema.parse({
          parent_id: parentId,
          label: values.label,
          link_type:
            values.link_type,
          url: values.url,
          route_name:
            values.route_name,
          route_parameters:
            parseJsonObject(
              values.route_parameters,
              "Route parameters",
            ),
          cms_page_id:
            nullableId(
              values.cms_page_id,
            ),
          service_id:
            nullableId(
              values.service_id,
            ),
          package_id:
            nullableId(
              values.package_id,
            ),
          industry_id:
            nullableId(
              values.industry_id,
            ),
          insight_id:
            nullableId(
              values.insight_id,
            ),
          case_study_id:
            nullableId(
              values.case_study_id,
            ),
          visibility:
            values.visibility,
          icon: values.icon,
          css_class:
            values.css_class,
          target_blank:
            values.target_blank,
          rel_attribute:
            values.rel_attribute,
          is_active:
            values.is_active,
          is_featured:
            values.is_featured,
          sort_order: Number(
            values.sort_order,
          ),
          metadata: parseJsonObject(
            values.metadata,
            "Metadata",
          ),
        });

      if (item) {
        await updateMutation.mutateAsync({
          itemId: item.id,
          payload,
        });
      } else {
        await createMutation.mutateAsync({
          menuId: menu.id,
          payload,
        });
      }

      closeForm();
    } catch (error) {
      setFormError(
        error instanceof Error
          ? error.message
          : "The navigation item could not be saved.",
      );
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={closeForm}
        aria-label="Close item form"
        className="fixed inset-0 z-[60] bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-[70] flex w-full max-w-2xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Navigation item
            </p>

            <h2 className="font-semibold text-slate-950 dark:text-white">
              {item
                ? "Edit item"
                : "Create item"}
            </h2>
          </div>

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
            <label className="block md:col-span-2">
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

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Parent item
              </span>

              <select
                {...form.register(
                  "parent_id",
                )}
                className="mt-2 h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              >
                <option value="">
                  Root level
                </option>

                {flattened
                  .filter(
                    (candidate) =>
                      candidate.id
                      !== item?.id,
                  )
                  .map((candidate) => (
                    <option
                      key={candidate.id}
                      value={candidate.id}
                    >
                      {"— ".repeat(
                        candidate.depth,
                      )}
                      {candidate.label}
                    </option>
                  ))}
              </select>
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Link type
              </span>

              <select
                {...form.register(
                  "link_type",
                )}
                className="mt-2 h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              >
                {navigationLinkTypes.map(
                  (linkType) => (
                    <option
                      key={linkType}
                      value={linkType}
                    >
                      {
                        navigationLinkTypeLabels[
                          linkType
                        ]
                      }
                    </option>
                  ),
                )}
              </select>
            </label>

            <label className="block md:col-span-2">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                URL
              </span>

              <Input
                {...form.register("url")}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Route name
              </span>

              <Input
                {...form.register(
                  "route_name",
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Visibility
              </span>

              <select
                {...form.register(
                  "visibility",
                )}
                className="mt-2 h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              >
                {navigationVisibilityValues.map(
                  (visibility) => (
                    <option
                      key={visibility}
                      value={visibility}
                    >
                      {
                        navigationVisibilityLabels[
                          visibility
                        ]
                      }
                    </option>
                  ),
                )}
              </select>
            </label>

            <label className="block md:col-span-2">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Route parameters JSON
              </span>

              <textarea
                {...form.register(
                  "route_parameters",
                )}
                rows={4}
                spellCheck={false}
                className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 font-mono text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              />
            </label>

            {[
              [
                "cms_page_id",
                "CMS Page UUID",
              ],
              [
                "service_id",
                "Service UUID",
              ],
              [
                "package_id",
                "Package UUID",
              ],
              [
                "industry_id",
                "Industry UUID",
              ],
              [
                "insight_id",
                "Insight UUID",
              ],
              [
                "case_study_id",
                "Case Study UUID",
              ],
            ].map(([field, label]) => (
              <label
                key={field}
                className="block"
              >
                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  {label}
                </span>

                <Input
                  {...form.register(
                    field as
                      | "cms_page_id"
                      | "service_id"
                      | "package_id"
                      | "industry_id"
                      | "insight_id"
                      | "case_study_id",
                  )}
                  className="mt-2 dark:border-slate-700 dark:bg-slate-950"
                />
              </label>
            ))}

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Icon
              </span>

              <Input
                {...form.register("icon")}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                CSS class
              </span>

              <Input
                {...form.register(
                  "css_class",
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Rel attribute
              </span>

              <Input
                {...form.register(
                  "rel_attribute",
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
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

            <div className="grid gap-3 sm:grid-cols-2 md:col-span-2">
              {[
                [
                  "is_active",
                  "Active",
                ],
                [
                  "is_featured",
                  "Featured",
                ],
                [
                  "target_blank",
                  "Open in new tab",
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
                        | "is_active"
                        | "is_featured"
                        | "target_blank",
                    )}
                  />

                  <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                    {label}
                  </span>
                </label>
              ))}
            </div>

            <label className="block md:col-span-2">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Metadata JSON
              </span>

              <textarea
                {...form.register(
                  "metadata",
                )}
                rows={6}
                spellCheck={false}
                className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 font-mono text-xs dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              />
            </label>

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
                : "Save item"}
            </Button>
          </footer>
        </form>
      </aside>
    </>
  );
}
