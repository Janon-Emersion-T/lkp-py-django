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
  navigationLocationLabels,
  parseJsonObject,
  formatJson,
} from "../formatters";
import {
  useCreateNavigationMenu,
  useUpdateNavigationMenu,
} from "../hooks";
import {
  navigationMenuPayloadSchema,
} from "../schemas";
import {
  navigationLocations,
  type NavigationMenu,
  type NavigationMenuPayload,
} from "../types";

interface MenuFormValues {
  name: string;
  slug: string;
  location:
    NavigationMenuPayload["location"];
  description: string;
  sort_order: number;
  is_active: boolean;
  is_public: boolean;
  metadata: string;
}

const defaultValues: MenuFormValues = {
  name: "",
  slug: "",
  location: "custom",
  description: "",
  sort_order: 0,
  is_active: true,
  is_public: true,
  metadata: "{}",
};

export function NavigationMenuForm({
  menu,
  open,
  onClose,
  onSaved,
}: {
  menu: NavigationMenu | null;
  open: boolean;
  onClose: () => void;
  onSaved: (
    menu: NavigationMenu,
  ) => void;
}) {
  const [
    formError,
    setFormError,
  ] = useState("");

  const createMutation =
    useCreateNavigationMenu();

  const updateMutation =
    useUpdateNavigationMenu();

  const form = useForm<MenuFormValues>({
    defaultValues,
  });

  useEffect(() => {
    if (!open) {
      return;
    }

    form.reset(
      menu
        ? {
          name: menu.name,
          slug: menu.slug,
          location: menu.location,
          description:
            menu.description,
          sort_order:
            menu.sort_order,
          is_active: menu.is_active,
          is_public: menu.is_public,
          metadata: formatJson(
            menu.metadata,
          ),
        }
        : defaultValues,
    );
  }, [form, menu, open]);

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
    values: MenuFormValues,
  ) {
    setFormError("");

    try {
      const payload =
        navigationMenuPayloadSchema.parse({
          name: values.name,
          slug: values.slug,
          location: values.location,
          description:
            values.description,
          sort_order: Number(
            values.sort_order,
          ),
          is_active:
            values.is_active,
          is_public:
            values.is_public,
          metadata: parseJsonObject(
            values.metadata,
            "Metadata",
          ),
        });

      const saved = menu
        ? await updateMutation.mutateAsync({
          menuId: menu.id,
          payload,
        })
        : await createMutation.mutateAsync(
          payload,
        );

      onSaved(saved);
      closeForm();
    } catch (error) {
      setFormError(
        error instanceof Error
          ? error.message
          : "The menu could not be saved.",
      );
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={closeForm}
        aria-label="Close menu form"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Navigation menu
            </p>

            <h2 className="font-semibold text-slate-950 dark:text-white">
              {menu
                ? "Edit menu"
                : "Create menu"}
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
          <div className="flex-1 space-y-5 overflow-y-auto p-5">
            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Name
              </span>

              <Input
                {...form.register(
                  "name",
                  {
                    required: true,
                  },
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Slug
              </span>

              <Input
                {...form.register(
                  "slug",
                  {
                    required: true,
                  },
                )}
                className="mt-2 dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Location
              </span>

              <select
                {...form.register(
                  "location",
                )}
                className="mt-2 h-10 w-full rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              >
                {navigationLocations.map(
                  (location) => (
                    <option
                      key={location}
                      value={location}
                    >
                      {
                        navigationLocationLabels[
                          location
                        ]
                      }
                    </option>
                  ),
                )}
              </select>
            </label>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Description
              </span>

              <textarea
                {...form.register(
                  "description",
                )}
                rows={4}
                className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm outline-none focus:border-blue-500 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
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

            <div className="grid gap-3 sm:grid-cols-2">
              <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                <input
                  type="checkbox"
                  {...form.register(
                    "is_active",
                  )}
                />

                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  Active
                </span>
              </label>

              <label className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                <input
                  type="checkbox"
                  {...form.register(
                    "is_public",
                  )}
                />

                <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                  Public
                </span>
              </label>
            </div>

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Metadata JSON
              </span>

              <textarea
                {...form.register(
                  "metadata",
                )}
                rows={7}
                spellCheck={false}
                className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 font-mono text-xs outline-none focus:border-blue-500 dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
              />
            </label>

            {formError && (
              <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
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
                : "Save menu"}
            </Button>
          </footer>
        </form>
      </aside>
    </>
  );
}
