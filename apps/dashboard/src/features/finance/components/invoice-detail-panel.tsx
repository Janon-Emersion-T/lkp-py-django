import {
  Building2,
  CalendarDays,
  ReceiptText,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  formatCurrency,
  formatDate,
  formatDateTime,
} from "../formatters";
import {
  useFinanceInvoice,
} from "../hooks";
import {
  InvoiceStatusBadge,
} from "./finance-badges";

export function InvoiceDetailPanel({
  invoiceId,
  onClose,
}: {
  invoiceId: string | null;
  onClose: () => void;
}) {
  const query =
    useFinanceInvoice(invoiceId);

  if (!invoiceId) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close invoice"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-2xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Invoice record
            </p>

            <h2 className="font-semibold text-slate-950 dark:text-white">
              {query.data?.invoice_number
                ?? "Loading invoice"}
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
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

          {query.data && (
            <div className="space-y-6">
              <section>
                <InvoiceStatusBadge
                  status={query.data.status}
                />

                <h3 className="mt-4 text-2xl font-bold text-slate-950 dark:text-white">
                  {query.data.invoice_number}
                </h3>

                <p className="mt-3 text-3xl font-bold text-slate-950 dark:text-white">
                  {formatCurrency(
                    query.data.total_amount,
                    query.data.currency,
                  )}
                </p>
              </section>

              <section className="grid gap-3 sm:grid-cols-2">
                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <Building2
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500">
                      Client
                    </p>

                    <p className="font-medium text-slate-950 dark:text-white">
                      {query.data.client_name}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <CalendarDays
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500">
                      Issue / due
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatDate(
                        query.data.issue_date,
                      )}
                      {" — "}
                      {formatDate(
                        query.data.due_date,
                      )}
                    </p>
                  </div>
                </div>
              </section>

              <section>
                <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                  Invoice items
                </h4>

                <div className="mt-3 space-y-3">
                  {query.data.items.map(
                    (item) => (
                      <article
                        key={item.id}
                        className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                      >
                        <div className="flex justify-between gap-4">
                          <div>
                            <p className="font-medium text-slate-950 dark:text-white">
                              {item.title}
                            </p>

                            <p className="mt-1 text-xs text-slate-500">
                              {item.quantity} ×{" "}
                              {formatCurrency(
                                item.unit_price,
                                query.data.currency,
                              )}
                            </p>
                          </div>

                          <p className="font-semibold text-slate-950 dark:text-white">
                            {formatCurrency(
                              item.total_amount,
                              query.data.currency,
                            )}
                          </p>
                        </div>
                      </article>
                    ),
                  )}
                </div>
              </section>

              <section className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                <h4 className="flex items-center gap-2 font-semibold text-slate-950 dark:text-white">
                  <ReceiptText size={16} />
                  Financial summary
                </h4>

                <dl className="mt-4 space-y-3 text-sm">
                  {[
                    [
                      "Subtotal",
                      query.data.subtotal,
                    ],
                    [
                      "Discount",
                      query.data.discount_amount,
                    ],
                    [
                      "Tax",
                      query.data.tax_amount,
                    ],
                    [
                      "Paid",
                      query.data.paid_amount,
                    ],
                    [
                      "Balance due",
                      query.data.balance_due,
                    ],
                  ].map(([label, value]) => (
                    <div
                      key={label}
                      className="flex justify-between gap-4"
                    >
                      <dt className="text-slate-500">
                        {label}
                      </dt>

                      <dd className="font-medium text-slate-950 dark:text-white">
                        {formatCurrency(
                          value,
                          query.data.currency,
                        )}
                      </dd>
                    </div>
                  ))}
                </dl>
              </section>

              <p className="text-xs text-slate-500">
                Sent:{" "}
                {formatDateTime(
                  query.data.sent_at,
                )}
                {" · Paid: "}
                {formatDateTime(
                  query.data.paid_at,
                )}
              </p>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
