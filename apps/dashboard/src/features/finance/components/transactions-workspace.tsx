import {
  Search,
} from "lucide-react";
import {
  useDeferredValue,
  useState,
} from "react";

import {
  Input,
} from "../../../components/ui/input";
import {
  formatCurrency,
  formatDate,
  transactionTypeLabels,
} from "../formatters";
import {
  useFinanceTransactions,
} from "../hooks";
import {
  transactionTypes,
  type TransactionFilters,
  type TransactionType,
} from "../types";
import {
  FinancePagination,
} from "./finance-pagination";
import {
  TransactionTypeBadge,
} from "./finance-badges";

const initialFilters: TransactionFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  transactionType: "",
  ordering: "-transaction_date",
};

export function TransactionsWorkspace() {
  const [
    filters,
    setFilters,
  ] = useState(initialFilters);

  const deferredSearch =
    useDeferredValue(filters.search);

  const query = useFinanceTransactions({
    ...filters,
    search: deferredSearch,
  });

  return (
    <div className="space-y-4">
      <div className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 md:grid-cols-2 dark:border-slate-800 dark:bg-slate-900">
        <label className="relative">
          <Search
            size={16}
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
          />

          <Input
            value={filters.search}
            onChange={(event) => {
              setFilters((current) => ({
                ...current,
                page: 1,
                search: event.target.value,
              }));
            }}
            placeholder="Search number, description or reference"
            className="pl-9 dark:border-slate-700 dark:bg-slate-950"
          />
        </label>

        <select
          value={filters.transactionType}
          onChange={(event) => {
            setFilters((current) => ({
              ...current,
              page: 1,
              transactionType:
                event.target.value as
                  | TransactionType
                  | "",
            }));
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All transaction types
          </option>

          {transactionTypes.map(
            (type) => (
              <option
                key={type}
                value={type}
              >
                {
                  transactionTypeLabels[
                    type
                  ]
                }
              </option>
            ),
          )}
        </select>
      </div>

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
          <div className="space-y-3">
            {query.data.items.map(
              (transaction) => (
                <article
                  key={transaction.id}
                  className="rounded-xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900"
                >
                  <div className="flex flex-col gap-3 sm:flex-row sm:items-start">
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <p className="font-semibold text-slate-950 dark:text-white">
                          {
                            transaction.transaction_number
                          }
                        </p>

                        <TransactionTypeBadge
                          type={
                            transaction.transaction_type
                          }
                        />
                      </div>

                      <p className="mt-2 text-sm text-slate-600 dark:text-slate-300">
                        {transaction.description}
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        {formatDate(
                          transaction.transaction_date,
                        )}
                        {transaction.reference
                          ? ` · ${transaction.reference}`
                          : ""}
                      </p>
                    </div>

                    <p className="text-xl font-bold text-slate-950 sm:ml-auto dark:text-white">
                      {formatCurrency(
                        transaction.total_amount,
                      )}
                    </p>
                  </div>

                  <div className="mt-4 overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-700">
                    <table className="w-full min-w-[650px] text-sm">
                      <thead className="bg-slate-50 text-left text-xs text-slate-500 dark:bg-slate-800">
                        <tr>
                          <th className="px-3 py-2">
                            Ledger account
                          </th>
                          <th className="px-3 py-2 text-right">
                            Debit
                          </th>
                          <th className="px-3 py-2 text-right">
                            Credit
                          </th>
                        </tr>
                      </thead>

                      <tbody>
                        {transaction.entries.map(
                          (entry) => (
                            <tr
                              key={entry.id}
                              className="border-t border-slate-200 dark:border-slate-700"
                            >
                              <td className="px-3 py-2">
                                <p className="font-medium text-slate-800 dark:text-slate-200">
                                  {
                                    entry.account_name
                                  }
                                </p>

                                <p className="text-xs text-slate-500">
                                  {
                                    entry.account_code
                                  }
                                </p>
                              </td>

                              <td className="px-3 py-2 text-right">
                                {formatCurrency(
                                  entry.debit,
                                )}
                              </td>

                              <td className="px-3 py-2 text-right">
                                {formatCurrency(
                                  entry.credit,
                                )}
                              </td>
                            </tr>
                          ),
                        )}
                      </tbody>
                    </table>
                  </div>
                </article>
              ),
            )}
          </div>

          <FinancePagination
            pagination={
              query.data.pagination
            }
            onPageChange={(page) => {
              setFilters((current) => ({
                ...current,
                page,
              }));
            }}
          />
        </>
      )}
    </div>
  );
}
