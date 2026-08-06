import {
  BarChart3,
  BriefcaseBusiness,
  CalendarClock,
  ChevronLeft,
  ChevronRight,
  ExternalLink,
  Eye,
  FileText,
  FilterX,
  Globe2,
  ImageIcon,
  LoaderCircle,
  MapPin,
  Quote,
  Rocket,
  Search,
  Star,
  Trash2,
  X,
} from "lucide-react";
import { useMemo, useState, type ReactNode } from "react";

import {
  caseStudyStatusLabels,
  displayStructuredContent,
  formatDate,
  formatDateTime,
  formatNumber,
  statusClasses,
} from "../formatters";
import {
  useCaseStudies,
  useCaseStudy,
  useDeleteCaseStudy,
  usePublishCaseStudy,
  useScheduleCaseStudy,
} from "../hooks";
import {
  caseStudyStatuses,
  type CaseStudy,
  type CaseStudyFilters,
} from "../types";

const defaultFilters: CaseStudyFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  clientId: "",
  projectId: "",
  industryId: "",
  serviceId: "",
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

export function CaseStudiesPage() {
  const [filters, setFilters] = useState(defaultFilters);

  const [selectedId, setSelectedId] = useState("");

  const [dialog, setDialog] = useState<Dialog>(null);

  const [scheduleValue, setScheduleValue] = useState("");

  const [notice, setNotice] = useState("");

  const [operationError, setOperationError] = useState("");

  const caseStudiesQuery = useCaseStudies(filters);

  const detailQuery = useCaseStudy(selectedId, selectedId !== "");

  const publishMutation = usePublishCaseStudy();

  const scheduleMutation = useScheduleCaseStudy();

  const deleteMutation = useDeleteCaseStudy();

  const caseStudies = useMemo(
    () => caseStudiesQuery.data?.items ?? [],
    [caseStudiesQuery.data?.items],
  );

  const pagination = caseStudiesQuery.data?.pagination;

  const selectedCaseStudy = detailQuery.data;

  const totals = useMemo(
    () => ({
      published: caseStudies.filter((item) => item.status === "published")
        .length,
      featured: caseStudies.filter((item) => item.is_featured).length,
      public: caseStudies.filter((item) => item.is_publicly_available).length,
      views: caseStudies.reduce((total, item) => total + item.view_count, 0),
    }),
    [caseStudies],
  );

  const isMutating =
    publishMutation.isPending ||
    scheduleMutation.isPending ||
    deleteMutation.isPending;

  function updateFilters(changes: Partial<CaseStudyFilters>) {
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

  async function publishSelected(item: CaseStudy) {
    resetFeedback();

    try {
      await publishMutation.mutateAsync(item.id);

      setNotice(`${item.title} was published.`);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function scheduleSelected() {
    if (!selectedCaseStudy || !scheduleValue) {
      return;
    }

    resetFeedback();

    try {
      await scheduleMutation.mutateAsync({
        caseStudyId: selectedCaseStudy.id,
        payload: {
          scheduled_for: new Date(scheduleValue).toISOString(),
        },
      });

      setNotice(`${selectedCaseStudy.title} was scheduled.`);
      setDialog(null);
      setScheduleValue("");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function deleteSelected() {
    if (!selectedCaseStudy) {
      return;
    }

    resetFeedback();

    try {
      const message = await deleteMutation.mutateAsync(selectedCaseStudy.id);

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
            Client success portfolio
          </p>

          <h1 className="mt-2 text-2xl font-bold">Case Studies</h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500">
            Manage client outcomes, projects, industries, services,
            technologies, media, metrics, milestones, testimonials, SEO,
            revisions and publishing.
          </p>
        </div>

        <button
          type="button"
          disabled
          title="The complete case-study editor is the next milestone."
          className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white opacity-60"
        >
          <FileText size={16} />
          Create case study
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
              placeholder="Search case studies"
              className="h-10 w-full rounded-xl border border-slate-300 bg-white pl-10 pr-3 text-sm outline-none focus:border-blue-500 dark:border-slate-700 dark:bg-slate-900"
            />
          </label>

          <select
            value={filters.status}
            onChange={(event) =>
              updateFilters({
                status: event.target.value as CaseStudyFilters["status"],
              })
            }
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          >
            <option value="">All statuses</option>

            {caseStudyStatuses.map((status) => (
              <option key={status} value={status}>
                {caseStudyStatusLabels[status]}
              </option>
            ))}
          </select>

          <select
            value={filters.featuredState}
            onChange={(event) =>
              updateFilters({
                featuredState: event.target
                  .value as CaseStudyFilters["featuredState"],
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
                  .value as CaseStudyFilters["activeState"],
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

          <input
            value={filters.industryId}
            onChange={(event) =>
              updateFilters({
                industryId: event.target.value,
              })
            }
            placeholder="Industry ID"
            className="h-10 rounded-xl border border-slate-300 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-900"
          />

          <input
            value={filters.serviceId}
            onChange={(event) =>
              updateFilters({
                serviceId: event.target.value,
              })
            }
            placeholder="Service ID"
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
            <option value="-view_count">Most viewed</option>
            <option value="-project_completion_date">Recently completed</option>
            <option value="title">Title A–Z</option>
            <option value="-title">Title Z–A</option>
          </select>
        </div>

        {caseStudiesQuery.isLoading ? (
          <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
            <LoaderCircle className="h-5 w-5 animate-spin" />
            Loading case studies…
          </div>
        ) : caseStudiesQuery.isError ? (
          <div className="p-10 text-center">
            <p className="font-semibold text-rose-600">
              Case studies could not be loaded.
            </p>

            <p className="mt-2 text-sm text-slate-500">
              {errorMessage(caseStudiesQuery.error)}
            </p>
          </div>
        ) : caseStudies.length === 0 ? (
          <div className="p-10 text-center">
            <BriefcaseBusiness className="mx-auto h-10 w-10 text-slate-300" />

            <p className="mt-3 font-semibold text-slate-700 dark:text-slate-300">
              No case studies match the current filters.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-slate-200 dark:divide-slate-800">
            {caseStudies.map((item) => (
              <article
                key={item.id}
                className="grid gap-4 p-5 transition hover:bg-slate-50 dark:hover:bg-slate-900/50 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
              >
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h2 className="font-semibold text-slate-950 dark:text-white">
                      {item.title}
                    </h2>

                    <span
                      className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${statusClasses(item.status)}`}
                    >
                      {caseStudyStatusLabels[item.status]}
                    </span>

                    {item.is_featured && (
                      <span className="rounded-full bg-violet-100 px-2 py-0.5 text-xs font-semibold text-violet-700 dark:bg-violet-950 dark:text-violet-300">
                        Featured
                      </span>
                    )}
                  </div>

                  <p className="mt-1 text-sm text-slate-500">/{item.slug}</p>

                  <p className="mt-2 line-clamp-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
                    {item.short_description || "No summary supplied."}
                  </p>

                  <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-xs text-slate-500">
                    <span>
                      {item.linked_client_name ||
                        item.client_name ||
                        "No client"}
                    </span>

                    <span>{item.industry_name || "No industry"}</span>

                    <span>{item.services.length} services</span>

                    <span>{item.metrics.length} metrics</span>

                    <span>Revision {item.current_revision_number}</span>
                  </div>
                </div>

                <div className="space-y-2 text-sm">
                  <p className="font-semibold text-slate-800 dark:text-slate-200">
                    {item.project_name || "No linked project"}
                  </p>

                  <p className="flex items-center gap-1 text-xs text-slate-500">
                    <MapPin className="h-3.5 w-3.5" />
                    {item.location || "No location"}
                  </p>

                  <p className="text-xs text-slate-500">
                    {item.project_duration || "Duration not supplied"}
                  </p>

                  <p className="text-xs text-slate-500">
                    {formatNumber(item.view_count)} views
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
            {pagination?.total_items ?? 0} case studies
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
                  Case study record
                </p>

                <h2 className="mt-1 text-xl font-bold">
                  {selectedCaseStudy?.title || "Loading case study"}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => {
                  setSelectedId("");
                  setDialog(null);
                }}
                className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800"
                aria-label="Close case-study details"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {detailQuery.isLoading ? (
              <div className="flex min-h-72 items-center justify-center gap-3 text-sm text-slate-500">
                <LoaderCircle className="h-5 w-5 animate-spin" />
                Loading case-study details…
              </div>
            ) : detailQuery.isError || !selectedCaseStudy ? (
              <div className="p-6 text-sm text-rose-600">
                Case-study details could not be loaded.
              </div>
            ) : (
              <div className="space-y-6 p-6">
                <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
                  <Detail
                    label="Status"
                    value={caseStudyStatusLabels[selectedCaseStudy.status]}
                  />

                  <Detail
                    label="Client"
                    value={
                      selectedCaseStudy.linked_client_name ||
                      selectedCaseStudy.client_name ||
                      "No client"
                    }
                  />

                  <Detail
                    label="Project"
                    value={selectedCaseStudy.project_name || "No project"}
                  />

                  <Detail
                    label="Industry"
                    value={selectedCaseStudy.industry_name || "No industry"}
                  />

                  <Detail
                    label="Location"
                    value={selectedCaseStudy.location || "Not supplied"}
                  />

                  <Detail
                    label="Duration"
                    value={selectedCaseStudy.project_duration || "Not supplied"}
                  />

                  <Detail
                    label="Started"
                    value={formatDate(selectedCaseStudy.project_start_date)}
                  />

                  <Detail
                    label="Completed"
                    value={formatDate(
                      selectedCaseStudy.project_completion_date,
                    )}
                  />

                  <Detail
                    label="Revision"
                    value={String(selectedCaseStudy.current_revision_number)}
                  />

                  <Detail
                    label="Views"
                    value={formatNumber(selectedCaseStudy.view_count)}
                  />

                  <Detail
                    label="Published"
                    value={formatDateTime(selectedCaseStudy.published_at)}
                  />

                  <Detail
                    label="Public"
                    value={
                      selectedCaseStudy.is_publicly_available
                        ? "Available"
                        : "Unavailable"
                    }
                  />
                </section>

                {selectedCaseStudy.website_url && (
                  <a
                    href={selectedCaseStudy.website_url}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-2 text-sm font-semibold text-blue-600 hover:underline"
                  >
                    <ExternalLink className="h-4 w-4" />
                    Visit project website
                  </a>
                )}

                <StructuredSection
                  title="Overview"
                  value={selectedCaseStudy.overview}
                />

                <StructuredSection
                  title="Challenge"
                  value={selectedCaseStudy.challenge}
                />

                <StructuredSection
                  title="Solution"
                  value={selectedCaseStudy.solution}
                />

                <StructuredSection
                  title="Implementation"
                  value={selectedCaseStudy.implementation}
                />

                <StructuredSection
                  title="Results"
                  value={selectedCaseStudy.results}
                />

                <Collection title="Services" empty="No linked services.">
                  {selectedCaseStudy.services.map((service) => (
                    <div
                      key={service.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <p className="text-sm font-semibold">
                        {service.service_title}
                      </p>

                      <p className="mt-1 text-xs leading-5 text-slate-500">
                        {service.description ||
                          "No case-study service description."}
                      </p>
                    </div>
                  ))}
                </Collection>

                <Collection title="Technologies" empty="No technologies.">
                  {selectedCaseStudy.technologies.map((technology) => (
                    <div
                      key={technology.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <p className="text-sm font-semibold">{technology.name}</p>

                      <p className="mt-1 text-xs leading-5 text-slate-500">
                        {technology.description || "No technology description."}
                      </p>
                    </div>
                  ))}
                </Collection>

                <Collection title="Outcome metrics" empty="No outcome metrics.">
                  {selectedCaseStudy.metrics.map((metric) => (
                    <div
                      key={metric.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <div className="flex items-center gap-3">
                        <BarChart3 className="h-4 w-4 text-blue-500" />

                        <div>
                          <p className="text-sm font-semibold">
                            {metric.label}: {metric.value}
                          </p>

                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            {metric.description || "No metric description."}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </Collection>

                <Collection title="Milestones" empty="No milestones.">
                  {selectedCaseStudy.milestones.map((milestone) => (
                    <div
                      key={milestone.id}
                      className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <p className="text-sm font-semibold">{milestone.title}</p>

                      <p className="mt-1 text-xs text-slate-400">
                        {formatDate(milestone.milestone_date)}
                      </p>

                      <p className="mt-1 text-xs leading-5 text-slate-500">
                        {milestone.description || "No milestone description."}
                      </p>
                    </div>
                  ))}
                </Collection>

                <Collection title="Media" empty="No case-study media.">
                  {selectedCaseStudy.media_items.map((media) => (
                    <div
                      key={media.id}
                      className="flex gap-3 rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                    >
                      <ImageIcon className="mt-0.5 h-4 w-4 shrink-0 text-blue-500" />

                      <div>
                        <p className="text-sm font-semibold">
                          {media.title || media.asset_title}
                        </p>

                        <p className="mt-1 text-xs capitalize text-slate-400">
                          {media.media_role}
                        </p>

                        {media.caption && (
                          <p className="mt-1 text-xs leading-5 text-slate-500">
                            {media.caption}
                          </p>
                        )}
                      </div>
                    </div>
                  ))}
                </Collection>

                {selectedCaseStudy.testimonial && (
                  <section className="rounded-2xl border border-slate-200 p-5 dark:border-slate-800">
                    <Quote className="h-5 w-5 text-blue-500" />

                    <p className="mt-3 text-sm leading-7 text-slate-600 dark:text-slate-400">
                      “{selectedCaseStudy.testimonial}”
                    </p>

                    <p className="mt-3 text-sm font-semibold">
                      {selectedCaseStudy.testimonial_author}
                    </p>

                    <p className="text-xs text-slate-500">
                      {selectedCaseStudy.testimonial_position}
                    </p>
                  </section>
                )}

                <section className="rounded-2xl border border-slate-200 p-5 dark:border-slate-800">
                  <h3 className="font-semibold">SEO</h3>

                  <div className="mt-4 grid gap-4 sm:grid-cols-2">
                    <Detail
                      label="Meta title"
                      value={
                        selectedCaseStudy.seo?.meta_title || "Not supplied"
                      }
                    />

                    <Detail
                      label="Canonical"
                      value={
                        selectedCaseStudy.seo?.canonical_url || "Not supplied"
                      }
                    />

                    <Detail
                      label="Indexing"
                      value={
                        selectedCaseStudy.seo?.robots_index
                          ? "Index"
                          : "No index"
                      }
                    />

                    <Detail
                      label="Following"
                      value={
                        selectedCaseStudy.seo?.robots_follow
                          ? "Follow"
                          : "No follow"
                      }
                    />
                  </div>
                </section>

                <section className="flex flex-wrap gap-3 border-t border-slate-200 pt-6 dark:border-slate-800">
                  {selectedCaseStudy.status !== "published" && (
                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => void publishSelected(selectedCaseStudy)}
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

      {dialog && selectedCaseStudy && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 p-4">
          <div className="w-full max-w-md rounded-3xl bg-white p-6 shadow-2xl dark:bg-slate-950">
            {dialog === "schedule" ? (
              <>
                <CalendarClock className="h-8 w-8 text-blue-600" />

                <h2 className="mt-4 text-xl font-bold">Schedule publication</h2>

                <p className="mt-2 text-sm text-slate-500">
                  Select a future date and time for {selectedCaseStudy.title}.
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

                <h2 className="mt-4 text-xl font-bold">Delete case study?</h2>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  This will soft delete {selectedCaseStudy.title}. It will no
                  longer appear in the standard Case Studies workspace.
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
                    Delete case study
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

function StructuredSection({
  title,
  value,
}: {
  title: string;
  value: Record<string, unknown>;
}) {
  return (
    <section>
      <h3 className="font-semibold">{title}</h3>

      <p className="mt-2 text-sm leading-6 text-slate-500">
        {displayStructuredContent(value)}
      </p>
    </section>
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
