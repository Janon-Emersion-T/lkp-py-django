import {
  BookOpenText,
  CalendarClock,
  ChevronLeft,
  ChevronRight,
  Clock3,
  Eye,
  FileText,
  FilterX,
  Globe2,
  Link2,
  LoaderCircle,
  Rocket,
  Search,
  Star,
  Trash2,
  X,
} from "lucide-react";
import { useMemo, useState, type ReactNode } from "react";

import {
  formatDateTime,
  formatNumber,
  insightStatusLabels,
  statusClasses,
} from "../formatters";
import {
  useDeleteInsight,
  useInsight,
  useInsightCategories,
  useInsights,
  useInsightTags,
  usePublishInsight,
  useScheduleInsight,
} from "../hooks";
import {
  insightStatuses,
  type InsightArticle,
  type InsightFilters,
} from "../types";

const defaultFilters: InsightFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  categoryId: "",
  tagId: "",
  featuredState: "all",
  activeState: "all",
  ordering: "-created_at",
};

type Dialog = "schedule" | "delete" | null;

function errorMessage(error: unknown): string {
  return error instanceof Error
    ? error.message
    : "The operation could not be completed.";
}

export function InsightsPage() {
  const [filters, setFilters] = useState(defaultFilters);

  const [selectedId, setSelectedId] = useState("");

  const [dialog, setDialog] = useState<Dialog>(null);

  const [scheduleValue, setScheduleValue] = useState("");

  const [notice, setNotice] = useState("");

  const [operationError, setOperationError] = useState("");

  const insightsQuery = useInsights(filters);

  const categoriesQuery = useInsightCategories();

  const tagsQuery = useInsightTags();

  const detailQuery = useInsight(selectedId, selectedId !== "");

  const publishMutation = usePublishInsight();

  const scheduleMutation = useScheduleInsight();

  const deleteMutation = useDeleteInsight();

  const articles = useMemo(
    () => insightsQuery.data?.items ?? [],
    [insightsQuery.data?.items],
  );

  const categories = categoriesQuery.data ?? [];

  const tags = tagsQuery.data ?? [];

  const pagination = insightsQuery.data?.pagination;

  const selectedArticle = detailQuery.data;

  const totals = useMemo(
    () => ({
      published: articles.filter((article) => article.status === "published")
        .length,
      featured: articles.filter((article) => article.is_featured).length,
      public: articles.filter((article) => article.is_publicly_available)
        .length,
      views: articles.reduce((total, article) => total + article.view_count, 0),
    }),
    [articles],
  );

  const isMutating =
    publishMutation.isPending ||
    scheduleMutation.isPending ||
    deleteMutation.isPending;

  function updateFilters(changes: Partial<InsightFilters>) {
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

  async function publishSelected(article: InsightArticle) {
    resetFeedback();

    try {
      await publishMutation.mutateAsync(article.id);

      setNotice(`${article.title} was published.`);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function scheduleSelected() {
    if (!selectedArticle || !scheduleValue) {
      return;
    }

    resetFeedback();

    try {
      await scheduleMutation.mutateAsync({
        articleId: selectedArticle.id,
        payload: {
          scheduled_for: new Date(scheduleValue).toISOString(),
        },
      });

      setNotice(`${selectedArticle.title} was scheduled.`);
      setDialog(null);
      setScheduleValue("");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function deleteSelected() {
    if (!selectedArticle) {
      return;
    }

    resetFeedback();

    try {
      const message = await deleteMutation.mutateAsync(selectedArticle.id);

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
            Editorial publishing
          </p>

          <h1 className="mt-2 text-2xl font-bold">Insights</h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Manage LKP articles, categories, tags, authorship, reading metrics,
            related content, internal links, publishing events, revisions and
            SEO.
          </p>
        </div>

        <button
          type="button"
          disabled
          title="The complete article editor is the next milestone."
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white opacity-60"
        >
          <FileText size={16} />
          Create article
        </button>
      </header>

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Metric label="Published" value={totals.published} icon={Rocket} />
        <Metric label="Featured" value={totals.featured} icon={Star} />
        <Metric label="Public" value={totals.public} icon={Globe2} />
        <Metric label="Views" value={totals.views} icon={Eye} />
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
              placeholder="Search insights"
              className="h-10 w-full rounded-xl border border-slate-300 bg-white pl-10 pr-3 text-sm outline-none focus:border-blue-500 dark:border-slate-700 dark:bg-slate-900"
            />
          </label>

          <select
            value={filters.status}
            onChange={(event) =>
              updateFilters({
                status: event.target.value as InsightFilters["status"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All statuses</option>

            {insightStatuses.map((status) => (
              <option key={status} value={status}>
                {insightStatusLabels[status]}
              </option>
            ))}
          </select>

          <select
            value={filters.categoryId}
            onChange={(event) =>
              updateFilters({
                categoryId: event.target.value,
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All categories</option>

            {categories.map((category) => (
              <option key={category.id} value={category.id}>
                {category.name}
              </option>
            ))}
          </select>

          <select
            value={filters.tagId}
            onChange={(event) =>
              updateFilters({
                tagId: event.target.value,
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All tags</option>

            {tags.map((tag) => (
              <option key={tag.id} value={tag.id}>
                {tag.name}
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
                  .value as InsightFilters["featuredState"],
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
                  .value as InsightFilters["activeState"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="all">Any activity state</option>
            <option value="active">Active only</option>
            <option value="inactive">Inactive only</option>
          </select>

          <select
            value={filters.ordering}
            onChange={(event) =>
              updateFilters({
                ordering: event.target.value,
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900 xl:col-span-2"
          >
            <option value="-created_at">Recently created</option>
            <option value="-updated_at">Recently updated</option>
            <option value="-published_at">Recently published</option>
            <option value="-view_count">Most viewed</option>
            <option value="title">Title A–Z</option>
            <option value="-title">Title Z–A</option>
          </select>
        </div>

        {insightsQuery.isLoading ? (
          <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
            <LoaderCircle className="h-5 w-5 animate-spin" />
            Loading insights…
          </div>
        ) : insightsQuery.isError ? (
          <div className="p-10 text-center">
            <p className="font-semibold text-rose-600">
              Insights could not be loaded.
            </p>
            <p className="mt-2 text-sm text-slate-500">
              {errorMessage(insightsQuery.error)}
            </p>
          </div>
        ) : articles.length === 0 ? (
          <div className="p-10 text-center">
            <BookOpenText className="mx-auto h-10 w-10 text-slate-300" />
            <p className="mt-3 font-semibold text-slate-700 dark:text-slate-300">
              No insights match the current filters.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-slate-200 dark:divide-slate-800">
            {articles.map((article) => (
              <article
                key={article.id}
                className="grid gap-4 p-5 transition hover:bg-slate-50 dark:hover:bg-slate-900/50 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
              >
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="font-semibold text-slate-950 dark:text-white">
                      {article.title}
                    </h2>

                    <span
                      className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${statusClasses(article.status)}`}
                    >
                      {insightStatusLabels[article.status]}
                    </span>

                    {article.is_featured && (
                      <span className="rounded-full bg-violet-100 px-2 py-0.5 text-xs font-semibold text-violet-700 dark:bg-violet-950 dark:text-violet-300">
                        Featured
                      </span>
                    )}
                  </div>

                  <p className="mt-1 text-sm text-slate-500">/{article.slug}</p>

                  <p className="mt-2 line-clamp-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
                    {article.excerpt || "No excerpt supplied."}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-xs text-slate-500">
                    <span>{article.category_name || "Uncategorised"}</span>
                    <span>{article.tags.length} tags</span>
                    <span>{article.word_count} words</span>
                    <span>Revision {article.current_revision_number}</span>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <p className="font-semibold text-slate-800 dark:text-slate-200">
                    {article.author_email || "No author"}
                  </p>
                  <p className="text-xs text-slate-500">
                    {article.reading_time_minutes} minute read
                  </p>
                  <p className="text-xs text-slate-500">
                    {formatNumber(article.view_count)} views
                  </p>
                  <p className="text-xs text-slate-500">
                    Updated {formatDateTime(article.updated_at)}
                  </p>
                </div>

                <div className="flex flex-wrap items-start gap-2 lg:justify-end">
                  <button
                    type="button"
                    onClick={() => {
                      resetFeedback();
                      setSelectedId(article.id);
                    }}
                    className="inline-flex h-9 items-center gap-2 rounded-lg border border-slate-300 px-3 text-sm font-semibold hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-800"
                  >
                    <Eye className="h-4 w-4" />
                    Inspect
                  </button>

                  {article.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(article)}
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
            {pagination?.total_items ?? 0} articles
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
                  Insight article
                </p>
                <h2 className="mt-1 text-xl font-bold">
                  {selectedArticle?.title || "Loading article"}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => {
                  setSelectedId("");
                  setDialog(null);
                }}
                className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800"
                aria-label="Close insight details"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {detailQuery.isLoading ? (
              <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
                <LoaderCircle className="h-5 w-5 animate-spin" />
                Loading article details…
              </div>
            ) : detailQuery.isError || !selectedArticle ? (
              <div className="p-6 text-sm text-rose-600">
                Article details could not be loaded.
              </div>
            ) : (
              <div className="space-y-6 p-6">
                <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
                  <Detail
                    label="Status"
                    value={insightStatusLabels[selectedArticle.status]}
                  />
                  <Detail
                    label="Category"
                    value={selectedArticle.category_name || "Uncategorised"}
                  />
                  <Detail
                    label="Author"
                    value={selectedArticle.author_email || "No author"}
                  />
                  <Detail
                    label="Reading time"
                    value={`${selectedArticle.reading_time_minutes} minutes`}
                  />
                  <Detail
                    label="Word count"
                    value={formatNumber(selectedArticle.word_count)}
                  />
                  <Detail
                    label="Views"
                    value={formatNumber(selectedArticle.view_count)}
                  />
                  <Detail
                    label="Revision"
                    value={String(selectedArticle.current_revision_number)}
                  />
                  <Detail
                    label="Public"
                    value={
                      selectedArticle.is_publicly_available
                        ? "Available"
                        : "Unavailable"
                    }
                  />
                </section>

                <section>
                  <h3 className="font-semibold">Excerpt</h3>
                  <p className="mt-2 text-sm leading-6 text-slate-500">
                    {selectedArticle.excerpt || "No excerpt supplied."}
                  </p>
                </section>

                <Collection title="Tags" empty="No tags assigned.">
                  <div className="flex flex-wrap gap-2">
                    {selectedArticle.tags.map((tag) => (
                      <span
                        key={tag.id}
                        className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700 dark:bg-slate-800 dark:text-slate-300"
                      >
                        {tag.name}
                      </span>
                    ))}
                  </div>
                </Collection>

                <Collection
                  title="Related articles"
                  empty="No related articles."
                >
                  {selectedArticle.related_articles.map((article) => (
                    <div
                      key={article.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <p className="text-sm font-semibold">{article.title}</p>
                      <p className="mt-1 text-xs text-slate-500">
                        /{article.slug}
                      </p>
                    </div>
                  ))}
                </Collection>

                <Collection title="Internal links" empty="No internal links.">
                  {selectedArticle.internal_links.map((link) => (
                    <div
                      key={link.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <div className="flex items-start gap-3">
                        <Link2 className="mt-0.5 h-4 w-4 shrink-0 text-blue-500" />
                        <div>
                          <p className="text-sm font-semibold">
                            {link.target_article_title}
                          </p>
                          <p className="mt-1 text-xs text-slate-500">
                            Anchor: {link.anchor_text}
                          </p>
                          {link.context && (
                            <p className="mt-1 text-xs leading-5 text-slate-500">
                              {link.context}
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </Collection>

                <section className="rounded-2xl border border-slate-200 p-5 dark:border-slate-800">
                  <h3 className="font-semibold">SEO</h3>

                  <div className="mt-4 grid gap-4 sm:grid-cols-2">
                    <Detail
                      label="Meta title"
                      value={selectedArticle.seo?.meta_title || "Not supplied"}
                    />
                    <Detail
                      label="Canonical"
                      value={
                        selectedArticle.seo?.canonical_url || "Not supplied"
                      }
                    />
                    <Detail
                      label="Indexing"
                      value={
                        selectedArticle.seo?.robots_index ? "Index" : "No index"
                      }
                    />
                    <Detail
                      label="Following"
                      value={
                        selectedArticle.seo?.robots_follow
                          ? "Follow"
                          : "No follow"
                      }
                    />
                  </div>
                </section>

                <Collection
                  title="Publishing timeline"
                  empty="No publishing events."
                >
                  {selectedArticle.publishing_events.map((event) => (
                    <div
                      key={event.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <div className="flex items-start gap-3">
                        <Clock3 className="mt-0.5 h-4 w-4 shrink-0 text-blue-500" />
                        <div>
                          <p className="text-sm font-semibold capitalize">
                            {event.event_type.replaceAll("_", " ")}
                          </p>
                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            {event.description}
                          </p>
                          <p className="mt-1 text-xs text-slate-400">
                            {formatDateTime(event.created_at)}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </Collection>

                <section className="flex flex-wrap gap-3 border-t border-slate-200 pt-6 dark:border-slate-800">
                  {selectedArticle.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(selectedArticle)}
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

      {dialog && selectedArticle && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 p-4">
          <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl dark:bg-slate-950">
            {dialog === "schedule" ? (
              <>
                <CalendarClock className="h-8 w-8 text-blue-600" />

                <h2 className="mt-4 text-xl font-bold">Schedule publication</h2>

                <p className="mt-2 text-sm text-slate-500">
                  Select a future date and time for {selectedArticle.title}.
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

                <h2 className="mt-4 text-xl font-bold">Delete article?</h2>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  This will soft delete {selectedArticle.title}. It will no
                  longer appear in the normal Insights list.
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
                    Delete article
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

      <p className="mt-3 text-3xl font-bold">{formatNumber(value)}</p>

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
