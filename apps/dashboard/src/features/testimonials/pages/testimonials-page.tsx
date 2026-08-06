import {
  BadgeCheck,
  CalendarClock,
  ChevronLeft,
  ChevronRight,
  ExternalLink,
  Eye,
  FilterX,
  Globe2,
  LoaderCircle,
  Quote,
  Rocket,
  Search,
  Star,
  Trash2,
  X,
} from "lucide-react";
import { useMemo, useState } from "react";

import {
  formatDateTime,
  statusClasses,
  testimonialSourceLabels,
  testimonialStatusLabels,
} from "../formatters";
import {
  useDeleteTestimonial,
  usePublishTestimonial,
  useScheduleTestimonial,
  useTestimonial,
  useTestimonials,
} from "../hooks";
import {
  testimonialSources,
  testimonialStatuses,
  type Testimonial,
  type TestimonialFilters,
} from "../types";

const defaultFilters: TestimonialFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  source: "",
  rating: "",
  featuredState: "all",
  verifiedState: "all",
  activeState: "all",
  clientId: "",
  projectId: "",
  ordering: "sort_order",
};

type Dialog = "schedule" | "delete" | null;

function errorMessage(error: unknown): string {
  return error instanceof Error
    ? error.message
    : "The operation could not be completed.";
}

export function TestimonialsPage() {
  const [filters, setFilters] = useState(defaultFilters);

  const [selectedId, setSelectedId] = useState("");

  const [dialog, setDialog] = useState<Dialog>(null);

  const [scheduleValue, setScheduleValue] = useState("");

  const [notice, setNotice] = useState("");

  const [operationError, setOperationError] = useState("");

  const testimonialsQuery = useTestimonials(filters);

  const detailQuery = useTestimonial(selectedId, selectedId !== "");

  const publishMutation = usePublishTestimonial();

  const scheduleMutation = useScheduleTestimonial();

  const deleteMutation = useDeleteTestimonial();

  const testimonials = useMemo(
    () => testimonialsQuery.data?.items ?? [],
    [testimonialsQuery.data?.items],
  );

  const pagination = testimonialsQuery.data?.pagination;

  const selectedTestimonial = detailQuery.data;

  const totals = useMemo(
    () => ({
      published: testimonials.filter((item) => item.status === "published")
        .length,
      featured: testimonials.filter((item) => item.is_featured).length,
      verified: testimonials.filter((item) => item.is_verified).length,
      public: testimonials.filter((item) => item.is_publicly_available).length,
    }),
    [testimonials],
  );

  const isMutating =
    publishMutation.isPending ||
    scheduleMutation.isPending ||
    deleteMutation.isPending;

  function updateFilters(changes: Partial<TestimonialFilters>) {
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

  async function publishSelected(testimonial: Testimonial) {
    resetFeedback();

    try {
      await publishMutation.mutateAsync(testimonial.id);

      setNotice(`Testimonial from ${testimonial.author_name} was published.`);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function scheduleSelected() {
    if (!selectedTestimonial || !scheduleValue) {
      return;
    }

    resetFeedback();

    try {
      await scheduleMutation.mutateAsync({
        testimonialId: selectedTestimonial.id,
        payload: {
          scheduled_for: new Date(scheduleValue).toISOString(),
        },
      });

      setNotice(
        `Testimonial from ${selectedTestimonial.author_name} was scheduled.`,
      );
      setDialog(null);
      setScheduleValue("");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function deleteSelected() {
    if (!selectedTestimonial) {
      return;
    }

    resetFeedback();

    try {
      const message = await deleteMutation.mutateAsync(selectedTestimonial.id);

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
            Social proof management
          </p>

          <h1 className="mt-2 text-2xl font-bold">Testimonials</h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Manage client feedback, ratings, sources, client and project
            relationships, verification, featured placement, publishing and
            internal review notes.
          </p>
        </div>

        <button
          type="button"
          disabled
          title="The complete testimonial editor is the next milestone."
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white opacity-60"
        >
          <Quote size={16} />
          Create testimonial
        </button>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Metric label="Published" value={totals.published} icon={Rocket} />
        <Metric label="Featured" value={totals.featured} icon={Star} />
        <Metric label="Verified" value={totals.verified} icon={BadgeCheck} />
        <Metric label="Public" value={totals.public} icon={Globe2} />
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
              placeholder="Search testimonials"
              className="h-10 w-full rounded-xl border border-slate-300 bg-white pl-10 pr-3 text-sm outline-none focus:border-blue-500 dark:border-slate-700 dark:bg-slate-900"
            />
          </label>

          <select
            value={filters.status}
            onChange={(event) =>
              updateFilters({
                status: event.target.value as TestimonialFilters["status"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All statuses</option>

            {testimonialStatuses.map((status) => (
              <option key={status} value={status}>
                {testimonialStatusLabels[status]}
              </option>
            ))}
          </select>

          <select
            value={filters.source}
            onChange={(event) =>
              updateFilters({
                source: event.target.value as TestimonialFilters["source"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All sources</option>

            {testimonialSources.map((source) => (
              <option key={source} value={source}>
                {testimonialSourceLabels[source]}
              </option>
            ))}
          </select>

          <select
            value={filters.rating}
            onChange={(event) =>
              updateFilters({
                rating: event.target.value ? Number(event.target.value) : "",
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">Any rating</option>
            {[5, 4, 3, 2, 1].map((rating) => (
              <option key={rating} value={rating}>
                {rating} stars
              </option>
            ))}
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
            value={filters.featuredState}
            onChange={(event) =>
              updateFilters({
                featuredState: event.target
                  .value as TestimonialFilters["featuredState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any prominence</option>
            <option value="featured">Featured only</option>
            <option value="standard">Non-featured</option>
          </select>

          <select
            value={filters.verifiedState}
            onChange={(event) =>
              updateFilters({
                verifiedState: event.target
                  .value as TestimonialFilters["verifiedState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any verification</option>
            <option value="verified">Verified only</option>
            <option value="unverified">Unverified only</option>
          </select>

          <select
            value={filters.activeState}
            onChange={(event) =>
              updateFilters({
                activeState: event.target
                  .value as TestimonialFilters["activeState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any activity state</option>
            <option value="active">Active only</option>
            <option value="inactive">Inactive only</option>
          </select>

          <input
            value={filters.clientId}
            onChange={(event) =>
              updateFilters({
                clientId: event.target.value,
              })
            }
            placeholder="Client ID"
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          />

          <input
            value={filters.projectId}
            onChange={(event) =>
              updateFilters({
                projectId: event.target.value,
              })
            }
            placeholder="Project ID"
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
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
            <option value="-updated_at">Recently updated</option>
            <option value="-published_at">Recently published</option>
            <option value="-rating">Highest rating</option>
            <option value="rating">Lowest rating</option>
            <option value="author_name">Author A–Z</option>
            <option value="-author_name">Author Z–A</option>
            <option value="company_name">Company A–Z</option>
          </select>
        </div>

        {testimonialsQuery.isLoading ? (
          <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
            <LoaderCircle className="h-5 w-5 animate-spin" />
            Loading testimonials…
          </div>
        ) : testimonialsQuery.isError ? (
          <div className="p-10 text-center">
            <p className="font-semibold text-rose-600">
              Testimonials could not be loaded.
            </p>
            <p className="mt-2 text-sm text-slate-500">
              {errorMessage(testimonialsQuery.error)}
            </p>
          </div>
        ) : testimonials.length === 0 ? (
          <div className="p-10 text-center">
            <Quote className="mx-auto h-10 w-10 text-slate-300" />
            <p className="mt-3 font-semibold text-slate-700 dark:text-slate-300">
              No testimonials match the current filters.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-slate-200 dark:divide-slate-800">
            {testimonials.map((testimonial) => (
              <article
                key={testimonial.id}
                className="grid gap-4 p-5 transition hover:bg-slate-50 dark:hover:bg-slate-900/50 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
              >
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="font-semibold text-slate-950 dark:text-white">
                      {testimonial.author_name}
                    </h2>

                    <span
                      className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${statusClasses(testimonial.status)}`}
                    >
                      {testimonialStatusLabels[testimonial.status]}
                    </span>

                    {testimonial.is_verified && (
                      <span className="inline-flex items-center gap-1 rounded-full bg-blue-100 px-2 py-0.5 text-xs font-semibold text-blue-700 dark:bg-blue-950 dark:text-blue-300">
                        <BadgeCheck className="h-3.5 w-3.5" />
                        Verified
                      </span>
                    )}

                    {testimonial.is_featured && (
                      <span className="rounded-full bg-violet-100 px-2 py-0.5 text-xs font-semibold text-violet-700 dark:bg-violet-950 dark:text-violet-300">
                        Featured
                      </span>
                    )}
                  </div>

                  <p className="mt-1 text-sm text-slate-500">
                    {testimonial.author_position || "No position"}
                    {testimonial.company_name
                      ? ` · ${testimonial.company_name}`
                      : ""}
                  </p>

                  <p className="mt-3 line-clamp-3 text-sm leading-6 text-slate-600 dark:text-slate-400">
                    {testimonial.short_content || testimonial.content}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-xs text-slate-500">
                    <span>
                      {"★".repeat(testimonial.rating)}
                      {"☆".repeat(5 - testimonial.rating)}
                    </span>
                    <span>{testimonialSourceLabels[testimonial.source]}</span>
                    <span>{testimonial.client_name || "No linked client"}</span>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <p className="font-semibold text-slate-800 dark:text-slate-200">
                    {testimonial.project_title || "No linked project"}
                  </p>

                  <p className="text-xs text-slate-500">
                    Updated {formatDateTime(testimonial.updated_at)}
                  </p>

                  <p className="text-xs text-slate-500">
                    {testimonial.is_publicly_available
                      ? "Publicly available"
                      : "Not publicly available"}
                  </p>
                </div>

                <div className="flex flex-wrap items-start gap-2 lg:justify-end">
                  <button
                    type="button"
                    onClick={() => {
                      resetFeedback();
                      setSelectedId(testimonial.id);
                    }}
                    className="inline-flex h-9 items-center gap-2 rounded-lg border border-slate-300 px-3 text-sm font-semibold hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-800"
                  >
                    <Eye className="h-4 w-4" />
                    Inspect
                  </button>

                  {testimonial.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(testimonial)}
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
            {pagination?.total_items ?? 0} testimonials
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
                  Testimonial record
                </p>
                <h2 className="mt-1 text-xl font-bold">
                  {selectedTestimonial?.author_name || "Loading testimonial"}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => {
                  setSelectedId("");
                  setDialog(null);
                }}
                className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800"
                aria-label="Close testimonial details"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {detailQuery.isLoading ? (
              <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
                <LoaderCircle className="h-5 w-5 animate-spin" />
                Loading testimonial…
              </div>
            ) : detailQuery.isError || !selectedTestimonial ? (
              <div className="p-6 text-sm text-rose-600">
                Testimonial details could not be loaded.
              </div>
            ) : (
              <div className="space-y-6 p-6">
                <section className="rounded-2xl border border-slate-200 p-5 dark:border-slate-800">
                  <Quote className="h-6 w-6 text-blue-500" />

                  <p className="mt-4 text-base leading-8 text-slate-700 dark:text-slate-300">
                    “{selectedTestimonial.content}”
                  </p>

                  <p className="mt-4 font-semibold">
                    {selectedTestimonial.author_name}
                  </p>

                  <p className="text-sm text-slate-500">
                    {selectedTestimonial.author_position || "No position"}
                    {selectedTestimonial.company_name
                      ? ` · ${selectedTestimonial.company_name}`
                      : ""}
                  </p>
                </section>

                <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
                  <Detail
                    label="Status"
                    value={testimonialStatusLabels[selectedTestimonial.status]}
                  />

                  <Detail
                    label="Rating"
                    value={`${selectedTestimonial.rating} of 5`}
                  />

                  <Detail
                    label="Source"
                    value={testimonialSourceLabels[selectedTestimonial.source]}
                  />

                  <Detail
                    label="Verification"
                    value={
                      selectedTestimonial.is_verified
                        ? "Verified"
                        : "Unverified"
                    }
                  />

                  <Detail
                    label="Client"
                    value={selectedTestimonial.client_name || "Not linked"}
                  />

                  <Detail
                    label="Project"
                    value={selectedTestimonial.project_title || "Not linked"}
                  />

                  <Detail
                    label="Published"
                    value={formatDateTime(selectedTestimonial.published_at)}
                  />

                  <Detail
                    label="Scheduled"
                    value={formatDateTime(selectedTestimonial.scheduled_for)}
                  />

                  <Detail
                    label="Featured"
                    value={selectedTestimonial.is_featured ? "Yes" : "No"}
                  />

                  <Detail
                    label="Public"
                    value={
                      selectedTestimonial.is_publicly_available
                        ? "Available"
                        : "Unavailable"
                    }
                  />
                </section>

                {selectedTestimonial.source_url && (
                  <a
                    href={selectedTestimonial.source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 text-sm font-semibold text-blue-600 hover:underline"
                  >
                    <ExternalLink className="h-4 w-4" />
                    Open original source
                  </a>
                )}

                <section>
                  <h3 className="font-semibold">Short content</h3>

                  <p className="mt-2 text-sm leading-6 text-slate-500">
                    {selectedTestimonial.short_content ||
                      "No shortened version supplied."}
                  </p>
                </section>

                <section className="rounded-2xl border border-slate-200 p-5 dark:border-slate-800">
                  <h3 className="font-semibold">Internal notes</h3>

                  <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-500">
                    {selectedTestimonial.internal_notes || "No internal notes."}
                  </p>
                </section>

                <section className="flex flex-wrap gap-3 border-t border-slate-200 pt-6 dark:border-slate-800">
                  {selectedTestimonial.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(selectedTestimonial)}
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

      {dialog && selectedTestimonial && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 p-4">
          <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl dark:bg-slate-950">
            {dialog === "schedule" ? (
              <>
                <CalendarClock className="h-8 w-8 text-blue-600" />

                <h2 className="mt-4 text-xl font-bold">Schedule testimonial</h2>

                <p className="mt-2 text-sm text-slate-500">
                  Select a future date and time for the testimonial from{" "}
                  {selectedTestimonial.author_name}.
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

                <h2 className="mt-4 text-xl font-bold">Delete testimonial?</h2>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  This will soft delete the testimonial from{" "}
                  {selectedTestimonial.author_name}. It will no longer appear in
                  the standard workspace.
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
                    Delete testimonial
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
