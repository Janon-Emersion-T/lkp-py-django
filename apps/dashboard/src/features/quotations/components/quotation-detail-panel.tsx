import {
  Building2,
  CalendarDays,
  CheckCircle2,
  Clock3,
  Copy,
  FileText,
  Mail,
  ReceiptText,
  Send,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  formatCurrency,
  formatDate,
  formatDateTime,
  formatQuantity,
} from "../formatters";
import {
  useQuotation,
} from "../hooks";
import {
  QuotationStatusBadge,
} from "./quotation-status-badge";

interface QuotationDetailPanelProps {
  quotationId: string | null;
  onClose: () => void;
}

export function QuotationDetailPanel({
  quotationId,
  onClose,
}: QuotationDetailPanelProps) {
  const quotationQuery =
    useQuotation(quotationId);

  const quotation =
    quotationQuery.data;

  if (!quotationId) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close quotation details"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-3xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Quotation record
            </p>

            <h2 className="mt-0.5 font-semibold text-slate-950 dark:text-white">
              {quotation?.quotation_number
                ?? "Loading quotation"}
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            aria-label="Close quotation details"
            className="dark:text-slate-300"
          >
            <X size={19} />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {quotationQuery.isLoading && (
            <div className="space-y-4">
              {Array.from({
                length: 8,
              }).map((_, index) => (
                <div
                  key={index}
                  className="h-16 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800"
                />
              ))}
            </div>
          )}

          {quotationQuery.isError && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {quotationQuery.error
                instanceof Error
                ? quotationQuery.error.message
                : "Quotation details could not be loaded."}
            </div>
          )}

          {quotation && (
            <div className="space-y-6">
              <section>
                <div className="flex flex-wrap items-center gap-2">
                  <QuotationStatusBadge
                    status={
                      quotation.status
                    }
                  />

                  {quotation.is_expired
                    && quotation.status
                      !== "expired" && (
                      <span className="rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-700 dark:bg-amber-950/60 dark:text-amber-300">
                        Past expiry date
                      </span>
                    )}

                  {quotation.duplicated_from_id && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold text-violet-700 dark:bg-violet-950/60 dark:text-violet-300">
                      <Copy size={13} />
                      Duplicate
                    </span>
                  )}
                </div>

                <h3 className="mt-4 text-2xl font-bold text-slate-950 dark:text-white">
                  {quotation.title}
                </h3>

                {quotation.subject && (
                  <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                    {quotation.subject}
                  </p>
                )}

                <p className="mt-4 text-3xl font-bold tracking-tight text-slate-950 dark:text-white">
                  {formatCurrency(
                    quotation.total_amount,
                    quotation.currency,
                  )}
                </p>
              </section>

              <section className="grid gap-3 sm:grid-cols-2">
                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <Building2
                    size={17}
                    className="text-slate-400"
                  />

                  <div className="min-w-0">
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Client
                    </p>

                    <p className="truncate text-sm font-medium text-slate-950 dark:text-white">
                      {quotation.client_name}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <CalendarDays
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Issue date
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatDate(
                        quotation.issue_date,
                      )}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <Clock3
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Expiry date
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatDate(
                        quotation.expiry_date,
                      )}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <Send
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Sent
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatDateTime(
                        quotation.sent_at,
                      )}
                    </p>
                  </div>
                </div>
              </section>

              {quotation.description && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Description
                  </h4>

                  <p className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-600 dark:bg-slate-800/70 dark:text-slate-300">
                    {quotation.description}
                  </p>
                </section>
              )}

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Line items
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {quotation.items.length}
                  </span>
                </div>

                {quotation.items.length === 0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No quotation items recorded
                  </p>
                ) : (
                  <div className="mt-3 overflow-hidden rounded-xl border border-slate-200 dark:border-slate-700">
                    {quotation.items.map(
                      (item) => (
                        <article
                          key={item.id}
                          className="border-b border-slate-200 p-4 last:border-b-0 dark:border-slate-700"
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="min-w-0">
                              <p className="font-medium text-slate-950 dark:text-white">
                                {item.title}
                              </p>

                              {item.description && (
                                <p className="mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">
                                  {
                                    item.description
                                  }
                                </p>
                              )}
                            </div>

                            <p className="shrink-0 text-sm font-semibold text-slate-950 dark:text-white">
                              {formatCurrency(
                                item.total_amount,
                                quotation.currency,
                              )}
                            </p>
                          </div>

                          <div className="mt-3 flex flex-wrap gap-x-5 gap-y-1 text-xs text-slate-500 dark:text-slate-400">
                            <span>
                              Qty{" "}
                              {formatQuantity(
                                item.quantity,
                              )}
                            </span>

                            <span>
                              Unit{" "}
                              {formatCurrency(
                                item.unit_price,
                                quotation.currency,
                              )}
                            </span>

                            <span>
                              Tax {item.tax_rate}%
                            </span>

                            {Number(
                              item.discount_amount,
                            ) > 0 && (
                              <span>
                                Discount{" "}
                                {formatCurrency(
                                  item.discount_amount,
                                  quotation.currency,
                                )}
                              </span>
                            )}
                          </div>
                        </article>
                      ),
                    )}
                  </div>
                )}
              </section>

              <section className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-950 dark:text-white">
                  <ReceiptText size={16} />
                  Financial summary
                </h4>

                <dl className="mt-4 space-y-3">
                  <div className="flex justify-between gap-4 text-sm">
                    <dt className="text-slate-500 dark:text-slate-400">
                      Subtotal
                    </dt>

                    <dd className="font-medium text-slate-950 dark:text-white">
                      {formatCurrency(
                        quotation.subtotal,
                        quotation.currency,
                      )}
                    </dd>
                  </div>

                  <div className="flex justify-between gap-4 text-sm">
                    <dt className="text-slate-500 dark:text-slate-400">
                      Discount
                    </dt>

                    <dd className="font-medium text-slate-950 dark:text-white">
                      -{" "}
                      {formatCurrency(
                        quotation.discount_amount,
                        quotation.currency,
                      )}
                    </dd>
                  </div>

                  <div className="flex justify-between gap-4 text-sm">
                    <dt className="text-slate-500 dark:text-slate-400">
                      Tax
                    </dt>

                    <dd className="font-medium text-slate-950 dark:text-white">
                      {formatCurrency(
                        quotation.tax_amount,
                        quotation.currency,
                      )}
                    </dd>
                  </div>

                  <div className="flex justify-between gap-4 border-t border-slate-200 pt-3 dark:border-slate-700">
                    <dt className="font-semibold text-slate-950 dark:text-white">
                      Total
                    </dt>

                    <dd className="text-lg font-bold text-slate-950 dark:text-white">
                      {formatCurrency(
                        quotation.total_amount,
                        quotation.currency,
                      )}
                    </dd>
                  </div>
                </dl>
              </section>

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Recipients
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {
                      quotation.recipients
                        .length
                    }
                  </span>
                </div>

                {quotation.recipients.length ===
                0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No recipients recorded
                  </p>
                ) : (
                  <div className="mt-3 space-y-3">
                    {quotation.recipients.map(
                      (recipient) => (
                        <article
                          key={recipient.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <div className="flex items-start gap-3">
                            <Mail
                              size={17}
                              className="mt-0.5 shrink-0 text-slate-400"
                            />

                            <div className="min-w-0 flex-1">
                              <div className="flex flex-wrap items-center gap-2">
                                <p className="font-medium text-slate-950 dark:text-white">
                                  {recipient.name
                                    || recipient.email}
                                </p>

                                {recipient.is_primary && (
                                  <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700 dark:bg-blue-950/60 dark:text-blue-300">
                                    Primary
                                  </span>
                                )}
                              </div>

                              <a
                                href={`mailto:${recipient.email}`}
                                className="mt-1 block truncate text-sm text-blue-700 hover:underline dark:text-blue-400"
                              >
                                {recipient.email}
                              </a>

                              <div className="mt-2 flex flex-wrap gap-3 text-xs text-slate-500 dark:text-slate-400">
                                <span>
                                  Received:{" "}
                                  {formatDateTime(
                                    recipient.received_at,
                                  )}
                                </span>

                                <span>
                                  Viewed:{" "}
                                  {formatDateTime(
                                    recipient.viewed_at,
                                  )}
                                </span>
                              </div>
                            </div>
                          </div>
                        </article>
                      ),
                    )}
                  </div>
                )}
              </section>

              {quotation.accepted_at && (
                <section className="rounded-xl border border-emerald-200 bg-emerald-50 p-4 dark:border-emerald-900 dark:bg-emerald-950/30">
                  <h4 className="flex items-center gap-2 text-sm font-semibold text-emerald-900 dark:text-emerald-200">
                    <CheckCircle2 size={17} />
                    Acceptance record
                  </h4>

                  <p className="mt-2 text-sm text-emerald-800 dark:text-emerald-300">
                    Accepted by{" "}
                    <strong>
                      {
                        quotation.accepted_by_name
                      }
                    </strong>{" "}
                    ({quotation.accepted_by_email})
                    on{" "}
                    {formatDateTime(
                      quotation.accepted_at,
                    )}.
                  </p>
                </section>
              )}

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Activity timeline
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {quotation.events.length}
                  </span>
                </div>

                {quotation.events.length === 0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No quotation events recorded
                  </p>
                ) : (
                  <div className="mt-3 space-y-3">
                    {quotation.events.map(
                      (event) => (
                        <article
                          key={event.id}
                          className="flex gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                            <FileText
                              size={15}
                            />
                          </span>

                          <div className="min-w-0">
                            <p className="text-sm font-medium text-slate-950 dark:text-white">
                              {
                                event.description
                              }
                            </p>

                            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                              {event.event_type}
                              {" · "}
                              {formatDateTime(
                                event.created_at,
                              )}
                            </p>
                          </div>
                        </article>
                      ),
                    )}
                  </div>
                )}
              </section>

              {(quotation.terms
                || quotation.notes) && (
                <section className="grid gap-4 sm:grid-cols-2">
                  {quotation.terms && (
                    <div>
                      <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                        Terms
                      </h4>

                      <p className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-600 dark:bg-slate-800/70 dark:text-slate-300">
                        {quotation.terms}
                      </p>
                    </div>
                  )}

                  {quotation.notes && (
                    <div>
                      <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                        Notes
                      </h4>

                      <p className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-600 dark:bg-slate-800/70 dark:text-slate-300">
                        {quotation.notes}
                      </p>
                    </div>
                  )}
                </section>
              )}

              <section className="border-t border-slate-200 pt-4 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
                <p>
                  Created{" "}
                  {formatDateTime(
                    quotation.created_at,
                  )}
                </p>

                <p className="mt-1">
                  Updated{" "}
                  {formatDateTime(
                    quotation.updated_at,
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
