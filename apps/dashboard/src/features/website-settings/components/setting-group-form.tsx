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
  useCreateSettingGroup,
  useUpdateSettingGroup,
} from "../hooks";
import {
  websiteSettingGroupPayloadSchema,
} from "../schemas";
import type {
  WebsiteSettingGroup,
  WebsiteSettingGroupPayload,
} from "../types";

const defaults:
WebsiteSettingGroupPayload = {
  name: "",
  slug: "",
  description: "",
  icon: "",
  is_active: true,
  sort_order: 0,
};

export function SettingGroupForm({
  group,
  open,
  onClose,
}: {
  group: WebsiteSettingGroup | null;
  open: boolean;
  onClose: () => void;
}) {
  const [
    formError,
    setFormError,
  ] = useState("");

  const form =
    useForm<WebsiteSettingGroupPayload>({
      defaultValues: defaults,
    });

  const createMutation =
    useCreateSettingGroup();

  const updateMutation =
    useUpdateSettingGroup();

  useEffect(() => {
    if (!open) {
      return;
    }

    form.reset(
      group
        ? {
          name: group.name,
          slug: group.slug,
          description:
            group.description,
          icon: group.icon,
          is_active:
            group.is_active,
          sort_order:
            group.sort_order,
        }
        : defaults,
    );
  }, [form, group, open]);

  if (!open) {
    return null;
  }

  function closeForm() {
    setFormError("");
    onClose();
  }

  async function submit(
    values:
      WebsiteSettingGroupPayload,
  ) {
    setFormError("");

    try {
      const payload =
        websiteSettingGroupPayloadSchema
          .parse({
            ...values,
            sort_order: Number(
              values.sort_order,
            ),
          });

      if (group) {
        await updateMutation.mutateAsync({
          groupId: group.id,
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
          : "The setting group could not be saved.",
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
        aria-label="Close group form"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <h2 className="font-semibold text-slate-950 dark:text-white">
            {group
              ? "Edit setting group"
              : "Create setting group"}
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
          <div className="flex-1 space-y-5 overflow-y-auto p-5">
            {[
              [
                "name",
                "Name",
              ],
              [
                "slug",
                "Slug",
              ],
              [
                "icon",
                "Icon",
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
                      | "name"
                      | "slug"
                      | "icon",
                    {
                      required:
                        field !== "icon",
                    },
                  )}
                  className="mt-2 dark:border-slate-700 dark:bg-slate-950"
                />
              </label>
            ))}

            <label className="block">
              <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                Description
              </span>

              <textarea
                {...form.register(
                  "description",
                )}
                rows={5}
                className="mt-2 w-full rounded-md border border-slate-200 bg-white px-3 py-2 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
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
                : "Save group"}
            </Button>
          </footer>
        </form>
      </aside>
    </>
  );
}
