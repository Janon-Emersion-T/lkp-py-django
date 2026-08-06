import {
  CalendarClock,
  Eye,
  FileText,
  Link2,
  Star,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  formatCurrency,
  formatDateTime,
  getCmsSlug,
  getCmsSubtitle,
  getCmsTitle,
} from "../formatters";
import {
  useCmsRecord,
} from "../hooks";
import type {
  CmsContentType,
} from "../types";
import {
  ContentStatusBadge,
} from "./content-status-badge";

export function CmsDetailPanel({
  type,
  recordId,
  onClose,
}: {
  type: CmsContentType;
  recordId: string | null;
  onClose: () => void;
}) {
  const query = useCmsRecord(
    type,
    recordId,
  );

  if (!recordId) {
    return null;
  }

  const record = query.data;

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close content details"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-3xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              CMS content record
            </p>

            <h2 className="font-semibold text-slate-950 dark:text-white">
              {record
                ? getCmsTitle(record)
                : "Loading content"}
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            aria-label="Close content details"
          >
            <X size={18} />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {query.isLoading && (
            <div className="h-96 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
          )}

          {query.isError && (
            <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {query.error.message}
            </p>
          )}

          {record && (
            <div className="space-y-6">
              <section>
                <div className="flex flex-wrap gap-2">
                  <ContentStatusBadge
                    status={record.status}
                  />

                  {record.is_featured && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-700 dark:bg-amber-950/60 dark:text-amber-300">
                      <Star size={13} />
                      Featured
                    </span>
                  )}

                  {record.is_active && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2.5 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300">
                      <Eye size={13} />
                      Active
                    </span>
                  )}
                </div>

                <h3 className="mt-4 text-2xl font-bold text-slate-950 dark:text-white">
                  {getCmsTitle(record)}
                </h3>

                {getCmsSlug(record) && (
                  <p className="mt-2 flex items-center gap-2 text-sm text-slate-500">
                    <Link2 size={14} />
                    /{getCmsSlug(record)}
                  </p>
                )}

                {getCmsSubtitle(record) && (
                  <p className="mt-4 whitespace-pre-wrap text-sm leading-6 text-slate-600 dark:text-slate-300">
                    {getCmsSubtitle(record)}
                  </p>
                )}
              </section>

              <section className="grid gap-3 sm:grid-cols-2">
                <div className="flex items-center gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                  <CalendarClock
                    size={18}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500">
                      Published
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatDateTime(
                        record.published_at,
                      )}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                  <CalendarClock
                    size={18}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500">
                      Scheduled
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatDateTime(
                        record.scheduled_for,
                      )}
                    </p>
                  </div>
                </div>
              </section>

              {"price" in record && (
                <section className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Package pricing
                  </p>

                  <p className="mt-3 text-3xl font-bold text-slate-950 dark:text-white">
                    {formatCurrency(
                      record.price,
                      record.currency,
                    )}
                  </p>

                  <p className="mt-2 text-sm text-slate-500">
                    {record.pricing_type}
                    {record.billing_cycle
                      ? ` · ${record.billing_cycle}`
                      : ""}
                  </p>
                </section>
              )}

              {"rating" in record && (
                <section className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                  <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Testimonial
                  </p>

                  <p className="mt-3 text-lg font-semibold text-slate-950 dark:text-white">
                    {record.rating}/5
                  </p>

                  <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-600 dark:text-slate-300">
                    {record.content}
                  </p>

                  <p className="mt-4 text-sm font-medium text-slate-950 dark:text-white">
                    {record.author_name}
                  </p>

                  <p className="text-xs text-slate-500">
                    {record.author_position}
                    {record.company_name
                      ? ` · ${record.company_name}`
                      : ""}
                  </p>
                </section>
              )}

              <section className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-950 dark:text-white">
                  <FileText size={16} />
                  Record metadata
                </h4>

                <dl className="mt-4 grid gap-3 text-sm sm:grid-cols-2">
                  <div>
                    <dt className="text-slate-500">
                      Created
                    </dt>
                    <dd className="mt-1 font-medium text-slate-950 dark:text-white">
                      {formatDateTime(
                        record.created_at,
                      )}
                    </dd>
                  </div>

                  <div>
                    <dt className="text-slate-500">
                      Updated
                    </dt>
                    <dd className="mt-1 font-medium text-slate-950 dark:text-white">
                      {formatDateTime(
                        record.updated_at,
                      )}
                    </dd>
                  </div>

                  <div>
                    <dt className="text-slate-500">
                      Publicly available
                    </dt>
                    <dd className="mt-1 font-medium text-slate-950 dark:text-white">
                      {record.is_publicly_available
                        ? "Yes"
                        : "No"}
                    </dd>
                  </div>

                  <div>
                    <dt className="text-slate-500">
                      Record ID
                    </dt>
                    <dd className="mt-1 break-all font-mono text-xs text-slate-700 dark:text-slate-300">
                      {record.id}
                    </dd>
                  </div>
                </dl>
              </section>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
