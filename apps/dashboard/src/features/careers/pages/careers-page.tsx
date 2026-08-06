import {
  Archive,
  BadgeCheck,
  BriefcaseBusiness,
  CalendarClock,
  CheckCircle2,
  CircleOff,
  Eye,
  FileText,
  FilterX,
  LoaderCircle,
  MessageSquarePlus,
  Search,
  Send,
  Star,
  UserCheck,
  Users,
  Video,
  X,
} from "lucide-react";
import { useMemo, useState } from "react";

import {
  applicationSourceLabels,
  applicationStatusLabels,
  formatDateTime,
  formatMoney,
  interviewStatusLabels,
  interviewTypeLabels,
  listingStatusLabels,
  statusClasses,
} from "../formatters";
import {
  useAddApplicationNote,
  useArchiveListing,
  useCareerReferenceData,
  useCareersDashboard,
  useCloseListing,
  useInterviews,
  useJobApplication,
  useJobApplications,
  useJobListings,
  usePublishListing,
  useReviewApplication,
  useScheduleListing,
  useUpdateApplicationStatus,
} from "../hooks";
import {
  applicationSources,
  applicationStatuses,
  interviewStatuses,
  interviewTypes,
  jobListingStatuses,
  type ApplicationFilters,
  type ApplicationStatus,
  type InterviewFilters,
  type JobListing,
  type ListingFilters,
} from "../types";

type CareersTab = "overview" | "listings" | "applications" | "interviews";

const defaultListingFilters: ListingFilters = {
  search: "",
  status: "",
  departmentId: "",
  employmentTypeId: "",
  featuredState: "all",
  activeState: "all",
  ordering: "sort_order",
};

const defaultApplicationFilters: ApplicationFilters = {
  search: "",
  listingId: "",
  status: "",
  source: "",
  assignedToId: "",
  ordering: "-submitted_at",
};

const defaultInterviewFilters: InterviewFilters = {
  applicationId: "",
  status: "",
  interviewType: "",
  organizerId: "",
  ordering: "scheduled_start",
};

function errorMessage(error: unknown) {
  return error instanceof Error
    ? error.message
    : "The operation could not be completed.";
}

export function CareersPage() {
  const [tab, setTab] = useState<CareersTab>("overview");

  const [listingFilters, setListingFilters] = useState(defaultListingFilters);

  const [applicationFilters, setApplicationFilters] = useState(
    defaultApplicationFilters,
  );

  const [interviewFilters, setInterviewFilters] = useState(
    defaultInterviewFilters,
  );

  const [selectedApplicationId, setSelectedApplicationId] = useState("");

  const [selectedListing, setSelectedListing] = useState<JobListing | null>(
    null,
  );

  const [scheduleValue, setScheduleValue] = useState("");

  const [dialog, setDialog] = useState<
    | "schedule-listing"
    | "application-review"
    | "application-status"
    | "application-note"
    | null
  >(null);

  const [notice, setNotice] = useState("");

  const [operationError, setOperationError] = useState("");

  const [reviewRating, setReviewRating] = useState("");

  const [reviewSummary, setReviewSummary] = useState("");

  const [reviewAssigneeId, setReviewAssigneeId] = useState("");

  const [nextApplicationStatus, setNextApplicationStatus] =
    useState<ApplicationStatus>("screening");

  const [rejectionReason, setRejectionReason] = useState("");

  const [noteText, setNoteText] = useState("");

  const [notePrivate, setNotePrivate] = useState(true);

  const dashboardQuery = useCareersDashboard();

  const referenceData = useCareerReferenceData();

  const listingsQuery = useJobListings(listingFilters);

  const applicationsQuery = useJobApplications(applicationFilters);

  const interviewsQuery = useInterviews(interviewFilters);

  const applicationDetailQuery = useJobApplication(
    selectedApplicationId,
    selectedApplicationId !== "",
  );

  const publishMutation = usePublishListing();

  const scheduleMutation = useScheduleListing();

  const closeMutation = useCloseListing();

  const archiveMutation = useArchiveListing();

  const statusMutation = useUpdateApplicationStatus();

  const reviewMutation = useReviewApplication();

  const noteMutation = useAddApplicationNote();

  const isMutating =
    publishMutation.isPending ||
    scheduleMutation.isPending ||
    closeMutation.isPending ||
    archiveMutation.isPending ||
    statusMutation.isPending ||
    reviewMutation.isPending ||
    noteMutation.isPending;

  const listings = listingsQuery.data ?? [];

  const applications = applicationsQuery.data ?? [];

  const interviews = interviewsQuery.data ?? [];

  const selectedApplication = applicationDetailQuery.data;

  const dashboard = dashboardQuery.data;

  const overviewMetrics = useMemo(
    () => [
      {
        label: "Open listings",
        value: dashboard?.open_listings ?? 0,
        icon: BriefcaseBusiness,
      },
      {
        label: "Applications",
        value: dashboard?.total_applications ?? 0,
        icon: Users,
      },
      {
        label: "New applications",
        value: dashboard?.new_applications ?? 0,
        icon: FileText,
      },
      {
        label: "Upcoming interviews",
        value: dashboard?.upcoming_interviews ?? 0,
        icon: Video,
      },
      {
        label: "Shortlisted",
        value: dashboard?.shortlisted_applications ?? 0,
        icon: Star,
      },
      {
        label: "Offered",
        value: dashboard?.offered_applications ?? 0,
        icon: Send,
      },
      {
        label: "Hired",
        value: dashboard?.hired_applications ?? 0,
        icon: UserCheck,
      },
      {
        label: "Completed interviews",
        value: dashboard?.completed_interviews ?? 0,
        icon: CheckCircle2,
      },
    ],
    [dashboard],
  );

  function resetFeedback() {
    setNotice("");
    setOperationError("");
  }

  async function performListingAction(
    listing: JobListing,
    action: "publish" | "close" | "archive",
  ) {
    resetFeedback();

    try {
      if (action === "publish") {
        await publishMutation.mutateAsync(listing.id);
      } else if (action === "close") {
        await closeMutation.mutateAsync(listing.id);
      } else {
        await archiveMutation.mutateAsync(listing.id);
      }

      setNotice(
        `${listing.position_title} was ${action === "publish" ? "published" : action === "close" ? "closed" : "archived"}.`,
      );
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitSchedule() {
    if (!selectedListing || !scheduleValue) {
      return;
    }

    resetFeedback();

    try {
      await scheduleMutation.mutateAsync({
        listingId: selectedListing.id,
        payload: {
          scheduled_for: new Date(scheduleValue).toISOString(),
        },
      });

      setNotice(`${selectedListing.position_title} was scheduled.`);
      setDialog(null);
      setSelectedListing(null);
      setScheduleValue("");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitReview() {
    if (!selectedApplication) {
      return;
    }

    resetFeedback();

    try {
      await reviewMutation.mutateAsync({
        applicationId: selectedApplication.id,
        payload: {
          assigned_to_id: reviewAssigneeId || null,
          rating: reviewRating === "" ? null : Number(reviewRating),
          internal_summary: reviewSummary,
        },
      });

      setNotice(`${selectedApplication.applicant_name}'s review was updated.`);
      setDialog(null);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitStatus() {
    if (!selectedApplication) {
      return;
    }

    resetFeedback();

    try {
      await statusMutation.mutateAsync({
        applicationId: selectedApplication.id,
        payload: {
          status: nextApplicationStatus,
          rejection_reason:
            nextApplicationStatus === "rejected" ? rejectionReason : "",
        },
      });

      setNotice(`${selectedApplication.applicant_name}'s status was updated.`);
      setDialog(null);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitNote() {
    if (!selectedApplication || !noteText.trim()) {
      return;
    }

    resetFeedback();

    try {
      await noteMutation.mutateAsync({
        applicationId: selectedApplication.id,
        payload: {
          note: noteText.trim(),
          is_private: notePrivate,
        },
      });

      setNotice("Application note added.");
      setNoteText("");
      setDialog(null);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  return (
    <div className="space-y-6 pb-10">
      <header>
        <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
          Recruitment operations
        </p>

        <h1 className="mt-2 text-2xl font-bold">Careers</h1>

        <p className="mt-2 max-w-4xl text-sm leading-6 text-slate-500">
          Operate vacancies, candidate pipelines, application reviews, interview
          schedules and recruitment outcomes from one workspace.
        </p>
      </header>

      {(notice || operationError) && (
        <div
          className={
            operationError
              ? "rounded-xl border border-rose-200 bg-rose-50 p-3 text-sm text-rose-700"
              : "rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-700"
          }
        >
          {operationError || notice}
        </div>
      )}

      <nav className="flex flex-wrap gap-2">
        {[
          ["overview", "Overview"],
          ["listings", "Job Listings"],
          ["applications", "Applications"],
          ["interviews", "Interviews"],
        ].map(([value, label]) => (
          <button
            key={value}
            type="button"
            onClick={() => setTab(value as CareersTab)}
            className={
              tab === value
                ? "rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white"
                : "rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-900"
            }
          >
            {label}
          </button>
        ))}
      </nav>

      {tab === "overview" && (
        <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {dashboardQuery.isLoading ? (
            <LoaderBlock />
          ) : (
            overviewMetrics.map((metric) => (
              <Metric key={metric.label} {...metric} />
            ))
          )}
        </section>
      )}

      {tab === "listings" && (
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
          <div className="grid gap-3 border-b border-slate-200 p-5 dark:border-slate-800 md:grid-cols-2 xl:grid-cols-6">
            <SearchInput
              value={listingFilters.search}
              placeholder="Search listings"
              onChange={(value) =>
                setListingFilters((current) => ({
                  ...current,
                  search: value,
                }))
              }
            />

            <select
              value={listingFilters.status}
              onChange={(event) =>
                setListingFilters((current) => ({
                  ...current,
                  status: event.target.value as ListingFilters["status"],
                }))
              }
              className="field"
            >
              <option value="">All statuses</option>
              {jobListingStatuses.map((status) => (
                <option key={status} value={status}>
                  {listingStatusLabels[status]}
                </option>
              ))}
            </select>

            <select
              value={listingFilters.departmentId}
              onChange={(event) =>
                setListingFilters((current) => ({
                  ...current,
                  departmentId: event.target.value,
                }))
              }
              className="field"
            >
              <option value="">All departments</option>
              {(referenceData.departments.data ?? []).map((department) => (
                <option key={department.id} value={department.id}>
                  {department.name}
                </option>
              ))}
            </select>

            <select
              value={listingFilters.employmentTypeId}
              onChange={(event) =>
                setListingFilters((current) => ({
                  ...current,
                  employmentTypeId: event.target.value,
                }))
              }
              className="field"
            >
              <option value="">All employment types</option>
              {(referenceData.employmentTypes.data ?? []).map((type) => (
                <option key={type.id} value={type.id}>
                  {type.name}
                </option>
              ))}
            </select>

            <select
              value={listingFilters.featuredState}
              onChange={(event) =>
                setListingFilters((current) => ({
                  ...current,
                  featuredState: event.target
                    .value as ListingFilters["featuredState"],
                }))
              }
              className="field"
            >
              <option value="all">Any prominence</option>
              <option value="featured">Featured</option>
              <option value="standard">Standard</option>
            </select>

            <button
              type="button"
              onClick={() => setListingFilters(defaultListingFilters)}
              className="button-secondary"
            >
              <FilterX size={16} />
              Reset
            </button>
          </div>

          {listingsQuery.isLoading ? (
            <LoaderBlock />
          ) : listingsQuery.isError ? (
            <ErrorBlock error={listingsQuery.error} />
          ) : (
            <div className="divide-y divide-slate-200 dark:divide-slate-800">
              {listings.map((listing) => (
                <article
                  key={listing.id}
                  className="grid gap-4 p-5 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
                >
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="font-semibold">
                        {listing.position_title}
                      </h2>
                      <StatusBadge
                        status={listing.status}
                        label={listingStatusLabels[listing.status]}
                      />
                      {listing.is_featured && (
                        <span className="rounded-full bg-violet-100 px-2 py-0.5 text-xs font-semibold text-violet-700">
                          Featured
                        </span>
                      )}
                    </div>

                    <p className="mt-1 text-sm text-slate-500">
                      {listing.reference_code} · {listing.department_name} ·{" "}
                      {listing.employment_type_name}
                    </p>

                    <p className="mt-3 text-xs text-slate-500">
                      {listing.number_of_openings} opening(s) · Deadline{" "}
                      {formatDateTime(listing.application_deadline)}
                    </p>
                  </div>

                  <div className="text-sm text-slate-500">
                    <p>
                      {listing.is_publicly_available
                        ? "Publicly available"
                        : "Not public"}
                    </p>
                    <p className="mt-2">
                      Updated {formatDateTime(listing.updated_at)}
                    </p>
                  </div>

                  <div className="flex flex-wrap gap-2 lg:justify-end">
                    {listing.status !== "published" && (
                      <button
                        type="button"
                        disabled={isMutating}
                        onClick={() =>
                          void performListingAction(listing, "publish")
                        }
                        className="button-primary"
                      >
                        Publish
                      </button>
                    )}

                    <button
                      type="button"
                      disabled={isMutating}
                      onClick={() => {
                        setSelectedListing(listing);
                        setDialog("schedule-listing");
                      }}
                      className="button-secondary"
                    >
                      <CalendarClock size={15} />
                      Schedule
                    </button>

                    {listing.status !== "closed" &&
                      listing.status !== "archived" && (
                        <button
                          type="button"
                          disabled={isMutating}
                          onClick={() =>
                            void performListingAction(listing, "close")
                          }
                          className="button-secondary"
                        >
                          <CircleOff size={15} />
                          Close
                        </button>
                      )}

                    {listing.status !== "archived" && (
                      <button
                        type="button"
                        disabled={isMutating}
                        onClick={() =>
                          void performListingAction(listing, "archive")
                        }
                        className="button-danger"
                      >
                        <Archive size={15} />
                        Archive
                      </button>
                    )}
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      )}

      {tab === "applications" && (
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
          <div className="grid gap-3 border-b border-slate-200 p-5 dark:border-slate-800 md:grid-cols-2 xl:grid-cols-6">
            <SearchInput
              value={applicationFilters.search}
              placeholder="Search candidates"
              onChange={(value) =>
                setApplicationFilters((current) => ({
                  ...current,
                  search: value,
                }))
              }
            />

            <select
              value={applicationFilters.status}
              onChange={(event) =>
                setApplicationFilters((current) => ({
                  ...current,
                  status: event.target.value as ApplicationFilters["status"],
                }))
              }
              className="field"
            >
              <option value="">All statuses</option>
              {applicationStatuses.map((status) => (
                <option key={status} value={status}>
                  {applicationStatusLabels[status]}
                </option>
              ))}
            </select>

            <select
              value={applicationFilters.source}
              onChange={(event) =>
                setApplicationFilters((current) => ({
                  ...current,
                  source: event.target.value as ApplicationFilters["source"],
                }))
              }
              className="field"
            >
              <option value="">All sources</option>
              {applicationSources.map((source) => (
                <option key={source} value={source}>
                  {applicationSourceLabels[source]}
                </option>
              ))}
            </select>

            <select
              value={applicationFilters.listingId}
              onChange={(event) =>
                setApplicationFilters((current) => ({
                  ...current,
                  listingId: event.target.value,
                }))
              }
              className="field xl:col-span-2"
            >
              <option value="">All vacancies</option>
              {listings.map((listing) => (
                <option key={listing.id} value={listing.id}>
                  {listing.position_title} — {listing.reference_code}
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={() => setApplicationFilters(defaultApplicationFilters)}
              className="button-secondary"
            >
              <FilterX size={16} />
              Reset
            </button>
          </div>

          {applicationsQuery.isLoading ? (
            <LoaderBlock />
          ) : applicationsQuery.isError ? (
            <ErrorBlock error={applicationsQuery.error} />
          ) : (
            <div className="divide-y divide-slate-200 dark:divide-slate-800">
              {applications.map((application) => (
                <article
                  key={application.id}
                  className="grid gap-4 p-5 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
                >
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="font-semibold">
                        {application.applicant_name}
                      </h2>
                      <StatusBadge
                        status={application.status}
                        label={applicationStatusLabels[application.status]}
                      />
                    </div>

                    <p className="mt-1 text-sm text-slate-500">
                      {application.email}
                      {application.phone ? ` · ${application.phone}` : ""}
                    </p>

                    <p className="mt-2 text-sm text-slate-600 dark:text-slate-400">
                      {application.position_title} ·{" "}
                      {application.listing_reference_code}
                    </p>

                    <p className="mt-2 text-xs text-slate-500">
                      {applicationSourceLabels[application.source]} · Submitted{" "}
                      {formatDateTime(application.submitted_at)}
                    </p>
                  </div>

                  <div className="text-sm text-slate-500">
                    <p>
                      {application.current_position || "No current position"}
                    </p>
                    <p className="mt-2">
                      {application.years_of_experience
                        ? `${application.years_of_experience} years`
                        : "Experience not supplied"}
                    </p>
                    <p className="mt-2">
                      Rating: {application.rating ?? "Not reviewed"}
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() => {
                      resetFeedback();
                      setSelectedApplicationId(application.id);
                    }}
                    className="button-secondary self-start"
                  >
                    <Eye size={16} />
                    Inspect
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>
      )}

      {tab === "interviews" && (
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
          <div className="grid gap-3 border-b border-slate-200 p-5 dark:border-slate-800 md:grid-cols-2 xl:grid-cols-5">
            <select
              value={interviewFilters.status}
              onChange={(event) =>
                setInterviewFilters((current) => ({
                  ...current,
                  status: event.target.value as InterviewFilters["status"],
                }))
              }
              className="field"
            >
              <option value="">All statuses</option>
              {interviewStatuses.map((status) => (
                <option key={status} value={status}>
                  {interviewStatusLabels[status]}
                </option>
              ))}
            </select>

            <select
              value={interviewFilters.interviewType}
              onChange={(event) =>
                setInterviewFilters((current) => ({
                  ...current,
                  interviewType: event.target
                    .value as InterviewFilters["interviewType"],
                }))
              }
              className="field"
            >
              <option value="">All interview types</option>
              {interviewTypes.map((type) => (
                <option key={type} value={type}>
                  {interviewTypeLabels[type]}
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={() => setInterviewFilters(defaultInterviewFilters)}
              className="button-secondary"
            >
              <FilterX size={16} />
              Reset
            </button>
          </div>

          {interviewsQuery.isLoading ? (
            <LoaderBlock />
          ) : interviewsQuery.isError ? (
            <ErrorBlock error={interviewsQuery.error} />
          ) : (
            <div className="divide-y divide-slate-200 dark:divide-slate-800">
              {interviews.map((interview) => (
                <article
                  key={interview.id}
                  className="grid gap-4 p-5 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]"
                >
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="font-semibold">{interview.title}</h2>
                      <StatusBadge
                        status={interview.status}
                        label={interviewStatusLabels[interview.status]}
                      />
                    </div>

                    <p className="mt-1 text-sm text-slate-500">
                      {interview.applicant_name} · {interview.position_title}
                    </p>

                    <p className="mt-2 text-xs text-slate-500">
                      {interviewTypeLabels[interview.interview_type]} ·{" "}
                      {formatDateTime(interview.scheduled_start)} –{" "}
                      {formatDateTime(interview.scheduled_end)}
                    </p>
                  </div>

                  <div className="text-sm text-slate-500 lg:text-right">
                    <p>{interview.location || "Remote / no location"}</p>
                    <p className="mt-2">
                      Organizer: {interview.organizer_name || "Not assigned"}
                    </p>
                    <p className="mt-2">
                      {interview.participants.length} participant(s)
                    </p>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      )}

      {selectedApplicationId && (
        <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/50">
          <aside className="h-full w-full max-w-2xl overflow-y-auto bg-white dark:bg-slate-950">
            <div className="sticky top-0 flex items-center justify-between border-b border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-blue-600">
                  Candidate application
                </p>
                <h2 className="mt-1 text-xl font-bold">
                  {selectedApplication?.applicant_name || "Loading application"}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => setSelectedApplicationId("")}
                aria-label="Close application"
              >
                <X />
              </button>
            </div>

            {applicationDetailQuery.isLoading ? (
              <LoaderBlock />
            ) : !selectedApplication ? (
              <ErrorBlock error={applicationDetailQuery.error} />
            ) : (
              <div className="space-y-6 p-6">
                <section className="grid gap-4 rounded-xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
                  <Detail
                    label="Vacancy"
                    value={selectedApplication.position_title}
                  />
                  <Detail
                    label="Reference"
                    value={selectedApplication.listing_reference_code}
                  />
                  <Detail label="Email" value={selectedApplication.email} />
                  <Detail
                    label="Phone"
                    value={selectedApplication.phone || "Not supplied"}
                  />
                  <Detail
                    label="Location"
                    value={
                      [selectedApplication.city, selectedApplication.country]
                        .filter(Boolean)
                        .join(", ") || "Not supplied"
                    }
                  />
                  <Detail
                    label="Experience"
                    value={
                      selectedApplication.years_of_experience
                        ? `${selectedApplication.years_of_experience} years`
                        : "Not supplied"
                    }
                  />
                  <Detail
                    label="Expected salary"
                    value={formatMoney(
                      selectedApplication.expected_salary,
                      selectedApplication.expected_salary_currency,
                    )}
                  />
                  <Detail
                    label="Available"
                    value={
                      selectedApplication.availability_date || "Not supplied"
                    }
                  />
                  <Detail
                    label="Assigned to"
                    value={selectedApplication.assigned_to_name || "Unassigned"}
                  />
                  <Detail
                    label="Rating"
                    value={
                      selectedApplication.rating
                        ? `${selectedApplication.rating}/5`
                        : "Not reviewed"
                    }
                  />
                </section>

                <section>
                  <h3 className="font-semibold">Cover letter</h3>
                  <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-500">
                    {selectedApplication.cover_letter ||
                      "No cover letter supplied."}
                  </p>
                </section>

                <section>
                  <h3 className="font-semibold">Application answers</h3>
                  <div className="mt-3 space-y-2">
                    {selectedApplication.answers.length ? (
                      selectedApplication.answers.map((answer) => (
                        <div
                          key={answer.id}
                          className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                        >
                          <p className="text-sm font-semibold">
                            {answer.question}
                          </p>
                          <p className="mt-1 break-words text-sm text-slate-500">
                            {typeof answer.answer === "string"
                              ? answer.answer
                              : JSON.stringify(answer.answer)}
                          </p>
                        </div>
                      ))
                    ) : (
                      <EmptyBlock text="No application answers." />
                    )}
                  </div>
                </section>

                <section>
                  <h3 className="font-semibold">Internal notes</h3>
                  <div className="mt-3 space-y-2">
                    {selectedApplication.notes.length ? (
                      selectedApplication.notes.map((note) => (
                        <div
                          key={note.id}
                          className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                        >
                          <p className="text-sm text-slate-600 dark:text-slate-400">
                            {note.note}
                          </p>
                          <p className="mt-2 text-xs text-slate-400">
                            {note.author_name || "System"} ·{" "}
                            {formatDateTime(note.created_at)} ·{" "}
                            {note.is_private ? "Private" : "Shared"}
                          </p>
                        </div>
                      ))
                    ) : (
                      <EmptyBlock text="No notes." />
                    )}
                  </div>
                </section>

                <section className="flex flex-wrap gap-2 border-t border-slate-200 pt-5 dark:border-slate-800">
                  <button
                    type="button"
                    onClick={() => {
                      setReviewRating(
                        selectedApplication.rating?.toString() ?? "",
                      );
                      setReviewSummary(selectedApplication.internal_summary);
                      setReviewAssigneeId(
                        selectedApplication.assigned_to_id ?? "",
                      );
                      setDialog("application-review");
                    }}
                    className="button-primary"
                  >
                    <BadgeCheck size={16} />
                    Review
                  </button>

                  <button
                    type="button"
                    onClick={() => {
                      setNextApplicationStatus(selectedApplication.status);
                      setRejectionReason(selectedApplication.rejection_reason);
                      setDialog("application-status");
                    }}
                    className="button-secondary"
                  >
                    Update status
                  </button>

                  <button
                    type="button"
                    onClick={() => setDialog("application-note")}
                    className="button-secondary"
                  >
                    <MessageSquarePlus size={16} />
                    Add note
                  </button>
                </section>
              </div>
            )}
          </aside>
        </div>
      )}

      {dialog && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 p-4">
          <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl dark:bg-slate-950">
            {dialog === "schedule-listing" && (
              <>
                <h2 className="text-xl font-bold">Schedule listing</h2>
                <input
                  type="datetime-local"
                  value={scheduleValue}
                  onChange={(event) => setScheduleValue(event.target.value)}
                  className="field mt-5 w-full"
                />
                <DialogActions
                  pending={isMutating}
                  disabled={!scheduleValue}
                  onCancel={() => setDialog(null)}
                  onSubmit={() => void submitSchedule()}
                  submitLabel="Schedule"
                />
              </>
            )}

            {dialog === "application-review" && (
              <>
                <h2 className="text-xl font-bold">Review application</h2>

                <label className="mt-5 block text-sm font-semibold">
                  Rating
                </label>
                <select
                  value={reviewRating}
                  onChange={(event) => setReviewRating(event.target.value)}
                  className="field mt-2 w-full"
                >
                  <option value="">No rating</option>
                  {[1, 2, 3, 4, 5].map((rating) => (
                    <option key={rating} value={rating}>
                      {rating}/5
                    </option>
                  ))}
                </select>

                <label className="mt-4 block text-sm font-semibold">
                  Assigned user ID
                </label>
                <input
                  value={reviewAssigneeId}
                  onChange={(event) => setReviewAssigneeId(event.target.value)}
                  placeholder="Optional user UUID"
                  className="field mt-2 w-full"
                />

                <label className="mt-4 block text-sm font-semibold">
                  Internal summary
                </label>
                <textarea
                  value={reviewSummary}
                  onChange={(event) => setReviewSummary(event.target.value)}
                  rows={5}
                  className="field mt-2 w-full"
                />

                <DialogActions
                  pending={isMutating}
                  onCancel={() => setDialog(null)}
                  onSubmit={() => void submitReview()}
                  submitLabel="Save review"
                />
              </>
            )}

            {dialog === "application-status" && (
              <>
                <h2 className="text-xl font-bold">Update application status</h2>

                <select
                  value={nextApplicationStatus}
                  onChange={(event) =>
                    setNextApplicationStatus(
                      event.target.value as ApplicationStatus,
                    )
                  }
                  className="field mt-5 w-full"
                >
                  {applicationStatuses.map((status) => (
                    <option key={status} value={status}>
                      {applicationStatusLabels[status]}
                    </option>
                  ))}
                </select>

                {nextApplicationStatus === "rejected" && (
                  <textarea
                    value={rejectionReason}
                    onChange={(event) => setRejectionReason(event.target.value)}
                    placeholder="Rejection reason"
                    rows={4}
                    className="field mt-4 w-full"
                  />
                )}

                <DialogActions
                  pending={isMutating}
                  onCancel={() => setDialog(null)}
                  onSubmit={() => void submitStatus()}
                  submitLabel="Update status"
                />
              </>
            )}

            {dialog === "application-note" && (
              <>
                <h2 className="text-xl font-bold">Add application note</h2>

                <textarea
                  value={noteText}
                  onChange={(event) => setNoteText(event.target.value)}
                  placeholder="Enter recruitment note"
                  rows={6}
                  className="field mt-5 w-full"
                />

                <label className="mt-4 flex items-center gap-2 text-sm">
                  <input
                    type="checkbox"
                    checked={notePrivate}
                    onChange={(event) => setNotePrivate(event.target.checked)}
                  />
                  Private internal note
                </label>

                <DialogActions
                  pending={isMutating}
                  disabled={!noteText.trim()}
                  onCancel={() => setDialog(null)}
                  onSubmit={() => void submitNote()}
                  submitLabel="Add note"
                />
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
  icon: typeof Users;
}) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center justify-between">
        <p className="text-sm text-slate-500">{label}</p>
        <Icon className="h-5 w-5 text-blue-500" />
      </div>
      <p className="mt-3 text-3xl font-bold">{value}</p>
    </article>
  );
}

function SearchInput({
  value,
  placeholder,
  onChange,
}: {
  value: string;
  placeholder: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="relative xl:col-span-2">
      <Search className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-slate-400" />
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="field w-full pl-10"
      />
    </label>
  );
}

function StatusBadge({ status, label }: { status: string; label: string }) {
  return (
    <span
      className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${statusClasses(status)}`}
    >
      {label}
    </span>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
        {label}
      </p>
      <p className="mt-1 break-words text-sm font-semibold">{value}</p>
    </div>
  );
}

function LoaderBlock() {
  return (
    <div className="flex min-h-48 items-center justify-center gap-2 p-8 text-sm text-slate-500">
      <LoaderCircle className="h-5 w-5 animate-spin" />
      Loading…
    </div>
  );
}

function ErrorBlock({ error }: { error: unknown }) {
  return (
    <div className="p-8 text-center text-sm text-rose-600">
      {errorMessage(error)}
    </div>
  );
}

function EmptyBlock({ text }: { text: string }) {
  return (
    <p className="rounded-xl border border-dashed border-slate-300 p-4 text-sm text-slate-500 dark:border-slate-700">
      {text}
    </p>
  );
}

function DialogActions({
  pending,
  disabled = false,
  onCancel,
  onSubmit,
  submitLabel,
}: {
  pending: boolean;
  disabled?: boolean;
  onCancel: () => void;
  onSubmit: () => void;
  submitLabel: string;
}) {
  return (
    <div className="mt-6 flex justify-end gap-3">
      <button type="button" onClick={onCancel} className="button-secondary">
        Cancel
      </button>
      <button
        type="button"
        disabled={pending || disabled}
        onClick={onSubmit}
        className="button-primary disabled:opacity-50"
      >
        {submitLabel}
      </button>
    </div>
  );
}
