import {
  Building2,
  CalendarClock,
  ChevronRight,
  FileText,
  Inbox,
} from "lucide-react";

import {
  formatCurrency,
  formatDate,
} from "../formatters";
import type {
  Quotation,
} from "../types";
import {
  QuotationStatusBadge,
} from "./quotation-status-badge";

interface QuotationListProps {
  quotations: Quotation[];
  onSelect: (
    quotationId: string,
  ) => void;
}

export function QuotationList({
  quotations,
  onSelect,
}: QuotationListProps) {
  if (quotations.length === 0) {
    return (
      <section className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center dark:border-slate-700 dark:bg-slate-900">
        <Inbox
          size={30}
          className="mx-auto text-slate-300 dark:text-slate-600"
        />

        <h2 className="mt-4 font-semibold text-slate-950 dark:text-white">
          No quotations found
        </h2>

        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          No quotation records match the current search and filters.
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
                  Quotation
                </th>
                <th className="px-5 py-3">
                  Client
                </th>
                <th className="px-5 py-3">
                  Status
                </th>
                <th className="px-5 py-3">
                  Issue date
                </th>
                <th className="px-5 py-3">
                  Expiry date
                </th>
                <th className="px-5 py-3">
                  Items
                </th>
                <th className="px-5 py-3">
                  Total
                </th>
                <th className="w-12 px-3 py-3">
                  <span className="sr-only">
                    View
                  </span>
                </th>
              </tr>
            </thead>

            <tbody>
              {quotations.map(
                (quotation) => (
                  <tr
                    key={quotation.id}
                    className="border-t border-slate-200 transition hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/50"
                  >
                    <td className="px-5 py-4">
                      <button
                        type="button"
                        onClick={() => {
                          onSelect(
                            quotation.id,
                          );
                        }}
                        className="text-left"
                      >
                        <p className="font-medium text-slate-950 hover:text-blue-700 dark:text-white dark:hover:text-blue-400">
                          {quotation.title}
                        </p>

                        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                          {
                            quotation.quotation_number
                          }
                        </p>
                      </button>
                    </td>

                    <td className="px-5 py-4">
                      <span className="inline-flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                        <Building2
                          size={15}
                          className="text-slate-400"
                        />
                        <span className="max-w-48 truncate">
                          {
                            quotation.client_name
                          }
                        </span>
                      </span>
                    </td>

                    <td className="px-5 py-4">
                      <div className="space-y-1">
                        <QuotationStatusBadge
                          status={
                            quotation.status
                          }
                        />

                        {quotation.is_expired
                          && quotation.status
                            !== "expired" && (
                            <p className="text-xs font-medium text-amber-700 dark:text-amber-400">
                              Past expiry
                            </p>
                          )}
                      </div>
                    </td>

                    <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                      {formatDate(
                        quotation.issue_date,
                      )}
                    </td>

                    <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                      {formatDate(
                        quotation.expiry_date,
                      )}
                    </td>

                    <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                      {quotation.items.length}
                    </td>

                    <td className="px-5 py-4 text-sm font-semibold text-slate-950 dark:text-white">
                      {formatCurrency(
                        quotation.total_amount,
                        quotation.currency,
                      )}
                    </td>

                    <td className="px-3 py-4">
                      <button
                        type="button"
                        onClick={() => {
                          onSelect(
                            quotation.id,
                          );
                        }}
                        aria-label={`View ${quotation.quotation_number}`}
                        className="grid h-8 w-8 place-items-center rounded-md text-slate-400 transition hover:bg-slate-100 hover:text-slate-950 dark:hover:bg-slate-700 dark:hover:text-white"
                      >
                        <ChevronRight
                          size={17}
                        />
                      </button>
                    </td>
                  </tr>
                ),
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid gap-3 lg:hidden">
        {quotations.map(
          (quotation) => (
            <button
              key={quotation.id}
              type="button"
              onClick={() => {
                onSelect(quotation.id);
              }}
              className="rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:border-blue-300 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-blue-800"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate font-semibold text-slate-950 dark:text-white">
                    {quotation.title}
                  </p>

                  <p className="mt-1 flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
                    <FileText size={13} />
                    {
                      quotation.quotation_number
                    }
                  </p>
                </div>

                <ChevronRight
                  size={18}
                  className="shrink-0 text-slate-400"
                />
              </div>

              <div className="mt-4 flex flex-wrap items-center gap-2">
                <QuotationStatusBadge
                  status={
                    quotation.status
                  }
                />

                <span className="ml-auto text-sm font-semibold text-slate-950 dark:text-white">
                  {formatCurrency(
                    quotation.total_amount,
                    quotation.currency,
                  )}
                </span>
              </div>

              <div className="mt-4 grid gap-2 border-t border-slate-100 pt-3 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
                <span className="flex items-center gap-2">
                  <Building2 size={13} />
                  {quotation.client_name}
                </span>

                <span className="flex items-center gap-2">
                  <CalendarClock
                    size={13}
                  />
                  Expires{" "}
                  {formatDate(
                    quotation.expiry_date,
                  )}
                </span>
              </div>
            </button>
          ),
        )}
      </section>
    </>
  );
}
