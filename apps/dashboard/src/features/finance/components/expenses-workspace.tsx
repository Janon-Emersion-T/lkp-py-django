import {
  useState,
} from "react";

import {
  expenseCategoryLabels,
  formatCurrency,
  formatDate,
} from "../formatters";
import {
  useFinanceExpenses,
} from "../hooks";
import {
  ExpenseStatusBadge,
} from "./finance-badges";
import {
  FinancePagination,
} from "./finance-pagination";

export function ExpensesWorkspace() {
  const [
    page,
    setPage,
  ] = useState(1);

  const query = useFinanceExpenses({
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
            <table className="w-full min-w-[900px]">
              <thead className="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500 dark:bg-slate-800/70">
                <tr>
                  <th className="px-5 py-3">
                    Expense
                  </th>
                  <th className="px-5 py-3">
                    Category
                  </th>
                  <th className="px-5 py-3">
                    Vendor
                  </th>
                  <th className="px-5 py-3">
                    Status
                  </th>
                  <th className="px-5 py-3">
                    Date
                  </th>
                  <th className="px-5 py-3">
                    Amount
                  </th>
                </tr>
              </thead>

              <tbody>
                {query.data.items.map(
                  (expense) => (
                    <tr
                      key={expense.id}
                      className="border-t border-slate-200 dark:border-slate-800"
                    >
                      <td className="px-5 py-4">
                        <p className="font-medium text-slate-950 dark:text-white">
                          {expense.description}
                        </p>

                        <p className="mt-1 text-xs text-slate-500">
                          {expense.expense_number}
                        </p>
                      </td>

                      <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                        {
                          expenseCategoryLabels[
                            expense.category
                          ]
                        }
                      </td>

                      <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                        {expense.vendor
                          || "Not specified"}
                      </td>

                      <td className="px-5 py-4">
                        <ExpenseStatusBadge
                          status={
                            expense.status
                          }
                        />
                      </td>

                      <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                        {formatDate(
                          expense.expense_date,
                        )}
                      </td>

                      <td className="px-5 py-4 font-semibold text-red-700 dark:text-red-400">
                        {formatCurrency(
                          expense.amount,
                          expense.currency,
                        )}
                      </td>
                    </tr>
                  ),
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
    </div>
  );
}
