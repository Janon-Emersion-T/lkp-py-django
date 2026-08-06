import {
  CalendarClock,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Eye,
  FilterX,
  Globe2,
  LoaderCircle,
  Pencil,
  Plus,
  Rocket,
  Search,
  Star,
  Trash2,
  X,
} from "lucide-react";
import {
  useMemo,
  useState,
} from "react";

import {
  formatDateTime,
  serviceStatusLabels,
  statusClasses,
} from "../formatters";
import {
  useCatalogService,
  useDeleteService,
  usePublishService,
  useScheduleService,
  useServicesCatalog,
} from "../hooks";
import {
  serviceStatuses,
  type CatalogService,
  type ServiceFilters,
  type ServiceStatus,
} from "../types";

const defaultFilters:
ServiceFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  featuredState: "all",
  activeState: "all",
  ordering: "sort_order",
};

type Dialog =
  | "schedule"
  | "delete"
  | null;

export function ServicesCatalogPage() {
  const [
    filters,
    setFilters,
  ] = useState(defaultFilters);

  const [
    selectedId,
    setSelectedId,
  ] = useState("");

  const [
    dialog,
    setDialog,
  ] = useState<Dialog>(null);

  const [
    notice,
    setNotice,
  ] = useState("");

  const servicesQuery =
    useServicesCatalog(filters);

  const detailQuery =
    useCatalogService(
      selectedId,
      selectedId !== "",
    );

  const response =
    servicesQuery.data;

  const services = useMemo(
    () => response?.items ?? [],
    [response?.items],
  );

  const pagination =
    response?.pagination;

  const visibleTotals = useMemo(
    () => ({
      published: services.filter(
        (service) =>
          service.status
          === "published",
      ).length,
      scheduled: services.filter(
        (service) =>
          service.status
          === "scheduled",
      ).length,
      featured: services.filter(
        (service) =>
          service.is_featured,
      ).length,
      public: services.filter(
        (service) =>
          service.is_publicly_available,
      ).length,
    }),
    [services],
  );

  function updateFilters(
    values:
      Partial<ServiceFilters>,
  ) {
    setFilters(
      (current) => ({
        ...current,
        ...values,
        page:
          values.page
          ?? (
            "page" in values
              ? current.page
              : 1
          ),
      }),
    );
  }

  return (
    <div className="space-y-6 pb-10">
      <header className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Public service catalogue
          </p>

          <h1 className="mt-2 text-2xl font-bold">
            Services Catalog
          </h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Manage LKP service pages, lifecycle,
            publication schedules, public visibility,
            nested content, SEO, and revision history
            consumed by the Astro website.
          </p>
        </div>

        <button
          type="button"
          disabled
          title="The complete service editor is the next milestone."
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white opacity-60"
        >
          <Plus size={16} />
          Create service
        </button>
      </header>

      {notice && (
        <div className="flex items-center justify-between rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm font-medium text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950/30 dark:text-emerald-300">
          <span className="flex items-center gap-2">
            <CheckCircle2 size={18} />
            {notice}
          </span>

          <button
            type="button"
            onClick={() =>
              setNotice("")
            }
            aria-label="Dismiss notice"
          >
            <X size={17} />
          </button>
        </div>
      )}

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Summary
          label="Published on page"
          value={
            visibleTotals.published
          }
          icon={Rocket}
        />
        <Summary
          label="Scheduled on page"
          value={
            visibleTotals.scheduled
          }
          icon={CalendarClock}
        />
        <Summary
          label="Featured on page"
          value={
            visibleTotals.featured
          }
          icon={Star}
        />
        <Summary
          label="Publicly available"
          value={visibleTotals.public}
          icon={Globe2}
        />
      </section>

      <section className="rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
        <div className="grid gap-3 border-b border-slate-200 p-4 xl:grid-cols-[2fr_1fr_1fr_1fr_1fr_auto] dark:border-slate-800">
          <label className="relative">
            <Search
              size={16}
              className="absolute left-3 top-3 text-slate-400"
            />

            <input
              value={filters.search}
              onChange={(event) =>
                updateFilters({
                  search:
                    event.target.value,
                })
              }
              placeholder="Search services…"
              className="h-10 w-full rounded-lg border border-slate-200 bg-white pl-9 pr-3 text-sm dark:border-slate-700 dark:bg-slate-950"
            />
          </label>

          <select
            value={filters.status}
            onChange={(event) =>
              updateFilters({
                status:
                  event.target.value as | ServiceStatus
                    | "",
              })
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
          >
            <option value="">
              All statuses
            </option>

            {serviceStatuses.map(
              (status) => (
                <option
                  key={status}
                  value={status}
                >
                  {serviceStatusLabels[
                    status
                  ]}
                </option>
              ),
            )}
          </select>

          <select
            value={
              filters.featuredState
            }
            onChange={(event) =>
              updateFilters({
                featuredState:
                  event.target.value as ServiceFilters[
                      "featuredState"
                    ],
              })
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
          >
            <option value="all">
              All prominence
            </option>
            <option value="featured">
              Featured
            </option>
            <option value="standard">
              Standard
            </option>
          </select>

          <select
            value={filters.activeState}
            onChange={(event) =>
              updateFilters({
                activeState:
                  event.target.value as ServiceFilters[
                      "activeState"
                    ],
              })
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
          >
            <option value="all">
              All activity
            </option>
            <option value="active">
              Active
            </option>
            <option value="inactive">
              Inactive
            </option>
          </select>

          <select
            value={filters.ordering}
            onChange={(event) =>
              updateFilters({
                ordering:
                  event.target.value,
              })
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
          >
            <option value="sort_order">
              Manual order
            </option>
            <option value="title">
              Title A–Z
            </option>
            <option value="-title">
              Title Z–A
            </option>
            <option value="-updated_at">
              Recently updated
            </option>
            <option value="-created_at">
              Recently created
            </option>
            <option value="-published_at">
              Recently published
            </option>
          </select>

          <button
            type="button"
            onClick={() =>
              setFilters(
                defaultFilters,
              )
            }
            className="inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 text-sm font-semibold dark:border-slate-700"
          >
            <FilterX size={16} />
            Clear
          </button>
        </div>

        {servicesQuery.isLoading && (
          <div className="space-y-3 p-5">
            {Array.from({
              length: 7,
            }).map((_, index) => (
              <div
                key={index}
                className="h-20 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800"
              />
            ))}
          </div>
        )}

        {servicesQuery.isError && (
          <div className="m-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            {
              servicesQuery.error
                .message
            }
          </div>
        )}

        {!servicesQuery.isLoading
        && !servicesQuery.isError
        && services.length === 0 && (
          <div className="px-5 py-16 text-center">
            <Rocket
              size={36}
              className="mx-auto text-slate-300"
            />

            <h2 className="mt-4 font-semibold">
              No services found
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Adjust the filters or create
              the first service in the next
              milestone.
            </p>
          </div>
        )}

        {services.length > 0 && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
              <thead className="bg-slate-50 dark:bg-slate-950/40">
                <tr className="text-left text-xs font-semibold uppercase tracking-wider text-slate-400">
                  <th className="px-4 py-3">
                    Service
                  </th>
                  <th className="px-4 py-3">
                    Status
                  </th>
                  <th className="px-4 py-3">
                    Revision
                  </th>
                  <th className="px-4 py-3">
                    Publication
                  </th>
                  <th className="px-4 py-3">
                    Visibility
                  </th>
                  <th className="px-4 py-3 text-right">
                    Actions
                  </th>
                </tr>
              </thead>

              <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                {services.map(
                  (service) => (
                    <ServiceRow
                      key={service.id}
                      service={service}
                      onInspect={() =>
                        setSelectedId(
                          service.id,
                        )
                      }
                      onSchedule={() => {
                        setSelectedId(
                          service.id,
                        );
                        setDialog(
                          "schedule",
                        );
                      }}
                      onDelete={() => {
                        setSelectedId(
                          service.id,
                        );
                        setDialog(
                          "delete",
                        );
                      }}
                      onNotice={
                        setNotice
                      }
                    />
                  ),
                )}
              </tbody>
            </table>
          </div>
        )}

        {pagination
        && pagination.total_pages > 1 && (
          <footer className="flex flex-col gap-3 border-t border-slate-200 px-5 py-4 sm:flex-row sm:items-center sm:justify-between dark:border-slate-800">
            <p className="text-sm text-slate-500">
              Page {pagination.page} of{" "}
              {pagination.total_pages}
              {" · "}
              {pagination.total_items}
              {" services"}
            </p>

            <div className="flex gap-2">
              <button
                type="button"
                disabled={
                  pagination.page <= 1
                }
                onClick={() =>
                  updateFilters({
                    page:
                      pagination.page
                      - 1,
                  })
                }
                className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-3 py-2 text-sm disabled:opacity-40 dark:border-slate-700"
              >
                <ChevronLeft size={16} />
                Previous
              </button>

              <button
                type="button"
                disabled={
                  pagination.page
                  >= pagination.total_pages
                }
                onClick={() =>
                  updateFilters({
                    page:
                      pagination.page
                      + 1,
                  })
                }
                className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-3 py-2 text-sm disabled:opacity-40 dark:border-slate-700"
              >
                Next
                <ChevronRight size={16} />
              </button>
            </div>
          </footer>
        )}
      </section>

      <ServicePanel
        service={
          detailQuery.data ?? null
        }
        loading={
          detailQuery.isLoading
        }
        onClose={() =>
          setSelectedId("")
        }
      />

      <ServiceDialog
        dialog={dialog}
        service={
          detailQuery.data ?? null
        }
        onClose={() =>
          setDialog(null)
        }
        onNotice={setNotice}
      />
    </div>
  );
}

function Summary({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: number;
  icon: typeof Rocket;
}) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          {label}
        </p>
        <Icon
          size={17}
          className="text-slate-400"
        />
      </div>

      <p className="mt-3 text-2xl font-bold">
        {value}
      </p>
    </article>
  );
}

function ServiceRow({
  service,
  onInspect,
  onSchedule,
  onDelete,
  onNotice,
}: {
  service: CatalogService;
  onInspect: () => void;
  onSchedule: () => void;
  onDelete: () => void;
  onNotice: (value: string) => void;
}) {
  const publishMutation =
    usePublishService();

  async function publish() {
    try {
      const updated =
        await publishMutation.mutateAsync(
          service.id,
        );

      onNotice(
        `“${updated.title}” was published.`,
      );
    } catch {
      onNotice(
        `Unable to publish “${service.title}”.`,
      );
    }
  }

  return (
    <tr className="text-sm">
      <td className="px-4 py-4">
        <button
          type="button"
          onClick={onInspect}
          className="text-left"
        >
          <p className="font-semibold">
            {service.title}
          </p>

          <p className="mt-1 text-xs text-slate-500">
            /{service.slug}
          </p>
        </button>
      </td>

      <td className="px-4 py-4">
        <span
          className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${statusClasses(service.status)}`}
        >
          {
            serviceStatusLabels[
              service.status
            ]
          }
        </span>
      </td>

      <td className="px-4 py-4">
        v{service.current_revision_number}
      </td>

      <td className="px-4 py-4 text-xs text-slate-500">
        {service.status
          === "scheduled"
          ? formatDateTime(
              service.scheduled_for,
            )
          : formatDateTime(
              service.published_at,
            )}
      </td>

      <td className="px-4 py-4">
        <div className="flex flex-wrap gap-2">
          {service.is_featured && (
            <span className="rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-700 dark:bg-amber-950/40 dark:text-amber-300">
              Featured
            </span>
          )}

          <span
            className={`rounded-full px-2.5 py-1 text-xs font-semibold ${
              service.is_active
                ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
                : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300"
            }`}
          >
            {service.is_active
              ? "Active"
              : "Inactive"}
          </span>

          {service
            .is_publicly_available && (
            <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-950/40 dark:text-blue-300">
              Public
            </span>
          )}
        </div>
      </td>

      <td className="px-4 py-4">
        <div className="flex justify-end gap-2">
          {service.status
          !== "published" && (
            <button
              type="button"
              disabled={
                publishMutation.isPending
              }
              onClick={() => {
                void publish();
              }}
              className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold disabled:opacity-50 dark:border-slate-700"
            >
              {publishMutation.isPending
                ? (
                  <LoaderCircle
                    size={13}
                    className="animate-spin"
                  />
                )
                : (
                  <Rocket size={13} />
                )}
              Publish
            </button>
          )}

          <button
            type="button"
            onClick={onSchedule}
            className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
          >
            <CalendarClock size={13} />
            Schedule
          </button>

          <button
            type="button"
            onClick={onInspect}
            className="rounded-lg border border-slate-200 p-2 dark:border-slate-700"
            aria-label={`Inspect ${service.title}`}
          >
            <Eye size={14} />
          </button>

          <button
            type="button"
            disabled
            title="The nested service editor is the next milestone."
            className="rounded-lg border border-slate-200 p-2 opacity-40 dark:border-slate-700"
            aria-label={`Edit ${service.title}`}
          >
            <Pencil size={14} />
          </button>

          <button
            type="button"
            onClick={onDelete}
            className="rounded-lg border border-red-200 p-2 text-red-600 dark:border-red-900"
            aria-label={`Delete ${service.title}`}
          >
            <Trash2 size={14} />
          </button>
        </div>
      </td>
    </tr>
  );
}

function ServicePanel({
  service,
  loading,
  onClose,
}: {
  service: CatalogService | null;
  loading: boolean;
  onClose: () => void;
}) {
  if (!service && !loading) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close service details"
        className="fixed inset-0 z-40 bg-slate-950/50"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-4xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-950">
        <header className="flex items-center justify-between border-b border-slate-200 p-5 dark:border-slate-800">
          <h2 className="font-semibold">
            Service details
          </h2>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close service details"
          >
            <X size={19} />
          </button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {loading && (
            <div className="h-96 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
          )}

          {service && (
            <>
              <h3 className="text-2xl font-bold">
                {service.title}
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                /{service.slug}
              </p>

              <p className="mt-4 text-sm leading-6 text-slate-600 dark:text-slate-300">
                {
                  service.short_description
                  || "No short description."
                }
              </p>

              <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                <Meta
                  label="Status"
                  value={
                    serviceStatusLabels[
                      service.status
                    ]
                  }
                />
                <Meta
                  label="Revision"
                  value={`v${service.current_revision_number}`}
                />
                <Meta
                  label="Features"
                  value={String(
                    service.features.length,
                  )}
                />
                <Meta
                  label="FAQs"
                  value={String(
                    service.faqs.length,
                  )}
                />
              </div>

              <section className="mt-6 grid gap-5 lg:grid-cols-2">
                <DetailSection
                  title="Publication"
                  rows={[
                    [
                      "Published",
                      formatDateTime(
                        service.published_at,
                      ),
                    ],
                    [
                      "Scheduled",
                      formatDateTime(
                        service.scheduled_for,
                      ),
                    ],
                    [
                      "Public",
                      service
                        .is_publicly_available
                        ? "Yes"
                        : "No",
                    ],
                    [
                      "Featured",
                      service.is_featured
                        ? "Yes"
                        : "No",
                    ],
                    [
                      "Active",
                      service.is_active
                        ? "Yes"
                        : "No",
                    ],
                  ]}
                />

                <DetailSection
                  title="Calls to action"
                  rows={[
                    [
                      "Title",
                      service.cta_title,
                    ],
                    [
                      "Text",
                      service.cta_text,
                    ],
                    [
                      "Label",
                      service.cta_label,
                    ],
                    [
                      "URL",
                      service.cta_url,
                    ],
                  ]}
                />
              </section>

              <SectionList
                title="Features"
                items={service.features.map(
                  (item) => ({
                    title: item.title,
                    description:
                      item.description,
                  }),
                )}
              />

              <SectionList
                title="Process"
                items={
                  service.process_steps.map(
                    (item) => ({
                      title:
                        `${item.step_number}. ${item.title}`,
                      description:
                        item.description,
                    }),
                  )
                }
              />

              <SectionList
                title="Technologies"
                items={
                  service.technologies.map(
                    (item) => ({
                      title: item.name,
                      description:
                        item.description,
                    }),
                  )
                }
              />

              <SectionList
                title="FAQs"
                items={service.faqs.map(
                  (item) => ({
                    title:
                      item.question,
                    description:
                      item.answer,
                  }),
                )}
              />

              <section className="mt-6">
                <h4 className="font-semibold">
                  Revisions
                </h4>

                <div className="mt-3 space-y-2">
                  {service.revisions.map(
                    (revision) => (
                      <div
                        key={revision.id}
                        className="rounded-xl border border-slate-200 p-4 dark:border-slate-800"
                      >
                        <div className="flex items-center justify-between gap-3">
                          <p className="font-semibold">
                            Revision{" "}
                            {
                              revision
                                .revision_number
                            }
                          </p>

                          <span className="text-xs text-slate-500">
                            {formatDateTime(
                              revision
                                .created_at,
                            )}
                          </span>
                        </div>

                        <p className="mt-2 text-sm text-slate-500">
                          {
                            revision
                              .change_summary
                            || "No change summary."
                          }
                        </p>
                      </div>
                    ),
                  )}
                </div>
              </section>
            </>
          )}
        </div>
      </aside>
    </>
  );
}

function Meta({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
        {label}
      </p>

      <p className="mt-2 text-sm font-semibold">
        {value}
      </p>
    </div>
  );
}

function DetailSection({
  title,
  rows,
}: {
  title: string;
  rows: [string, string][];
}) {
  return (
    <div className="rounded-xl border border-slate-200 p-5 dark:border-slate-800">
      <h4 className="font-semibold">
        {title}
      </h4>

      <dl className="mt-4 space-y-3">
        {rows.map(
          ([label, value]) => (
            <div
              key={label}
              className="grid grid-cols-[110px_1fr] gap-3 text-sm"
            >
              <dt className="text-slate-500">
                {label}
              </dt>
              <dd className="break-all">
                {value || "—"}
              </dd>
            </div>
          ),
        )}
      </dl>
    </div>
  );
}

function SectionList({
  title,
  items,
}: {
  title: string;
  items: {
    title: string;
    description: string;
  }[];
}) {
  return (
    <section className="mt-6">
      <h4 className="font-semibold">
        {title}
      </h4>

      {items.length === 0 ? (
        <p className="mt-2 text-sm text-slate-500">
          No items.
        </p>
      ) : (
        <div className="mt-3 space-y-2">
          {items.map(
            (item, index) => (
              <div
                key={`${item.title}-${index}`}
                className="rounded-xl border border-slate-200 p-4 dark:border-slate-800"
              >
                <p className="font-semibold">
                  {item.title}
                </p>

                <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-500">
                  {
                    item.description
                    || "—"
                  }
                </p>
              </div>
            ),
          )}
        </div>
      )}
    </section>
  );
}

function ServiceDialog({
  dialog,
  service,
  onClose,
  onNotice,
}: {
  dialog: Dialog;
  service: CatalogService | null;
  onClose: () => void;
  onNotice: (value: string) => void;
}) {
  const scheduleMutation =
    useScheduleService();

  const deleteMutation =
    useDeleteService();

  const [
    scheduledFor,
    setScheduledFor,
  ] = useState("");

  const [
    error,
    setError,
  ] = useState("");

  if (!dialog) {
    return null;
  }

  const pending =
    scheduleMutation.isPending
    || deleteMutation.isPending;

  async function schedule() {
    if (!service) {
      return;
    }

    setError("");

    try {
      if (!scheduledFor) {
        throw new Error(
          "Select a future publication time.",
        );
      }

      const date =
        new Date(scheduledFor);

      if (
        Number.isNaN(date.getTime())
        || date <= new Date()
      ) {
        throw new Error(
          "Scheduled publication time must be in the future.",
        );
      }

      const updated =
        await scheduleMutation.mutateAsync({
          serviceId: service.id,
          payload: {
            scheduled_for:
              date.toISOString(),
          },
        });

      onNotice(
        `“${updated.title}” was scheduled.`,
      );
      onClose();
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Scheduling failed.",
      );
    }
  }

  async function remove() {
    if (!service) {
      return;
    }

    setError("");

    try {
      const message =
        await deleteMutation.mutateAsync(
          service.id,
        );

      onNotice(message);
      onClose();
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Deletion failed.",
      );
    }
  }

  return (
    <>
      <button
        type="button"
        disabled={pending}
        onClick={onClose}
        aria-label="Close service dialog"
        className="fixed inset-0 z-[60] bg-slate-950/60"
      />

      <div
        role="dialog"
        aria-modal="true"
        className="fixed left-1/2 top-1/2 z-[70] w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl dark:border-slate-800 dark:bg-slate-900"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">
            {dialog === "schedule"
              ? "Schedule publication"
              : "Delete service"}
          </h2>

          <button
            type="button"
            disabled={pending}
            onClick={onClose}
            aria-label="Close dialog"
          >
            <X size={18} />
          </button>
        </div>

        {!service ? (
          <div className="mt-5 flex items-center gap-2 text-sm text-slate-500">
            <LoaderCircle
              size={16}
              className="animate-spin"
            />
            Loading service…
          </div>
        ) : dialog === "schedule" ? (
          <div className="mt-5">
            <p className="text-sm text-slate-500">
              Schedule{" "}
              <strong>
                {service.title}
              </strong>{" "}
              for a future date and time.
            </p>

            <label className="mt-4 block space-y-1.5">
              <span className="text-sm font-semibold">
                Publication time
              </span>

              <input
                type="datetime-local"
                value={scheduledFor}
                onChange={(event) =>
                  setScheduledFor(
                    event.target.value,
                  )
                }
                className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
              />
            </label>

            {error && (
              <ErrorBox value={error} />
            )}

            <button
              type="button"
              disabled={pending}
              onClick={() => {
                void schedule();
              }}
              className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50"
            >
              {pending && (
                <LoaderCircle
                  size={16}
                  className="animate-spin"
                />
              )}
              Schedule service
            </button>
          </div>
        ) : (
          <div className="mt-5">
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm leading-6 text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              Soft-delete{" "}
              <strong>
                {service.title}
              </strong>
              ? It will be removed from normal
              queries while remaining available
              to the backend audit trail.
            </div>

            {error && (
              <ErrorBox value={error} />
            )}

            <button
              type="button"
              disabled={pending}
              onClick={() => {
                void remove();
              }}
              className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50"
            >
              {pending && (
                <LoaderCircle
                  size={16}
                  className="animate-spin"
                />
              )}
              Delete service
            </button>
          </div>
        )}
      </div>
    </>
  );
}

function ErrorBox({
  value,
}: {
  value: string;
}) {
  return (
    <p className="mt-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
      {value}
    </p>
  );
}
