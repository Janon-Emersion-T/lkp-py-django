import {
  ChevronRight,
} from "lucide-react";
import {
  useState,
} from "react";

import {
  formatCurrency,
  formatDate,
  isInvoiceOverdue,
} from "../formatters";
import {
  useFinanceInvoices,
} from "../hooks";
import {
  FinancePagination,
} from "./finance-pagination";
import {
  InvoiceStatusBadge,
} from "./finance-badges";
import {
  InvoiceDetailPanel,
} from "./invoice-detail-panel";

export function InvoicesWorkspace() {
  const [
    page,
    setPage,
  ] = useState(1);

  const [
    selectedInvoiceId,
    setSelectedInvoiceId,
  ] = useState<string | null>(null);

  const query = useFinanceInvoices({
    page,
    pageSize: 25,
  });

  return (
    <div className="space-y-4">
      {query.isLoading && (
        <div className="h-72 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
      )}

      {query.isError && (
        <p className="rounded-xl border border-red-200 bg-red-50 p-5 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
          {query.error.message}
        </p>
      )}

      {query.data && (
        <>
          <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
            <table className="w-full min-w-[950px]">
              <thead className="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500 dark:bg-slate-800/70">
                <tr>
                  <th className="px-5 py-3">
                    Invoice
                  </th>
                  <th className="px-5 py-3">
                    Client
                  </th>
                  <th className="px-5 py-3">
                    Status
                  </th>
                  <th className="px-5 py-3">
                    Due
                  </th>
                  <th className="px-5 py-3">
                    Total
                  </th>
                  <th className="px-5 py-3">
                    Balance
                  </th>
                  <th className="w-12 px-3 py-3" />
                </tr>
              </thead>

              <tbody>
                {query.data.items.map(
                  (invoice) => {
                    const overdue =
                      isInvoiceOverdue(
                        invoice.due_date,
                        invoice.status,
                      );

                    return (
                      <tr
                        key={invoice.id}
                        className="border-t border-slate-200 dark:border-slate-800"
                      >
                        <td className="px-5 py-4">
                          <button
                            type="button"
                            onClick={() => {
                              setSelectedInvoiceId(
                                invoice.id,
                              );
                            }}
                            className="text-left"
                          >
                            <p className="font-medium text-slate-950 hover:text-blue-700 dark:text-white">
                              {
                                invoice.invoice_number
                              }
                            </p>

                            <p className="mt-1 text-xs text-slate-500">
                              {formatDate(
                                invoice.issue_date,
                              )}
                            </p>
                          </button>
                        </td>

                        <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                          {invoice.client_name}
                        </td>

                        <td className="px-5 py-4">
                          <InvoiceStatusBadge
                            status={
                              invoice.status
                            }
                          />
                        </td>

                        <td
                          className={
                            overdue
                              ? "px-5 py-4 text-sm font-semibold text-red-700 dark:text-red-400"
                              : "px-5 py-4 text-sm text-slate-600 dark:text-slate-300"
                          }
                        >
                          {formatDate(
                            invoice.due_date,
                          )}
                        </td>

                        <td className="px-5 py-4 font-semibold text-slate-950 dark:text-white">
                          {formatCurrency(
                            invoice.total_amount,
                            invoice.currency,
                          )}
                        </td>

                        <td className="px-5 py-4 font-semibold text-slate-950 dark:text-white">
                          {formatCurrency(
                            invoice.balance_due,
                            invoice.currency,
                          )}
                        </td>

                        <td className="px-3 py-4">
                          <button
                            type="button"
                            onClick={() => {
                              setSelectedInvoiceId(
                                invoice.id,
                              );
                            }}
                            aria-label="View invoice"
                          >
                            <ChevronRight
                              size={17}
                              className="text-slate-400"
                            />
                          </button>
                        </td>
                      </tr>
                    );
                  },
                )}
              </tbody>
            </table>
          </div>

          <FinancePagination
            pagination={
              query.data.pagination
            }
            onPageChange={setPage}
          />
        </>
      )}

      <InvoiceDetailPanel
        invoiceId={selectedInvoiceId}
        onClose={() => {
          setSelectedInvoiceId(null);
        }}
      />
    </div>
  );
}
