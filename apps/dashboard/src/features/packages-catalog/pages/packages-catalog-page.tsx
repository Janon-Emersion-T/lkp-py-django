import {
  CalendarClock,
  Check,
  ChevronLeft,
  ChevronRight,
  Eye,
  FilterX,
  Globe2,
  LoaderCircle,
  PackageOpen,
  Rocket,
  Search,
  Sparkles,
  Star,
  Trash2,
  X,
} from "lucide-react";
import { useMemo, useState, type ReactNode } from "react";

import {
  billingCycleLabels,
  formatDateTime,
  formatPackagePrice,
  packageCategoryLabels,
  packageStatusLabels,
  pricingTypeLabels,
  statusClasses,
} from "../formatters";
import {
  useCatalogPackage,
  useDeletePackage,
  usePackagesCatalog,
  usePublishPackage,
  useSchedulePackage,
} from "../hooks";
import {
  billingCycles,
  packageCategories,
  packageStatuses,
  type CatalogPackage,
  type PackageFilters,
} from "../types";

const defaultFilters: PackageFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  category: "",
  status: "",
  currency: "",
  billingCycle: "",
  featuredState: "all",
  popularState: "all",
  activeState: "all",
  ordering: "sort_order",
};

type Dialog = "schedule" | "delete" | null;

function mutationError(error: unknown): string {
  return error instanceof Error
    ? error.message
    : "The operation could not be completed.";
}

export function PackagesCatalogPage() {
  const [filters, setFilters] = useState(defaultFilters);

  const [selectedId, setSelectedId] = useState("");

  const [dialog, setDialog] = useState<Dialog>(null);

  const [scheduleValue, setScheduleValue] = useState("");

  const [notice, setNotice] = useState("");

  const [operationError, setOperationError] = useState("");

  const packagesQuery = usePackagesCatalog(filters);

  const detailQuery = useCatalogPackage(selectedId, selectedId !== "");

  const publishMutation = usePublishPackage();

  const scheduleMutation = useSchedulePackage();

  const deleteMutation = useDeletePackage();

  const packages = useMemo(
    () => packagesQuery.data?.items ?? [],
    [packagesQuery.data?.items],
  );

  const pagination = packagesQuery.data?.pagination;

  const selectedPackage = detailQuery.data;

  const visibleTotals = useMemo(
    () => ({
      published: packages.filter((item) => item.status === "published").length,
      featured: packages.filter((item) => item.is_featured).length,
      popular: packages.filter((item) => item.is_popular).length,
      public: packages.filter((item) => item.is_publicly_available).length,
    }),
    [packages],
  );

  const isMutating =
    publishMutation.isPending ||
    scheduleMutation.isPending ||
    deleteMutation.isPending;

  function updateFilters(values: Partial<PackageFilters>) {
    setFilters((current) => ({
      ...current,
      ...values,
      page:
        values.page ??
        (Object.keys(values).some((key) => key !== "page") ? 1 : current.page),
    }));
  }

  function resetFeedback() {
    setNotice("");
    setOperationError("");
  }

  async function publishSelected(item: CatalogPackage) {
    resetFeedback();

    try {
      await publishMutation.mutateAsync(item.id);
      setNotice(`${item.name} was published.`);
    } catch (error) {
      setOperationError(mutationError(error));
    }
  }

  async function scheduleSelected() {
    if (!selectedPackage || !scheduleValue) {
      return;
    }

    resetFeedback();

    try {
      await scheduleMutation.mutateAsync({
        packageId: selectedPackage.id,
        payload: {
          scheduled_for: new Date(scheduleValue).toISOString(),
        },
      });

      setNotice(`${selectedPackage.name} was scheduled.`);
      setDialog(null);
      setScheduleValue("");
    } catch (error) {
      setOperationError(mutationError(error));
    }
  }

  async function deleteSelected() {
    if (!selectedPackage) {
      return;
    }

    resetFeedback();

    try {
      const message = await deleteMutation.mutateAsync(selectedPackage.id);

      setNotice(message);
      setDialog(null);
      setSelectedId("");
    } catch (error) {
      setOperationError(mutationError(error));
    }
  }

  return (
    <div className="space-y-6">
      <section className="flex flex-col gap-4 rounded-3xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-950 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <div className="flex items-center gap-2 text-sm font-semibold text-indigo-600 dark:text-indigo-400">
            <PackageOpen className="h-4 w-4" />
            Commercial catalogue
          </div>

          <h1 className="mt-2 text-2xl font-bold tracking-tight text-slate-950 dark:text-white">
            Packages Catalog
          </h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-600 dark:text-slate-400">
            Manage packaged services, pricing, availability, included features,
            add-ons, target audiences, FAQs, publishing and revision visibility.
          </p>
        </div>

        <div className="rounded-2xl border border-indigo-200 bg-indigo-50 px-4 py-3 text-sm text-indigo-800 dark:border-indigo-900 dark:bg-indigo-950/40 dark:text-indigo-200">
          Creation and editing will be delivered in the next package editor
          milestone.
        </div>
      </section>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {[
          {
            label: "Published",
            value: visibleTotals.published,
            icon: Rocket,
          },
          {
            label: "Featured",
            value: visibleTotals.featured,
            icon: Star,
          },
          {
            label: "Popular",
            value: visibleTotals.popular,
            icon: Sparkles,
          },
          {
            label: "Publicly available",
            value: visibleTotals.public,
            icon: Globe2,
          },
        ].map((metric) => (
          <article
            key={metric.label}
            className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950"
          >
            <div className="flex items-center justify-between">
              <p className="text-sm font-medium text-slate-500 dark:text-slate-400">
                {metric.label}
              </p>
              <metric.icon className="h-5 w-5 text-indigo-500" />
            </div>
            <p className="mt-3 text-3xl font-bold text-slate-950 dark:text-white">
              {metric.value}
            </p>
            <p className="mt-1 text-xs text-slate-500">Current page</p>
          </article>
        ))}
      </section>

      {(notice || operationError) && (
        <section
          className={
            operationError
              ? "rounded-2xl border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-300"
              : "rounded-2xl border border-emerald-200 bg-emerald-50 px-4 py-3 text-sm text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300"
          }
        >
          {operationError || notice}
        </section>
      )}

      <section className="rounded-3xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-950">
        <div className="grid gap-3 border-b border-slate-200 p-5 dark:border-slate-800 md:grid-cols-2 xl:grid-cols-6">
          <label className="relative xl:col-span-2">
            <Search className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-slate-400" />
            <input
              value={filters.search}
              onChange={(event) =>
                updateFilters({
                  search: event.target.value,
                })
              }
              placeholder="Search packages"
              className="h-10 w-full rounded-xl border border-slate-300 bg-white pl-10 pr-3 text-sm outline-none transition focus:border-indigo-500 dark:border-slate-700 dark:bg-slate-900"
            />
          </label>

          <select
            value={filters.category}
            onChange={(event) =>
              updateFilters({
                category: event.target.value as PackageFilters["category"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All categories</option>
            {packageCategories.map((category) => (
              <option key={category} value={category}>
                {packageCategoryLabels[category]}
              </option>
            ))}
          </select>

          <select
            value={filters.status}
            onChange={(event) =>
              updateFilters({
                status: event.target.value as PackageFilters["status"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All statuses</option>
            {packageStatuses.map((status) => (
              <option key={status} value={status}>
                {packageStatusLabels[status]}
              </option>
            ))}
          </select>

          <select
            value={filters.billingCycle}
            onChange={(event) =>
              updateFilters({
                billingCycle: event.target
                  .value as PackageFilters["billingCycle"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All billing cycles</option>
            {billingCycles.map((cycle) => (
              <option key={cycle} value={cycle}>
                {billingCycleLabels[cycle]}
              </option>
            ))}
          </select>

          <button
            type="button"
            onClick={() => setFilters(defaultFilters)}
            className="inline-flex h-10 items-center justify-center gap-2 rounded-xl border border-slate-300 px-3 text-sm font-semibold text-slate-700 hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-900"
          >
            <FilterX className="h-4 w-4" />
            Reset
          </button>

          <select
            value={filters.featuredState}
            onChange={(event) =>
              updateFilters({
                featuredState: event.target
                  .value as PackageFilters["featuredState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any prominence</option>
            <option value="featured">Featured only</option>
            <option value="standard">Non-featured</option>
          </select>

          <select
            value={filters.popularState}
            onChange={(event) =>
              updateFilters({
                popularState: event.target
                  .value as PackageFilters["popularState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any popularity</option>
            <option value="popular">Popular only</option>
            <option value="standard">Not popular</option>
          </select>

          <select
            value={filters.activeState}
            onChange={(event) =>
              updateFilters({
                activeState: event.target
                  .value as PackageFilters["activeState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any activity state</option>
            <option value="active">Active only</option>
            <option value="inactive">Inactive only</option>
          </select>

          <input
            value={filters.currency}
            onChange={(event) =>
              updateFilters({
                currency: event.target.value,
              })
            }
            maxLength={3}
            placeholder="Currency"
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm uppercase dark:border-slate-700 dark:bg-slate-900"
          />

          <select
            value={filters.ordering}
            onChange={(event) =>
              updateFilters({
                ordering: event.target.value,
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900 xl:col-span-2"
          >
            <option value="sort_order">Sort order</option>
            <option value="name">Name A–Z</option>
            <option value="-name">Name Z–A</option>
            <option value="price">Price low to high</option>
            <option value="-price">Price high to low</option>
            <option value="-updated_at">Recently updated</option>
          </select>
        </div>

        {packagesQuery.isLoading ? (
          <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
            <LoaderCircle className="h-5 w-5 animate-spin" />
            Loading packages…
          </div>
        ) : packagesQuery.isError ? (
          <div className="p-8 text-center">
            <p className="font-semibold text-rose-600">
              Packages could not be loaded.
            </p>
            <p className="mt-2 text-sm text-slate-500">
              {mutationError(packagesQuery.error)}
            </p>
          </div>
        ) : packages.length === 0 ? (
          <div className="p-10 text-center">
            <PackageOpen className="mx-auto h-10 w-10 text-slate-300" />
            <p className="mt-3 font-semibold text-slate-700 dark:text-slate-300">
              No packages match the current filters.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-slate-200 dark:divide-slate-800">
            {packages.map((item) => (
              <article
                key={item.id}
                className="grid gap-4 p-5 transition hover:bg-slate-50 dark:hover:bg-slate-900/50 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
              >
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="font-semibold text-slate-950 dark:text-white">
                      {item.name}
                    </h2>

                    <span
                      className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${statusClasses(item.status)}`}
                    >
                      {packageStatusLabels[item.status]}
                    </span>

                    {item.is_featured && (
                      <span className="rounded-full bg-violet-100 px-2 py-0.5 text-xs font-semibold text-violet-700 dark:bg-violet-950 dark:text-violet-300">
                        Featured
                      </span>
                    )}

                    {item.is_popular && (
                      <span className="rounded-full bg-fuchsia-100 px-2 py-0.5 text-xs font-semibold text-fuchsia-700 dark:bg-fuchsia-950 dark:text-fuchsia-300">
                        Popular
                      </span>
                    )}
                  </div>

                  <p className="mt-1 text-sm text-slate-500">/{item.slug}</p>

                  <p className="mt-2 line-clamp-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
                    {item.short_description || "No short description supplied."}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-xs text-slate-500">
                    <span>{packageCategoryLabels[item.category]}</span>
                    <span>{billingCycleLabels[item.billing_cycle]}</span>
                    <span>{item.service_title || "No linked service"}</span>
                    <span>Revision {item.current_revision_number}</span>
                  </div>
                </div>

                <div>
                  <p className="text-lg font-bold text-slate-950 dark:text-white">
                    {formatPackagePrice({
                      pricingType: item.pricing_type,
                      price: item.price,
                      currency: item.currency,
                    })}
                  </p>

                  <p className="mt-1 text-xs text-slate-500">
                    {pricingTypeLabels[item.pricing_type]}
                  </p>

                  <p className="mt-3 text-xs text-slate-500">
                    Updated {formatDateTime(item.updated_at)}
                  </p>
                </div>

                <div className="flex flex-wrap items-start gap-2 lg:justify-end">
                  <button
                    type="button"
                    onClick={() => {
                      resetFeedback();
                      setSelectedId(item.id);
                    }}
                    className="inline-flex h-9 items-center gap-2 rounded-lg border border-slate-300 px-3 text-sm font-semibold hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-800"
                  >
                    <Eye className="h-4 w-4" />
                    Inspect
                  </button>

                  {item.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(item)}
                      className="inline-flex h-9 items-center gap-2 rounded-lg bg-indigo-600 px-3 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-50"
                    >
                      <Rocket className="h-4 w-4" />
                      Publish
                    </button>
                  )}
                </div>
              </article>
            ))}
          </div>
        )}

        <div className="flex flex-col gap-3 border-t border-slate-200 p-5 dark:border-slate-800 sm:flex-row sm:items-center sm:justify-between">
          <p className="text-sm text-slate-500">
            Page {pagination?.page ?? 1} of{" "}
            {Math.max(pagination?.total_pages ?? 1, 1)} ·{" "}
            {pagination?.total_items ?? 0} packages
          </p>

          <div className="flex gap-2">
            <button
              type="button"
              disabled={!pagination || pagination.page <= 1}
              onClick={() =>
                updateFilters({
                  page: filters.page - 1,
                })
              }
              className="inline-flex h-9 items-center gap-2 rounded-lg border border-slate-300 px-3 text-sm font-semibold disabled:opacity-40 dark:border-slate-700"
            >
              <ChevronLeft className="h-4 w-4" />
              Previous
            </button>

            <button
              type="button"
              disabled={
                !pagination || pagination.page >= pagination.total_pages
              }
              onClick={() =>
                updateFilters({
                  page: filters.page + 1,
                })
              }
              className="inline-flex h-9 items-center gap-2 rounded-lg border border-slate-300 px-3 text-sm font-semibold disabled:opacity-40 dark:border-slate-700"
            >
              Next
              <ChevronRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      </section>

      {selectedId && (
        <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/50">
          <aside className="h-full w-full max-w-2xl overflow-y-auto bg-white shadow-2xl dark:bg-slate-950">
            <div className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white/95 p-5 backdrop-blur dark:border-slate-800 dark:bg-slate-950/95">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-indigo-600">
                  Package record
                </p>
                <h2 className="mt-1 text-xl font-bold">
                  {selectedPackage?.name || "Loading package"}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => {
                  setSelectedId("");
                  setDialog(null);
                }}
                className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800"
                aria-label="Close package details"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {detailQuery.isLoading ? (
              <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
                <LoaderCircle className="h-5 w-5 animate-spin" />
                Loading package details…
              </div>
            ) : detailQuery.isError || !selectedPackage ? (
              <div className="p-6 text-sm text-rose-600">
                Package details could not be loaded.
              </div>
            ) : (
              <div className="space-y-6 p-6">
                <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
                  <Detail
                    label="Price"
                    value={formatPackagePrice({
                      pricingType: selectedPackage.pricing_type,
                      price: selectedPackage.price,
                      currency: selectedPackage.currency,
                    })}
                  />
                  <Detail
                    label="Billing"
                    value={billingCycleLabels[selectedPackage.billing_cycle]}
                  />
                  <Detail
                    label="Category"
                    value={packageCategoryLabels[selectedPackage.category]}
                  />
                  <Detail
                    label="Linked service"
                    value={selectedPackage.service_title || "Not linked"}
                  />
                  <Detail
                    label="Delivery time"
                    value={selectedPackage.delivery_time || "Not specified"}
                  />
                  <Detail
                    label="Support"
                    value={`${selectedPackage.support_period_days} days`}
                  />
                  <Detail
                    label="Revisions included"
                    value={String(selectedPackage.revisions_included)}
                  />
                  <Detail
                    label="Current revision"
                    value={String(selectedPackage.current_revision_number)}
                  />
                </section>

                <section>
                  <h3 className="font-semibold">Description</h3>
                  <p className="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
                    {selectedPackage.short_description ||
                      "No description supplied."}
                  </p>
                </section>

                <Collection
                  title="Included features"
                  empty="No package features."
                >
                  {selectedPackage.features.map((feature) => (
                    <div
                      key={feature.id}
                      className="flex gap-3 rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      {feature.is_included ? (
                        <Check className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
                      ) : (
                        <X className="mt-0.5 h-4 w-4 shrink-0 text-rose-500" />
                      )}
                      <div>
                        <p className="text-sm font-semibold">{feature.title}</p>
                        <p className="mt-1 text-xs leading-5 text-slate-500">
                          {feature.description ||
                            feature.value ||
                            "No detail supplied."}
                        </p>
                      </div>
                    </div>
                  ))}
                </Collection>

                <Collection title="Add-ons" empty="No package add-ons.">
                  {selectedPackage.addons.map((addon) => (
                    <div
                      key={addon.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-semibold">{addon.name}</p>
                        <p className="text-sm font-bold">
                          {addon.currency} {addon.price}
                        </p>
                      </div>
                      <p className="mt-1 text-xs leading-5 text-slate-500">
                        {addon.description ||
                          billingCycleLabels[addon.billing_cycle]}
                      </p>
                    </div>
                  ))}
                </Collection>

                <Collection
                  title="Target audiences"
                  empty="No target audiences."
                >
                  {selectedPackage.target_audiences.map((audience) => (
                    <div
                      key={audience.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <p className="text-sm font-semibold">{audience.title}</p>
                      <p className="mt-1 text-xs leading-5 text-slate-500">
                        {audience.description || "No detail supplied."}
                      </p>
                    </div>
                  ))}
                </Collection>

                <Collection title="FAQs" empty="No package FAQs.">
                  {selectedPackage.faqs.map((faq) => (
                    <div
                      key={faq.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <p className="text-sm font-semibold">{faq.question}</p>
                      <p className="mt-1 text-xs leading-5 text-slate-500">
                        {faq.answer}
                      </p>
                    </div>
                  ))}
                </Collection>

                <section className="rounded-2xl border border-slate-200 p-5 dark:border-slate-800">
                  <h3 className="font-semibold">Publishing</h3>

                  <div className="mt-4 grid gap-3 sm:grid-cols-2">
                    <Detail
                      label="Status"
                      value={packageStatusLabels[selectedPackage.status]}
                    />
                    <Detail
                      label="Published"
                      value={formatDateTime(selectedPackage.published_at)}
                    />
                    <Detail
                      label="Scheduled"
                      value={formatDateTime(selectedPackage.scheduled_for)}
                    />
                    <Detail
                      label="Public availability"
                      value={
                        selectedPackage.is_publicly_available
                          ? "Available"
                          : "Unavailable"
                      }
                    />
                  </div>
                </section>

                <section className="flex flex-wrap gap-3 border-t border-slate-200 pt-6 dark:border-slate-800">
                  {selectedPackage.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(selectedPackage)}
                      className="inline-flex h-10 items-center gap-2 rounded-xl bg-indigo-600 px-4 text-sm font-semibold text-white hover:bg-indigo-700 disabled:opacity-50"
                    >
                      <Rocket className="h-4 w-4" />
                      Publish now
                    </button>
                  )}

                  <button
                    type="button"
                    disabled={isMutating}
                    onClick={() => {
                      resetFeedback();
                      setDialog("schedule");
                    }}
                    className="inline-flex h-10 items-center gap-2 rounded-xl border border-slate-300 px-4 text-sm font-semibold hover:bg-slate-100 disabled:opacity-50 dark:border-slate-700 dark:hover:bg-slate-800"
                  >
                    <CalendarClock className="h-4 w-4" />
                    Schedule
                  </button>

                  <button
                    type="button"
                    disabled={isMutating}
                    onClick={() => {
                      resetFeedback();
                      setDialog("delete");
                    }}
                    className="inline-flex h-10 items-center gap-2 rounded-xl border border-rose-300 px-4 text-sm font-semibold text-rose-600 hover:bg-rose-50 disabled:opacity-50 dark:border-rose-900 dark:hover:bg-rose-950/40"
                  >
                    <Trash2 className="h-4 w-4" />
                    Delete
                  </button>
                </section>
              </div>
            )}
          </aside>
        </div>
      )}

      {dialog && selectedPackage && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 p-4">
          <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl dark:bg-slate-950">
            {dialog === "schedule" ? (
              <>
                <CalendarClock className="h-8 w-8 text-indigo-600" />
                <h2 className="mt-4 text-xl font-bold">Schedule publication</h2>
                <p className="mt-2 text-sm text-slate-500">
                  Select a future date and time for {selectedPackage.name}.
                </p>

                <input
                  type="datetime-local"
                  value={scheduleValue}
                  onChange={(event) => setScheduleValue(event.target.value)}
                  className="mt-5 h-11 w-full rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
                />

                <div className="mt-6 flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => setDialog(null)}
                    className="h-10 rounded-xl border border-slate-300 px-4 text-sm font-semibold dark:border-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    disabled={!scheduleValue || isMutating}
                    onClick={() => void scheduleSelected()}
                    className="h-10 rounded-xl bg-indigo-600 px-4 text-sm font-semibold text-white disabled:opacity-50"
                  >
                    Schedule
                  </button>
                </div>
              </>
            ) : (
              <>
                <Trash2 className="h-8 w-8 text-rose-600" />
                <h2 className="mt-4 text-xl font-bold">Delete package?</h2>
                <p className="mt-2 text-sm leading-6 text-slate-500">
                  This will soft delete {selectedPackage.name}. The normal
                  packages list will no longer return it.
                </p>

                <div className="mt-6 flex justify-end gap-3">
                  <button
                    type="button"
                    onClick={() => setDialog(null)}
                    className="h-10 rounded-xl border border-slate-300 px-4 text-sm font-semibold dark:border-slate-700"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    disabled={isMutating}
                    onClick={() => void deleteSelected()}
                    className="h-10 rounded-xl bg-rose-600 px-4 text-sm font-semibold text-white disabled:opacity-50"
                  >
                    Delete package
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>
      <p className="mt-1 text-sm font-semibold text-slate-800 dark:text-slate-200">
        {value}
      </p>
    </div>
  );
}

function Collection({
  title,
  empty,
  children,
}: {
  title: string;
  empty: string;
  children: ReactNode;
}) {
  const childCount = Array.isArray(children)
    ? children.length
    : children
      ? 1
      : 0;

  return (
    <section>
      <h3 className="font-semibold">{title}</h3>
      <div className="mt-3 space-y-2">
        {childCount > 0 ? (
          children
        ) : (
          <p className="rounded-xl border border-dashed border-slate-300 p-4 text-sm text-slate-500 dark:border-slate-700">
            {empty}
          </p>
        )}
      </div>
    </section>
  );
}
