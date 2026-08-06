import {
  Building2,
  CalendarClock,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  Eye,
  FilterX,
  Globe2,
  Landmark,
  LoaderCircle,
  Rocket,
  Search,
  Star,
  Trash2,
  X,
} from "lucide-react";
import { useMemo, useState, type ReactNode } from "react";

import {
  displayContentItem,
  formatDateTime,
  industryStatusLabels,
  statusClasses,
} from "../formatters";
import {
  useCatalogIndustry,
  useDeleteIndustry,
  useIndustriesCatalog,
  usePublishIndustry,
  useScheduleIndustry,
} from "../hooks";
import {
  industryStatuses,
  type CatalogIndustry,
  type IndustryFilters,
} from "../types";

const defaultFilters: IndustryFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  featuredState: "all",
  activeState: "all",
  ordering: "sort_order",
};

type Dialog = "schedule" | "delete" | null;

function errorMessage(error: unknown): string {
  return error instanceof Error
    ? error.message
    : "The operation could not be completed.";
}

export function IndustriesCatalogPage() {
  const [filters, setFilters] = useState(defaultFilters);

  const [selectedId, setSelectedId] = useState("");

  const [dialog, setDialog] = useState<Dialog>(null);

  const [scheduleValue, setScheduleValue] = useState("");

  const [notice, setNotice] = useState("");

  const [operationError, setOperationError] = useState("");

  const industriesQuery = useIndustriesCatalog(filters);

  const detailQuery = useCatalogIndustry(selectedId, selectedId !== "");

  const publishMutation = usePublishIndustry();

  const scheduleMutation = useScheduleIndustry();

  const deleteMutation = useDeleteIndustry();

  const industries = useMemo(
    () => industriesQuery.data?.items ?? [],
    [industriesQuery.data?.items],
  );

  const pagination = industriesQuery.data?.pagination;

  const selectedIndustry = detailQuery.data;

  const totals = useMemo(
    () => ({
      published: industries.filter((item) => item.status === "published")
        .length,
      featured: industries.filter((item) => item.is_featured).length,
      public: industries.filter((item) => item.is_publicly_available).length,
      linkedServices: industries.reduce(
        (total, item) => total + item.services.length,
        0,
      ),
    }),
    [industries],
  );

  const isMutating =
    publishMutation.isPending ||
    scheduleMutation.isPending ||
    deleteMutation.isPending;

  function updateFilters(changes: Partial<IndustryFilters>) {
    setFilters((current) => ({
      ...current,
      ...changes,
      page:
        changes.page ??
        (Object.keys(changes).some((key) => key !== "page") ? 1 : current.page),
    }));
  }

  function resetFeedback() {
    setNotice("");
    setOperationError("");
  }

  async function publishSelected(industry: CatalogIndustry) {
    resetFeedback();

    try {
      await publishMutation.mutateAsync(industry.id);

      setNotice(`${industry.name} was published.`);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function scheduleSelected() {
    if (!selectedIndustry || !scheduleValue) {
      return;
    }

    resetFeedback();

    try {
      await scheduleMutation.mutateAsync({
        industryId: selectedIndustry.id,
        payload: {
          scheduled_for: new Date(scheduleValue).toISOString(),
        },
      });

      setNotice(`${selectedIndustry.name} was scheduled.`);
      setDialog(null);
      setScheduleValue("");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function deleteSelected() {
    if (!selectedIndustry) {
      return;
    }

    resetFeedback();

    try {
      const message = await deleteMutation.mutateAsync(selectedIndustry.id);

      setNotice(message);
      setDialog(null);
      setSelectedId("");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  return (
    <div className="space-y-6 pb-10">
      <header className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Industry solutions catalogue
          </p>

          <h1 className="mt-2 text-2xl font-bold">Industries Catalog</h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Manage industry landing pages, business challenges, solutions,
            benefits, linked services, FAQs, SEO, lifecycle and Astro public
            visibility.
          </p>
        </div>

        <button
          type="button"
          disabled
          title="The complete industry editor is the next milestone."
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white opacity-60"
        >
          <Building2 size={16} />
          Create industry
        </button>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Metric label="Published" value={totals.published} icon={Rocket} />
        <Metric label="Featured" value={totals.featured} icon={Star} />
        <Metric label="Public" value={totals.public} icon={Globe2} />
        <Metric
          label="Linked services"
          value={totals.linkedServices}
          icon={Landmark}
        />
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

      <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-950">
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
              placeholder="Search industries"
              className="h-10 w-full rounded-xl border border-slate-300 bg-white pl-10 pr-3 text-sm outline-none focus:border-blue-500 dark:border-slate-700 dark:bg-slate-900"
            />
          </label>

          <select
            value={filters.status}
            onChange={(event) =>
              updateFilters({
                status: event.target.value as IndustryFilters["status"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All statuses</option>

            {industryStatuses.map((status) => (
              <option key={status} value={status}>
                {industryStatusLabels[status]}
              </option>
            ))}
          </select>

          <select
            value={filters.featuredState}
            onChange={(event) =>
              updateFilters({
                featuredState: event.target
                  .value as IndustryFilters["featuredState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any prominence</option>
            <option value="featured">Featured only</option>
            <option value="standard">Non-featured</option>
          </select>

          <select
            value={filters.activeState}
            onChange={(event) =>
              updateFilters({
                activeState: event.target
                  .value as IndustryFilters["activeState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any activity state</option>
            <option value="active">Active only</option>
            <option value="inactive">Inactive only</option>
          </select>

          <button
            type="button"
            onClick={() => setFilters(defaultFilters)}
            className="inline-flex h-10 items-center justify-center gap-2 rounded-xl border border-slate-300 px-3 text-sm font-semibold hover:bg-slate-50 dark:border-slate-700 dark:hover:bg-slate-900"
          >
            <FilterX className="h-4 w-4" />
            Reset
          </button>

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
            <option value="-updated_at">Recently updated</option>
            <option value="-published_at">Recently published</option>
          </select>
        </div>

        {industriesQuery.isLoading ? (
          <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
            <LoaderCircle className="h-5 w-5 animate-spin" />
            Loading industries…
          </div>
        ) : industriesQuery.isError ? (
          <div className="p-10 text-center">
            <p className="font-semibold text-rose-600">
              Industries could not be loaded.
            </p>
            <p className="mt-2 text-sm text-slate-500">
              {errorMessage(industriesQuery.error)}
            </p>
          </div>
        ) : industries.length === 0 ? (
          <div className="p-10 text-center">
            <Landmark className="mx-auto h-10 w-10 text-slate-300" />
            <p className="mt-3 font-semibold text-slate-700 dark:text-slate-300">
              No industries match the current filters.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-slate-200 dark:divide-slate-800">
            {industries.map((industry) => (
              <article
                key={industry.id}
                className="grid gap-4 p-5 transition hover:bg-slate-50 dark:hover:bg-slate-900/50 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
              >
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="font-semibold text-slate-950 dark:text-white">
                      {industry.name}
                    </h2>

                    <span
                      className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${statusClasses(industry.status)}`}
                    >
                      {industryStatusLabels[industry.status]}
                    </span>

                    {industry.is_featured && (
                      <span className="rounded-full bg-violet-100 px-2 py-0.5 text-xs font-semibold text-violet-700 dark:bg-violet-950 dark:text-violet-300">
                        Featured
                      </span>
                    )}
                  </div>

                  <p className="mt-1 text-sm text-slate-500">
                    /{industry.slug}
                  </p>

                  <p className="mt-2 line-clamp-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
                    {industry.short_description ||
                      industry.hero_description ||
                      "No summary supplied."}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-xs text-slate-500">
                    <span>{industry.services.length} linked services</span>
                    <span>{industry.faqs.length} FAQs</span>
                    <span>Revision {industry.current_revision_number}</span>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <p className="font-semibold text-slate-800 dark:text-slate-200">
                    {industry.hero_title || "No hero title"}
                  </p>
                  <p className="text-xs text-slate-500">
                    Updated {formatDateTime(industry.updated_at)}
                  </p>
                  <p className="text-xs text-slate-500">
                    {industry.is_publicly_available
                      ? "Publicly available"
                      : "Not publicly available"}
                  </p>
                </div>

                <div className="flex flex-wrap items-start gap-2 lg:justify-end">
                  <button
                    type="button"
                    onClick={() => {
                      resetFeedback();
                      setSelectedId(industry.id);
                    }}
                    className="inline-flex h-9 items-center gap-2 rounded-lg border border-slate-300 px-3 text-sm font-semibold hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-800"
                  >
                    <Eye className="h-4 w-4" />
                    Inspect
                  </button>

                  {industry.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(industry)}
                      className="inline-flex h-9 items-center gap-2 rounded-lg bg-blue-600 px-3 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
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
            {pagination?.total_items ?? 0} industries
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
                <p className="text-xs font-semibold uppercase tracking-wider text-blue-600">
                  Industry record
                </p>
                <h2 className="mt-1 text-xl font-bold">
                  {selectedIndustry?.name || "Loading industry"}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => {
                  setSelectedId("");
                  setDialog(null);
                }}
                className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800"
                aria-label="Close industry details"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {detailQuery.isLoading ? (
              <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
                <LoaderCircle className="h-5 w-5 animate-spin" />
                Loading industry details…
              </div>
            ) : detailQuery.isError || !selectedIndustry ? (
              <div className="p-6 text-sm text-rose-600">
                Industry details could not be loaded.
              </div>
            ) : (
              <div className="space-y-6 p-6">
                <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
                  <Detail
                    label="Status"
                    value={industryStatusLabels[selectedIndustry.status]}
                  />
                  <Detail
                    label="Revision"
                    value={String(selectedIndustry.current_revision_number)}
                  />
                  <Detail
                    label="Published"
                    value={formatDateTime(selectedIndustry.published_at)}
                  />
                  <Detail
                    label="Scheduled"
                    value={formatDateTime(selectedIndustry.scheduled_for)}
                  />
                  <Detail
                    label="Featured"
                    value={selectedIndustry.is_featured ? "Yes" : "No"}
                  />
                  <Detail
                    label="Public"
                    value={
                      selectedIndustry.is_publicly_available
                        ? "Available"
                        : "Unavailable"
                    }
                  />
                </section>

                <section>
                  <h3 className="font-semibold">Hero content</h3>
                  <p className="mt-2 text-base font-semibold">
                    {selectedIndustry.hero_title || selectedIndustry.name}
                  </p>
                  <p className="mt-2 text-sm leading-6 text-slate-500">
                    {selectedIndustry.hero_description ||
                      selectedIndustry.short_description ||
                      "No hero description supplied."}
                  </p>
                </section>

                <ContentCollection
                  title="Challenges"
                  values={selectedIndustry.challenges}
                  empty="No industry challenges."
                />

                <ContentCollection
                  title="Solutions"
                  values={selectedIndustry.solutions}
                  empty="No industry solutions."
                />

                <ContentCollection
                  title="Benefits"
                  values={selectedIndustry.benefits}
                  empty="No industry benefits."
                />

                <Collection title="Linked services" empty="No linked services.">
                  {selectedIndustry.services.map((service) => (
                    <div
                      key={service.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <p className="text-sm font-semibold">
                          {service.service_title}
                        </p>

                        {service.is_featured && (
                          <span className="rounded-full bg-violet-100 px-2 py-0.5 text-xs font-semibold text-violet-700 dark:bg-violet-950 dark:text-violet-300">
                            Featured
                          </span>
                        )}
                      </div>

                      <p className="mt-1 text-xs leading-5 text-slate-500">
                        {service.description ||
                          "No industry-specific description."}
                      </p>
                    </div>
                  ))}
                </Collection>

                <Collection title="FAQs" empty="No industry FAQs.">
                  {selectedIndustry.faqs.map((faq) => (
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
                  <h3 className="font-semibold">Conversion CTA</h3>

                  <p className="mt-3 text-sm font-semibold">
                    {selectedIndustry.cta_title || "No CTA title"}
                  </p>

                  <p className="mt-1 text-sm leading-6 text-slate-500">
                    {selectedIndustry.cta_text || "No CTA description."}
                  </p>

                  <p className="mt-3 text-xs text-slate-500">
                    {selectedIndustry.cta_label || "No CTA label"} ·{" "}
                    {selectedIndustry.cta_url || "No CTA URL"}
                  </p>
                </section>

                <section className="rounded-2xl border border-slate-200 p-5 dark:border-slate-800">
                  <h3 className="font-semibold">SEO</h3>

                  <div className="mt-4 grid gap-4 sm:grid-cols-2">
                    <Detail
                      label="Meta title"
                      value={selectedIndustry.seo?.meta_title || "Not supplied"}
                    />
                    <Detail
                      label="Canonical"
                      value={
                        selectedIndustry.seo?.canonical_url || "Not supplied"
                      }
                    />
                    <Detail
                      label="Indexing"
                      value={
                        selectedIndustry.seo?.robots_index
                          ? "Index"
                          : "No index"
                      }
                    />
                    <Detail
                      label="Following"
                      value={
                        selectedIndustry.seo?.robots_follow
                          ? "Follow"
                          : "No follow"
                      }
                    />
                  </div>
                </section>

                <section className="flex flex-wrap gap-3 border-t border-slate-200 pt-6 dark:border-slate-800">
                  {selectedIndustry.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(selectedIndustry)}
                      className="inline-flex h-10 items-center gap-2 rounded-xl bg-blue-600 px-4 text-sm font-semibold text-white hover:bg-blue-700 disabled:opacity-50"
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

      {dialog && selectedIndustry && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 p-4">
          <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl dark:bg-slate-950">
            {dialog === "schedule" ? (
              <>
                <CalendarClock className="h-8 w-8 text-blue-600" />

                <h2 className="mt-4 text-xl font-bold">Schedule publication</h2>

                <p className="mt-2 text-sm text-slate-500">
                  Select a future date and time for {selectedIndustry.name}.
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
                    className="h-10 rounded-xl bg-blue-600 px-4 text-sm font-semibold text-white disabled:opacity-50"
                  >
                    Schedule
                  </button>
                </div>
              </>
            ) : (
              <>
                <Trash2 className="h-8 w-8 text-rose-600" />

                <h2 className="mt-4 text-xl font-bold">Delete industry?</h2>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  This will soft delete {selectedIndustry.name}. It will no
                  longer appear in the normal industries catalogue.
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
                    Delete industry
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

function Metric({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: number;
  icon: typeof Rocket;
}) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{label}</p>
        <Icon className="h-5 w-5 text-blue-500" />
      </div>

      <p className="mt-3 text-3xl font-bold">{value}</p>

      <p className="mt-1 text-xs text-slate-500">Current page</p>
    </article>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wide text-slate-400">
        {label}
      </p>
      <p className="mt-1 break-words text-sm font-semibold text-slate-800 dark:text-slate-200">
        {value}
      </p>
    </div>
  );
}

function ContentCollection({
  title,
  values,
  empty,
}: {
  title: string;
  values: unknown[];
  empty: string;
}) {
  return (
    <Collection title={title} empty={empty}>
      {values.map((value, index) => (
        <div
          key={`${title}-${index}`}
          className="flex gap-3 rounded-xl border border-slate-200 p-3 dark:border-slate-800"
        >
          <CheckCircle2 className="mt-0.5 h-4 w-4 shrink-0 text-emerald-600" />
          <p className="text-sm leading-6 text-slate-600 dark:text-slate-400">
            {displayContentItem(value)}
          </p>
        </div>
      ))}
    </Collection>
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
