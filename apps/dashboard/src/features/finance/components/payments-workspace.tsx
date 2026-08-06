import {
  useState,
} from "react";

import {
  formatCurrency,
  formatDate,
  paymentMethodLabels,
} from "../formatters";
import {
  useFinancePayments,
} from "../hooks";
import {
  FinancePagination,
} from "./finance-pagination";
import {
  PaymentStatusBadge,
} from "./finance-badges";

export function PaymentsWorkspace() {
  const [
    page,
    setPage,
  ] = useState(1);

  const query = useFinancePayments({
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
          <div className="grid gap-3">
            {query.data.items.map(
              (payment) => (
                <article
                  key={payment.id}
                  className="rounded-xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900"
                >
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <p className="font-semibold text-slate-950 dark:text-white">
                          {payment.payment_number}
                        </p>

                        <PaymentStatusBadge
                          status={payment.status}
                        />
                      </div>

                      <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">
                        {
                          paymentMethodLabels[
                            payment.method
                          ]
                        }
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        {formatDate(
                          payment.payment_date,
                        )}
                        {payment.reference
                          ? ` · ${payment.reference}`
                          : ""}
                      </p>
                    </div>

                    <p className="text-xl font-bold text-emerald-700 sm:ml-auto dark:text-emerald-400">
                      {formatCurrency(
                        payment.amount,
                        payment.currency,
                      )}
                    </p>
                  </div>
                </article>
              ),
            )}
          </div>

          <FinancePagination
            pagination={
              query.data.pagination
            }
            onPageChange={setPage}
          />
        </>
      )}
    </div>
  );
}
