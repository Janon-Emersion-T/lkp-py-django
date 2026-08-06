import {
  Building2,
  CalendarClock,
  ExternalLink,
  Globe2,
  Mail,
  MessageCircle,
  Phone,
  UserRound,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  formatDateTime,
  formatLeadValue,
  formatUserName,
  leadSourceLabels,
  normalizeExternalUrl,
  whatsappUrl,
} from "../formatters";
import {
  useLead,
} from "../hooks";
import {
  LeadPriorityBadge,
  LeadStatusBadge,
} from "./lead-badges";

interface LeadDetailPanelProps {
  leadId: string | null;
  onClose: () => void;
}

export function LeadDetailPanel({
  leadId,
  onClose,
}: LeadDetailPanelProps) {
  const leadQuery = useLead(leadId);
  const lead = leadQuery.data;

  if (!leadId) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        aria-label="Close lead details"
        onClick={onClose}
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Lead record
            </p>

            <h2 className="mt-0.5 font-semibold text-slate-950 dark:text-white">
              {lead?.name ?? "Loading lead"}
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            aria-label="Close lead details"
            className="dark:text-slate-300"
          >
            <X size={19} />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {leadQuery.isLoading && (
            <div className="space-y-4">
              {Array.from({
                length: 6,
              }).map((_, index) => (
                <div
                  key={index}
                  className="h-14 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800"
                />
              ))}
            </div>
          )}

          {leadQuery.isError && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {leadQuery.error instanceof Error
                ? leadQuery.error.message
                : "Lead details could not be loaded."}
            </div>
          )}

          {lead && (
            <div className="space-y-6">
              <section>
                <div className="flex flex-wrap items-center gap-2">
                  <LeadStatusBadge
                    status={lead.status}
                  />

                  <LeadPriorityBadge
                    priority={lead.priority}
                  />

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    Score {lead.lead_score}/100
                  </span>
                </div>

                <h3 className="mt-4 text-2xl font-bold text-slate-950 dark:text-white">
                  {lead.name}
                </h3>

                {lead.company && (
                  <p className="mt-1 flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                    <Building2 size={15} />
                    {lead.company}
                  </p>
                )}

                <p className="mt-4 text-xl font-semibold text-slate-950 dark:text-white">
                  {formatLeadValue(
                    lead.estimated_value,
                    lead.currency,
                  )}
                </p>
              </section>

              <section className="grid gap-3 sm:grid-cols-2">
                {lead.email && (
                  <a
                    href={`mailto:${lead.email}`}
                    className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    <Mail
                      size={17}
                      className="text-slate-400"
                    />
                    <span className="truncate">
                      {lead.email}
                    </span>
                  </a>
                )}

                {lead.phone && (
                  <a
                    href={`tel:${lead.phone}`}
                    className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    <Phone
                      size={17}
                      className="text-slate-400"
                    />
                    <span>{lead.phone}</span>
                  </a>
                )}

                {lead.whatsapp && (
                  <a
                    href={whatsappUrl(
                      lead.whatsapp,
                    )}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    <MessageCircle
                      size={17}
                      className="text-emerald-600"
                    />
                    <span>{lead.whatsapp}</span>
                  </a>
                )}

                {lead.website && (
                  <a
                    href={normalizeExternalUrl(
                      lead.website,
                    )}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    <Globe2
                      size={17}
                      className="text-slate-400"
                    />
                    <span className="truncate">
                      Website
                    </span>
                    <ExternalLink
                      size={14}
                      className="ml-auto"
                    />
                  </a>
                )}
              </section>

              <section className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                  Lead information
                </h4>

                <dl className="mt-4 space-y-4">
                  <div className="flex items-start justify-between gap-4">
                    <dt className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                      <UserRound size={15} />
                      Assigned to
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {formatUserName(
                        lead.assigned_to,
                      )}
                    </dd>
                  </div>

                  <div className="flex items-start justify-between gap-4">
                    <dt className="text-sm text-slate-500 dark:text-slate-400">
                      Source
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {leadSourceLabels[
                        lead.source
                      ]}
                    </dd>
                  </div>

                  <div className="flex items-start justify-between gap-4">
                    <dt className="text-sm text-slate-500 dark:text-slate-400">
                      Country
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {lead.country || "Not provided"}
                    </dd>
                  </div>

                  <div className="flex items-start justify-between gap-4">
                    <dt className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                      <CalendarClock size={15} />
                      Next follow-up
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {formatDateTime(
                        lead.next_follow_up_at,
                      )}
                    </dd>
                  </div>
                </dl>
              </section>

              {lead.tags.length > 0 && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Tags
                  </h4>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {lead.tags.map((tag) => (
                      <span
                        key={tag}
                        className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </section>
              )}

              {lead.notes && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Notes
                  </h4>

                  <p className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-600 dark:bg-slate-800/70 dark:text-slate-300">
                    {lead.notes}
                  </p>
                </section>
              )}

              <section className="border-t border-slate-200 pt-4 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
                <p>
                  Created{" "}
                  {formatDateTime(
                    lead.created_at,
                  )}
                </p>

                <p className="mt-1">
                  Updated{" "}
                  {formatDateTime(
                    lead.updated_at,
                  )}
                </p>
              </section>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
