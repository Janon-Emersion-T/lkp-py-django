import {
  AlertTriangle,
  CalendarCheck,
  CalendarClock,
  CheckCircle2,
  ClipboardCheck,
  Eye,
  FilterX,
  Inbox,
  LoaderCircle,
  Mail,
  MessageSquarePlus,
  Search,
  UserRoundCog,
  Users,
  X,
} from "lucide-react";
import { useMemo, useState } from "react";

import {
  enquiryPriorityLabels,
  enquirySourceLabels,
  enquiryStatusLabels,
  formatDateTime,
  formatMoneyRange,
  priorityClasses,
  statusClasses,
} from "../formatters";
import {
  useAddEnquiryNote,
  useAssignEnquiry,
  useCompleteEnquiryFollowUp,
  useContactEnquiries,
  useEnquiryDashboard,
  useEnquiryDetail,
  useQuoteEnquiries,
  useUpdateEnquiryStatus,
} from "../hooks";
import {
  enquiryPriorities,
  enquirySources,
  enquiryStatuses,
  type BaseEnquiry,
  type ContactEnquiry,
  type ContactEnquiryFilters,
  type EnquiryKind,
  type EnquiryPriority,
  type EnquiryStatus,
  type QuoteEnquiry,
  type QuoteEnquiryFilters,
} from "../types";

type EnquiriesTab = "overview" | "contacts" | "quotes";

type DialogType = "status" | "assignment" | "follow-up" | "note" | null;

const defaultContactFilters: ContactEnquiryFilters = {
  search: "",
  status: "",
  priority: "",
  source: "",
  assignedToId: "",
  ordering: "-submitted_at",
};

const defaultQuoteFilters: QuoteEnquiryFilters = {
  ...defaultContactFilters,
  country: "",
  serviceId: "",
};

function errorMessage(error: unknown) {
  return error instanceof Error
    ? error.message
    : "The operation could not be completed.";
}

function toLocalDateTime(value: string | null) {
  if (!value) {
    return "";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  const offset = date.getTimezoneOffset();

  return new Date(date.getTime() - offset * 60_000).toISOString().slice(0, 16);
}

export function EnquiriesPage() {
  const [tab, setTab] = useState<EnquiriesTab>("overview");

  const [contactFilters, setContactFilters] = useState(defaultContactFilters);

  const [quoteFilters, setQuoteFilters] = useState(defaultQuoteFilters);

  const [selectedKind, setSelectedKind] = useState<EnquiryKind>("contact");

  const [selectedEnquiryId, setSelectedEnquiryId] = useState("");

  const [dialog, setDialog] = useState<DialogType>(null);

  const [notice, setNotice] = useState("");

  const [operationError, setOperationError] = useState("");

  const [statusValue, setStatusValue] = useState<EnquiryStatus>("new");

  const [lossReason, setLossReason] = useState("");

  const [assigneeId, setAssigneeId] = useState("");

  const [priorityValue, setPriorityValue] = useState<EnquiryPriority>("normal");

  const [internalSummary, setInternalSummary] = useState("");

  const [nextFollowUp, setNextFollowUp] = useState("");

  const [noteText, setNoteText] = useState("");

  const [notePrivate, setNotePrivate] = useState(true);

  const dashboardQuery = useEnquiryDashboard();

  const contactsQuery = useContactEnquiries(contactFilters);

  const quotesQuery = useQuoteEnquiries(quoteFilters);

  const detailQuery = useEnquiryDetail(
    selectedKind,
    selectedEnquiryId,
    selectedEnquiryId !== "",
  );

  const statusMutation = useUpdateEnquiryStatus();

  const assignmentMutation = useAssignEnquiry();

  const followUpMutation = useCompleteEnquiryFollowUp();

  const noteMutation = useAddEnquiryNote();

  const dashboard = dashboardQuery.data;

  const contacts = contactsQuery.data ?? [];

  const quotes = quotesQuery.data ?? [];

  const selectedEnquiry = detailQuery.data;

  const isMutating =
    statusMutation.isPending ||
    assignmentMutation.isPending ||
    followUpMutation.isPending ||
    noteMutation.isPending;

  const metrics = useMemo(
    () => [
      {
        label: "Total enquiries",
        value:
          (dashboard?.total_contact_enquiries ?? 0) +
          (dashboard?.total_quote_enquiries ?? 0),
        icon: Inbox,
      },
      {
        label: "New enquiries",
        value:
          (dashboard?.new_contact_enquiries ?? 0) +
          (dashboard?.new_quote_enquiries ?? 0),
        icon: Mail,
      },
      {
        label: "Active pipeline",
        value:
          (dashboard?.active_contact_enquiries ?? 0) +
          (dashboard?.active_quote_enquiries ?? 0),
        icon: Users,
      },
      {
        label: "Won",
        value:
          (dashboard?.won_contact_enquiries ?? 0) +
          (dashboard?.won_quote_enquiries ?? 0),
        icon: CheckCircle2,
      },
      {
        label: "Urgent",
        value:
          (dashboard?.urgent_contact_enquiries ?? 0) +
          (dashboard?.urgent_quote_enquiries ?? 0),
        icon: AlertTriangle,
      },
      {
        label: "Overdue follow-ups",
        value:
          (dashboard?.overdue_contact_follow_ups ?? 0) +
          (dashboard?.overdue_quote_follow_ups ?? 0),
        icon: CalendarClock,
      },
    ],
    [dashboard],
  );

  function resetFeedback() {
    setNotice("");
    setOperationError("");
  }

  function inspectEnquiry(kind: EnquiryKind, enquiryId: string) {
    resetFeedback();
    setSelectedKind(kind);
    setSelectedEnquiryId(enquiryId);
  }

  function openStatusDialog(enquiry: BaseEnquiry) {
    setStatusValue(enquiry.status);
    setLossReason(enquiry.loss_reason);
    setDialog("status");
  }

  function openAssignmentDialog(enquiry: BaseEnquiry) {
    setAssigneeId(enquiry.assigned_to_id ?? "");
    setPriorityValue(enquiry.priority);
    setInternalSummary(enquiry.internal_summary);
    setNextFollowUp(toLocalDateTime(enquiry.next_follow_up_at));
    setDialog("assignment");
  }

  function openFollowUpDialog(enquiry: BaseEnquiry) {
    setNextFollowUp(toLocalDateTime(enquiry.next_follow_up_at));
    setDialog("follow-up");
  }

  async function submitStatus() {
    if (!selectedEnquiry) {
      return;
    }

    resetFeedback();

    try {
      await statusMutation.mutateAsync({
        kind: selectedKind,
        enquiryId: selectedEnquiry.id,
        payload: {
          status: statusValue,
          loss_reason: statusValue === "lost" ? lossReason : "",
        },
      });

      setNotice(`${selectedEnquiry.reference_code} status updated.`);
      setDialog(null);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitAssignment() {
    if (!selectedEnquiry) {
      return;
    }

    resetFeedback();

    try {
      await assignmentMutation.mutateAsync({
        kind: selectedKind,
        enquiryId: selectedEnquiry.id,
        payload: {
          assigned_to_id: assigneeId.trim() || null,
          priority: priorityValue,
          internal_summary: internalSummary,
          next_follow_up_at: nextFollowUp
            ? new Date(nextFollowUp).toISOString()
            : null,
        },
      });

      setNotice(`${selectedEnquiry.reference_code} assignment updated.`);
      setDialog(null);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitFollowUp() {
    if (!selectedEnquiry) {
      return;
    }

    resetFeedback();

    try {
      await followUpMutation.mutateAsync({
        kind: selectedKind,
        enquiryId: selectedEnquiry.id,
        payload: {
          next_follow_up_at: nextFollowUp
            ? new Date(nextFollowUp).toISOString()
            : null,
        },
      });

      setNotice(`${selectedEnquiry.reference_code} follow-up completed.`);
      setDialog(null);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitNote() {
    if (!selectedEnquiry || !noteText.trim()) {
      return;
    }

    resetFeedback();

    try {
      await noteMutation.mutateAsync({
        kind: selectedKind,
        enquiryId: selectedEnquiry.id,
        payload: {
          note: noteText.trim(),
          is_private: notePrivate,
        },
      });

      setNotice("Enquiry note added.");
      setNoteText("");
      setDialog(null);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  return (
    <div className="space-y-6 pb-10">
      <header className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Inbound sales operations
          </p>

          <h1 className="mt-2 text-2xl font-bold">Enquiries</h1>

          <p className="mt-2 max-w-4xl text-sm leading-6 text-slate-500">
            Manage contact messages and quote requests, ownership, priority,
            qualification, proposals, follow-ups, outcomes and internal notes.
          </p>
        </div>

        <div className="flex gap-2">
          <button
            type="button"
            disabled
            title="Manual contact-enquiry creation will be included in the full editor milestone."
            className="button-secondary opacity-60"
          >
            New contact
          </button>

          <button
            type="button"
            disabled
            title="Manual quote-enquiry creation will be included in the full editor milestone."
            className="button-primary opacity-60"
          >
            New quote request
          </button>
        </div>
      </header>

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

      <nav className="flex flex-wrap gap-2">
        {[
          ["overview", "Overview"],
          ["contacts", "Contact Enquiries"],
          ["quotes", "Quote Requests"],
        ].map(([value, label]) => (
          <button
            key={value}
            type="button"
            onClick={() => setTab(value as EnquiriesTab)}
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
        <>
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {dashboardQuery.isLoading ? (
              <LoaderBlock />
            ) : dashboardQuery.isError ? (
              <ErrorBlock error={dashboardQuery.error} />
            ) : (
              metrics.map((metric) => <Metric key={metric.label} {...metric} />)
            )}
          </section>

          {dashboard && (
            <section className="grid gap-5 xl:grid-cols-2">
              <BreakdownCard
                title="Contact enquiries"
                total={dashboard.total_contact_enquiries}
                newCount={dashboard.new_contact_enquiries}
                active={dashboard.active_contact_enquiries}
                won={dashboard.won_contact_enquiries}
                lost={dashboard.lost_contact_enquiries}
                urgent={dashboard.urgent_contact_enquiries}
                overdue={dashboard.overdue_contact_follow_ups}
              />

              <BreakdownCard
                title="Quote requests"
                total={dashboard.total_quote_enquiries}
                newCount={dashboard.new_quote_enquiries}
                active={dashboard.active_quote_enquiries}
                won={dashboard.won_quote_enquiries}
                lost={dashboard.lost_quote_enquiries}
                urgent={dashboard.urgent_quote_enquiries}
                overdue={dashboard.overdue_quote_follow_ups}
              />
            </section>
          )}
        </>
      )}

      {tab === "contacts" && (
        <EnquiryListSection
          kind="contact"
          filters={contactFilters}
          onFiltersChange={(changes) =>
            setContactFilters((current) => ({
              ...current,
              ...changes,
            }))
          }
          enquiries={contacts}
          isLoading={contactsQuery.isLoading}
          error={contactsQuery.error}
          onInspect={(enquiry) => inspectEnquiry("contact", enquiry.id)}
          onReset={() => setContactFilters(defaultContactFilters)}
        />
      )}

      {tab === "quotes" && (
        <EnquiryListSection
          kind="quote"
          filters={quoteFilters}
          onFiltersChange={(changes) =>
            setQuoteFilters((current) => ({
              ...current,
              ...changes,
            }))
          }
          enquiries={quotes}
          isLoading={quotesQuery.isLoading}
          error={quotesQuery.error}
          onInspect={(enquiry) => inspectEnquiry("quote", enquiry.id)}
          onReset={() => setQuoteFilters(defaultQuoteFilters)}
        />
      )}

      {selectedEnquiryId && (
        <div className="fixed inset-0 z-50 flex justify-end bg-slate-950/50">
          <aside className="h-full w-full max-w-2xl overflow-y-auto bg-white shadow-2xl dark:bg-slate-950">
            <div className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white/95 p-5 backdrop-blur dark:border-slate-800 dark:bg-slate-950/95">
              <div>
                <p className="text-xs font-semibold uppercase tracking-wider text-blue-600">
                  {selectedKind === "contact"
                    ? "Contact enquiry"
                    : "Quote request"}
                </p>

                <h2 className="mt-1 text-xl font-bold">
                  {selectedEnquiry?.reference_code || "Loading enquiry"}
                </h2>
              </div>

              <button
                type="button"
                onClick={() => {
                  setSelectedEnquiryId("");
                  setDialog(null);
                }}
                className="rounded-lg p-2 hover:bg-slate-100 dark:hover:bg-slate-800"
                aria-label="Close enquiry details"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {detailQuery.isLoading ? (
              <LoaderBlock />
            ) : detailQuery.isError || !selectedEnquiry ? (
              <ErrorBlock error={detailQuery.error} />
            ) : (
              <EnquiryDetail
                kind={selectedKind}
                enquiry={selectedEnquiry}
                isMutating={isMutating}
                onStatus={() => openStatusDialog(selectedEnquiry)}
                onAssignment={() => openAssignmentDialog(selectedEnquiry)}
                onFollowUp={() => openFollowUpDialog(selectedEnquiry)}
                onNote={() => setDialog("note")}
              />
            )}
          </aside>
        </div>
      )}

      {dialog && selectedEnquiry && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 p-4">
          <div className="w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl dark:bg-slate-950">
            {dialog === "status" && (
              <>
                <h2 className="text-xl font-bold">Update enquiry status</h2>

                <select
                  value={statusValue}
                  onChange={(event) =>
                    setStatusValue(event.target.value as EnquiryStatus)
                  }
                  className="field mt-5 w-full"
                >
                  {enquiryStatuses.map((status) => (
                    <option key={status} value={status}>
                      {enquiryStatusLabels[status]}
                    </option>
                  ))}
                </select>

                {statusValue === "lost" && (
                  <textarea
                    value={lossReason}
                    onChange={(event) => setLossReason(event.target.value)}
                    rows={4}
                    placeholder="Reason the opportunity was lost"
                    className="field mt-4 h-auto min-h-28 w-full py-3"
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

            {dialog === "assignment" && (
              <>
                <h2 className="text-xl font-bold">Assignment and priority</h2>

                <label className="mt-5 block text-sm font-semibold">
                  Assigned user ID
                </label>

                <input
                  value={assigneeId}
                  onChange={(event) => setAssigneeId(event.target.value)}
                  placeholder="Optional user UUID"
                  className="field mt-2 w-full"
                />

                <label className="mt-4 block text-sm font-semibold">
                  Priority
                </label>

                <select
                  value={priorityValue}
                  onChange={(event) =>
                    setPriorityValue(event.target.value as EnquiryPriority)
                  }
                  className="field mt-2 w-full"
                >
                  {enquiryPriorities.map((priority) => (
                    <option key={priority} value={priority}>
                      {enquiryPriorityLabels[priority]}
                    </option>
                  ))}
                </select>

                <label className="mt-4 block text-sm font-semibold">
                  Next follow-up
                </label>

                <input
                  type="datetime-local"
                  value={nextFollowUp}
                  onChange={(event) => setNextFollowUp(event.target.value)}
                  className="field mt-2 w-full"
                />

                <label className="mt-4 block text-sm font-semibold">
                  Internal summary
                </label>

                <textarea
                  value={internalSummary}
                  onChange={(event) => setInternalSummary(event.target.value)}
                  rows={5}
                  className="field mt-2 h-auto min-h-32 w-full py-3"
                />

                <DialogActions
                  pending={isMutating}
                  onCancel={() => setDialog(null)}
                  onSubmit={() => void submitAssignment()}
                  submitLabel="Save assignment"
                />
              </>
            )}

            {dialog === "follow-up" && (
              <>
                <h2 className="text-xl font-bold">Complete follow-up</h2>

                <p className="mt-2 text-sm leading-6 text-slate-500">
                  The current time will be recorded as the completed follow-up.
                  Optionally schedule the next one.
                </p>

                <label className="mt-5 block text-sm font-semibold">
                  Next follow-up
                </label>

                <input
                  type="datetime-local"
                  value={nextFollowUp}
                  onChange={(event) => setNextFollowUp(event.target.value)}
                  className="field mt-2 w-full"
                />

                <DialogActions
                  pending={isMutating}
                  onCancel={() => setDialog(null)}
                  onSubmit={() => void submitFollowUp()}
                  submitLabel="Complete follow-up"
                />
              </>
            )}

            {dialog === "note" && (
              <>
                <h2 className="text-xl font-bold">Add enquiry note</h2>

                <textarea
                  value={noteText}
                  onChange={(event) => setNoteText(event.target.value)}
                  placeholder="Enter an internal sales note"
                  rows={6}
                  className="field mt-5 h-auto min-h-36 w-full py-3"
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

function EnquiryListSection({
  kind,
  filters,
  onFiltersChange,
  enquiries,
  isLoading,
  error,
  onInspect,
  onReset,
}: {
  kind: EnquiryKind;
  filters: ContactEnquiryFilters | QuoteEnquiryFilters;
  onFiltersChange: (
    changes: Partial<ContactEnquiryFilters & QuoteEnquiryFilters>,
  ) => void;
  enquiries: ContactEnquiry[] | QuoteEnquiry[];
  isLoading: boolean;
  error: unknown;
  onInspect: (enquiry: ContactEnquiry | QuoteEnquiry) => void;
  onReset: () => void;
}) {
  const quoteFilters =
    kind === "quote" ? (filters as QuoteEnquiryFilters) : null;

  return (
    <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-950">
      <div className="grid gap-3 border-b border-slate-200 p-5 dark:border-slate-800 md:grid-cols-2 xl:grid-cols-6">
        <label className="relative xl:col-span-2">
          <Search className="pointer-events-none absolute left-3 top-3 h-4 w-4 text-slate-400" />

          <input
            value={filters.search}
            onChange={(event) =>
              onFiltersChange({
                search: event.target.value,
              })
            }
            placeholder={
              kind === "contact"
                ? "Search contact enquiries"
                : "Search quote requests"
            }
            className="field w-full pl-10"
          />
        </label>

        <select
          value={filters.status}
          onChange={(event) =>
            onFiltersChange({
              status: event.target.value as ContactEnquiryFilters["status"],
            })
          }
          className="field"
        >
          <option value="">All statuses</option>

          {enquiryStatuses.map((status) => (
            <option key={status} value={status}>
              {enquiryStatusLabels[status]}
            </option>
          ))}
        </select>

        <select
          value={filters.priority}
          onChange={(event) =>
            onFiltersChange({
              priority: event.target.value as ContactEnquiryFilters["priority"],
            })
          }
          className="field"
        >
          <option value="">All priorities</option>

          {enquiryPriorities.map((priority) => (
            <option key={priority} value={priority}>
              {enquiryPriorityLabels[priority]}
            </option>
          ))}
        </select>

        <select
          value={filters.source}
          onChange={(event) =>
            onFiltersChange({
              source: event.target.value as ContactEnquiryFilters["source"],
            })
          }
          className="field"
        >
          <option value="">All sources</option>

          {enquirySources.map((source) => (
            <option key={source} value={source}>
              {enquirySourceLabels[source]}
            </option>
          ))}
        </select>

        <button type="button" onClick={onReset} className="button-secondary">
          <FilterX size={16} />
          Reset
        </button>

        <input
          value={filters.assignedToId}
          onChange={(event) =>
            onFiltersChange({
              assignedToId: event.target.value,
            })
          }
          placeholder="Assigned user ID"
          className="field"
        />

        {quoteFilters && (
          <>
            <input
              value={quoteFilters.country}
              onChange={(event) =>
                onFiltersChange({
                  country: event.target.value,
                })
              }
              placeholder="Country"
              className="field"
            />

            <input
              value={quoteFilters.serviceId}
              onChange={(event) =>
                onFiltersChange({
                  serviceId: event.target.value,
                })
              }
              placeholder="Service ID"
              className="field"
            />
          </>
        )}

        <select
          value={filters.ordering}
          onChange={(event) =>
            onFiltersChange({
              ordering: event.target.value,
            })
          }
          className="field xl:col-span-2"
        >
          <option value="-submitted_at">Recently submitted</option>

          <option value="submitted_at">Oldest submitted</option>

          <option value="priority">Priority ascending</option>

          <option value="-priority">Priority descending</option>

          <option value="next_follow_up_at">Next follow-up</option>

          <option value="-updated_at">Recently updated</option>

          <option value="name">Name A–Z</option>
        </select>
      </div>

      {isLoading ? (
        <LoaderBlock />
      ) : error ? (
        <ErrorBlock error={error} />
      ) : enquiries.length === 0 ? (
        <EmptyBlock
          text={
            kind === "contact"
              ? "No contact enquiries match the current filters."
              : "No quote requests match the current filters."
          }
        />
      ) : (
        <div className="divide-y divide-slate-200 dark:divide-slate-800">
          {enquiries.map((enquiry) => (
            <article
              key={enquiry.id}
              className="grid gap-4 p-5 transition hover:bg-slate-50 dark:hover:bg-slate-900/50 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
            >
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <h2 className="font-semibold">{enquiry.name}</h2>

                  <span
                    className={`rounded-full border px-2 py-0.5 text-xs font-semibold ${statusClasses(enquiry.status)}`}
                  >
                    {enquiryStatusLabels[enquiry.status]}
                  </span>

                  <span
                    className={`rounded-full px-2 py-0.5 text-xs font-semibold ${priorityClasses(enquiry.priority)}`}
                  >
                    {enquiryPriorityLabels[enquiry.priority]}
                  </span>
                </div>

                <p className="mt-1 text-sm text-slate-500">
                  {enquiry.reference_code} ·{" "}
                  {enquiry.company_name || "No company"}
                </p>

                <p className="mt-2 line-clamp-2 text-sm leading-6 text-slate-600 dark:text-slate-400">
                  {"subject" in enquiry
                    ? enquiry.subject || enquiry.message
                    : enquiry.project_title || enquiry.project_description}
                </p>

                <div className="mt-3 flex flex-wrap gap-x-5 gap-y-2 text-xs text-slate-500">
                  <span>{enquirySourceLabels[enquiry.source]}</span>

                  <span>Submitted {formatDateTime(enquiry.submitted_at)}</span>

                  <span>{enquiry.assigned_to_name || "Unassigned"}</span>
                </div>
              </div>

              <div className="space-y-2 text-sm text-slate-500">
                <p>{enquiry.email || "No email"}</p>

                <p>{enquiry.phone || "No phone"}</p>

                <p className="text-xs">
                  Next follow-up: {formatDateTime(enquiry.next_follow_up_at)}
                </p>
              </div>

              <button
                type="button"
                onClick={() => onInspect(enquiry)}
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
  );
}

function EnquiryDetail({
  kind,
  enquiry,
  isMutating,
  onStatus,
  onAssignment,
  onFollowUp,
  onNote,
}: {
  kind: EnquiryKind;
  enquiry: ContactEnquiry | QuoteEnquiry;
  isMutating: boolean;
  onStatus: () => void;
  onAssignment: () => void;
  onFollowUp: () => void;
  onNote: () => void;
}) {
  const quote = kind === "quote" ? (enquiry as QuoteEnquiry) : null;

  const contact = kind === "contact" ? (enquiry as ContactEnquiry) : null;

  return (
    <div className="space-y-6 p-6">
      <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
        <Detail label="Name" value={enquiry.name} />

        <Detail
          label="Company"
          value={enquiry.company_name || "Not supplied"}
        />

        <Detail label="Email" value={enquiry.email || "Not supplied"} />

        <Detail label="Phone" value={enquiry.phone || "Not supplied"} />

        <Detail label="Status" value={enquiryStatusLabels[enquiry.status]} />

        <Detail
          label="Priority"
          value={enquiryPriorityLabels[enquiry.priority]}
        />

        <Detail label="Source" value={enquirySourceLabels[enquiry.source]} />

        <Detail
          label="Assigned to"
          value={enquiry.assigned_to_name || "Unassigned"}
        />

        <Detail
          label="Submitted"
          value={formatDateTime(enquiry.submitted_at)}
        />

        <Detail
          label="Next follow-up"
          value={formatDateTime(enquiry.next_follow_up_at)}
        />

        <Detail
          label="First contacted"
          value={formatDateTime(enquiry.first_contacted_at)}
        />

        <Detail label="Resolved" value={formatDateTime(enquiry.resolved_at)} />
      </section>

      {contact && (
        <>
          <section>
            <h3 className="font-semibold">Subject</h3>

            <p className="mt-2 text-sm leading-6 text-slate-500">
              {contact.subject || "No subject supplied."}
            </p>
          </section>

          <section>
            <h3 className="font-semibold">Message</h3>

            <p className="mt-2 whitespace-pre-wrap text-sm leading-7 text-slate-500">
              {contact.message}
            </p>
          </section>
        </>
      )}

      {quote && (
        <>
          <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
            <Detail
              label="Project"
              value={quote.project_title || "Not supplied"}
            />

            <Detail label="Country" value={quote.country || "Not supplied"} />

            <Detail
              label="Budget"
              value={formatMoneyRange(
                quote.budget_min,
                quote.budget_max,
                quote.budget_currency,
              )}
            />

            <Detail
              label="Desired start"
              value={quote.desired_start_date || "Not supplied"}
            />

            <Detail
              label="Desired completion"
              value={quote.desired_completion_date || "Not supplied"}
            />

            <Detail
              label="Quotation"
              value={quote.quotation_id || "Not created"}
            />
          </section>

          <section>
            <h3 className="font-semibold">Project description</h3>

            <p className="mt-2 whitespace-pre-wrap text-sm leading-7 text-slate-500">
              {quote.project_description}
            </p>
          </section>

          <section>
            <h3 className="font-semibold">Required services</h3>

            <div className="mt-3 space-y-2">
              {quote.services.length ? (
                quote.services.map((service) => (
                  <div
                    key={service.id}
                    className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
                  >
                    <p className="text-sm font-semibold">
                      {service.service_title}
                    </p>

                    {service.notes && (
                      <p className="mt-1 text-xs leading-5 text-slate-500">
                        {service.notes}
                      </p>
                    )}
                  </div>
                ))
              ) : (
                <EmptyBlock text="No services selected." />
              )}
            </div>
          </section>
        </>
      )}

      <section className="rounded-2xl border border-slate-200 p-5 dark:border-slate-800">
        <h3 className="font-semibold">Internal summary</h3>

        <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-500">
          {enquiry.internal_summary || "No internal summary."}
        </p>
      </section>

      {enquiry.loss_reason && (
        <section className="rounded-2xl border border-rose-200 bg-rose-50 p-5 dark:border-rose-900 dark:bg-rose-950/30">
          <h3 className="font-semibold text-rose-700 dark:text-rose-300">
            Loss reason
          </h3>

          <p className="mt-2 text-sm leading-6 text-rose-600 dark:text-rose-400">
            {enquiry.loss_reason}
          </p>
        </section>
      )}

      <section>
        <h3 className="font-semibold">Notes</h3>

        <div className="mt-3 space-y-2">
          {enquiry.notes.length ? (
            enquiry.notes.map((note) => (
              <div
                key={note.id}
                className="rounded-xl border border-slate-200 p-3 dark:border-slate-800"
              >
                <p className="whitespace-pre-wrap text-sm text-slate-600 dark:text-slate-400">
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
            <EmptyBlock text="No enquiry notes." />
          )}
        </div>
      </section>

      <section className="flex flex-wrap gap-2 border-t border-slate-200 pt-6 dark:border-slate-800">
        <button
          type="button"
          disabled={isMutating}
          onClick={onStatus}
          className="button-primary"
        >
          <ClipboardCheck size={16} />
          Update status
        </button>

        <button
          type="button"
          disabled={isMutating}
          onClick={onAssignment}
          className="button-secondary"
        >
          <UserRoundCog size={16} />
          Assignment
        </button>

        <button
          type="button"
          disabled={isMutating}
          onClick={onFollowUp}
          className="button-secondary"
        >
          <CalendarCheck size={16} />
          Complete follow-up
        </button>

        <button
          type="button"
          disabled={isMutating}
          onClick={onNote}
          className="button-secondary"
        >
          <MessageSquarePlus size={16} />
          Add note
        </button>
      </section>
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
  icon: typeof Inbox;
}) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{label}</p>

        <Icon className="h-5 w-5 text-blue-500" />
      </div>

      <p className="mt-3 text-3xl font-bold">{value}</p>
    </article>
  );
}

function BreakdownCard({
  title,
  total,
  newCount,
  active,
  won,
  lost,
  urgent,
  overdue,
}: {
  title: string;
  total: number;
  newCount: number;
  active: number;
  won: number;
  lost: number;
  urgent: number;
  overdue: number;
}) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950">
      <h2 className="font-semibold">{title}</h2>

      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        <SmallMetric label="Total" value={total} />
        <SmallMetric label="New" value={newCount} />
        <SmallMetric label="Active" value={active} />
        <SmallMetric label="Won" value={won} />
        <SmallMetric label="Lost" value={lost} />
        <SmallMetric label="Urgent" value={urgent} />
        <SmallMetric label="Overdue" value={overdue} />
      </div>
    </article>
  );
}

function SmallMetric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3 dark:bg-slate-900">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 text-xl font-bold">{value}</p>
    </div>
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
    <p className="m-5 rounded-xl border border-dashed border-slate-300 p-5 text-center text-sm text-slate-500 dark:border-slate-700">
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
