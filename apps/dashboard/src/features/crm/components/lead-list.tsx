import {
  Building2,
  ChevronRight,
  Inbox,
  UserRound,
} from "lucide-react";

import {
  formatDateTime,
  formatLeadValue,
  formatUserName,
  leadSourceLabels,
} from "../formatters";
import type {
  Lead,
} from "../types";
import {
  LeadPriorityBadge,
  LeadStatusBadge,
} from "./lead-badges";

interface LeadListProps {
  leads: Lead[];
  onSelect: (leadId: string) => void;
}

export function LeadList({
  leads,
  onSelect,
}: LeadListProps) {
  if (leads.length === 0) {
    return (
      <section className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center dark:border-slate-700 dark:bg-slate-900">
        <Inbox
          size={30}
          className="mx-auto text-slate-300 dark:text-slate-600"
        />

        <h2 className="mt-4 font-semibold text-slate-950 dark:text-white">
          No leads found
        </h2>

        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          No CRM records match the current search and filters.
        </p>
      </section>
    );
  }

  return (
    <>
      <section className="hidden overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm lg:block dark:border-slate-800 dark:bg-slate-900">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[1050px] border-collapse">
            <thead className="bg-slate-50 dark:bg-slate-800/70">
              <tr className="text-left text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                <th className="px-5 py-3">
                  Lead
                </th>
                <th className="px-5 py-3">
                  Status
                </th>
                <th className="px-5 py-3">
                  Source
                </th>
                <th className="px-5 py-3">
                  Owner
                </th>
                <th className="px-5 py-3">
                  Score
                </th>
                <th className="px-5 py-3">
                  Estimated value
                </th>
                <th className="px-5 py-3">
                  Follow-up
                </th>
                <th className="w-12 px-3 py-3">
                  <span className="sr-only">
                    View
                  </span>
                </th>
              </tr>
            </thead>

            <tbody>
              {leads.map((lead) => (
                <tr
                  key={lead.id}
                  className="border-t border-slate-200 transition hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/50"
                >
                  <td className="px-5 py-4">
                    <button
                      type="button"
                      onClick={() => {
                        onSelect(lead.id);
                      }}
                      className="text-left"
                    >
                      <p className="font-medium text-slate-950 hover:text-blue-700 dark:text-white dark:hover:text-blue-400">
                        {lead.name}
                      </p>

                      <p className="mt-1 max-w-56 truncate text-xs text-slate-500 dark:text-slate-400">
                        {lead.company
                          || lead.email
                          || "No company provided"}
                      </p>
                    </button>
                  </td>

                  <td className="px-5 py-4">
                    <div className="space-y-1.5">
                      <LeadStatusBadge
                        status={lead.status}
                      />

                      <div>
                        <LeadPriorityBadge
                          priority={lead.priority}
                        />
                      </div>
                    </div>
                  </td>

                  <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                    {leadSourceLabels[
                      lead.source
                    ]}
                  </td>

                  <td className="px-5 py-4">
                    <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                      <UserRound
                        size={15}
                        className="text-slate-400"
                      />
                      <span className="max-w-40 truncate">
                        {formatUserName(
                          lead.assigned_to,
                        )}
                      </span>
                    </div>
                  </td>

                  <td className="px-5 py-4">
                    <span className="font-semibold text-slate-950 dark:text-white">
                      {lead.lead_score}
                    </span>

                    <span className="text-xs text-slate-400">
                      /100
                    </span>
                  </td>

                  <td className="px-5 py-4 text-sm font-medium text-slate-950 dark:text-white">
                    {formatLeadValue(
                      lead.estimated_value,
                      lead.currency,
                    )}
                  </td>

                  <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                    {formatDateTime(
                      lead.next_follow_up_at,
                    )}
                  </td>

                  <td className="px-3 py-4">
                    <button
                      type="button"
                      onClick={() => {
                        onSelect(lead.id);
                      }}
                      aria-label={`View ${lead.name}`}
                      className="grid h-8 w-8 place-items-center rounded-md text-slate-400 transition hover:bg-slate-100 hover:text-slate-950 dark:hover:bg-slate-700 dark:hover:text-white"
                    >
                      <ChevronRight size={17} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid gap-3 lg:hidden">
        {leads.map((lead) => (
          <button
            key={lead.id}
            type="button"
            onClick={() => {
              onSelect(lead.id);
            }}
            className="rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:border-blue-300 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-blue-800"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="truncate font-semibold text-slate-950 dark:text-white">
                  {lead.name}
                </p>

                <p className="mt-1 flex items-center gap-1.5 truncate text-xs text-slate-500 dark:text-slate-400">
                  <Building2 size={13} />
                  {lead.company || "No company"}
                </p>
              </div>

              <ChevronRight
                size={18}
                className="shrink-0 text-slate-400"
              />
            </div>

            <div className="mt-4 flex flex-wrap items-center gap-2">
              <LeadStatusBadge
                status={lead.status}
              />

              <LeadPriorityBadge
                priority={lead.priority}
              />

              <span className="ml-auto text-sm font-semibold text-slate-950 dark:text-white">
                {formatLeadValue(
                  lead.estimated_value,
                  lead.currency,
                )}
              </span>
            </div>

            <div className="mt-4 grid grid-cols-2 gap-3 border-t border-slate-100 pt-3 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
              <span>
                Score: {lead.lead_score}/100
              </span>

              <span className="text-right">
                {leadSourceLabels[
                  lead.source
                ]}
              </span>
            </div>
          </button>
        ))}
      </section>
    </>
  );
}
