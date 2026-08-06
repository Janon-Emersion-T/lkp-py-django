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
  accountTypeLabels,
  formatCurrency,
} from "../formatters";
import {
  useFinanceAccounts,
} from "../hooks";
import {
  accountTypes,
  type AccountFilters,
  type AccountType,
} from "../types";
import {
  AccountTypeBadge,
} from "./finance-badges";
import {
  FinancePagination,
} from "./finance-pagination";

const initialFilters: AccountFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  accountType: "",
  isActive: null,
  ordering: "account_code",
};

export function AccountsWorkspace() {
  const [
    filters,
    setFilters,
  ] = useState(initialFilters);

  const deferredSearch =
    useDeferredValue(filters.search);

  const query = useFinanceAccounts({
    ...filters,
    search: deferredSearch,
  });

  return (
    <div className="space-y-4">
      <div className="grid gap-3 rounded-xl border border-slate-200 bg-white p-4 md:grid-cols-3 dark:border-slate-800 dark:bg-slate-900">
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
            placeholder="Search account code or name"
            className="pl-9 dark:border-slate-700 dark:bg-slate-950"
          />
        </label>

        <select
          value={filters.accountType}
          onChange={(event) => {
            setFilters((current) => ({
              ...current,
              page: 1,
              accountType:
                event.target.value as
                  | AccountType
                  | "",
            }));
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All account types
          </option>

          {accountTypes.map((type) => (
            <option
              key={type}
              value={type}
            >
              {accountTypeLabels[type]}
            </option>
          ))}
        </select>

        <select
          value={
            filters.isActive === null
              ? ""
              : String(filters.isActive)
          }
          onChange={(event) => {
            setFilters((current) => ({
              ...current,
              page: 1,
              isActive:
                event.target.value === ""
                  ? null
                  : event.target.value
                    === "true",
            }));
          }}
          className="h-10 rounded-md border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          <option value="">
            All account states
          </option>
          <option value="true">
            Active
          </option>
          <option value="false">
            Inactive
          </option>
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
          <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
            <table className="w-full min-w-[850px]">
              <thead className="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500 dark:bg-slate-800/70 dark:text-slate-400">
                <tr>
                  <th className="px-5 py-3">
                    Account
                  </th>
                  <th className="px-5 py-3">
                    Type
                  </th>
                  <th className="px-5 py-3">
                    Opening balance
                  </th>
                  <th className="px-5 py-3">
                    Current balance
                  </th>
                  <th className="px-5 py-3">
                    State
                  </th>
                </tr>
              </thead>

              <tbody>
                {query.data.items.map(
                  (account) => (
                    <tr
                      key={account.id}
                      className="border-t border-slate-200 dark:border-slate-800"
                    >
                      <td className="px-5 py-4">
                        <p className="font-medium text-slate-950 dark:text-white">
                          {account.name}
                        </p>

                        <p className="mt-1 text-xs text-slate-500">
                          {account.account_code}
                          {account.is_system
                            ? " · System"
                            : ""}
                        </p>
                      </td>

                      <td className="px-5 py-4">
                        <AccountTypeBadge
                          type={
                            account.account_type
                          }
                        />
                      </td>

                      <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                        {formatCurrency(
                          account.opening_balance,
                          account.currency,
                        )}
                      </td>

                      <td className="px-5 py-4 font-semibold text-slate-950 dark:text-white">
                        {formatCurrency(
                          account.current_balance,
                          account.currency,
                        )}
                      </td>

                      <td className="px-5 py-4 text-sm">
                        {account.is_active
                          ? "Active"
                          : "Inactive"}
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
