import {
  BookOpen,
  Building2,
  CircleDollarSign,
  CreditCard,
  FileText,
  Receipt,
  RefreshCw,
} from "lucide-react";
import {
  useState,
} from "react";
import {
  useQueryClient,
} from "@tanstack/react-query";

import {
  PageHeader,
} from "../../../components/layout/page-header";
import {
  Button,
} from "../../../components/ui/button";
import {
  AccountsWorkspace,
} from "../components/accounts-workspace";
import {
  ExpensesWorkspace,
} from "../components/expenses-workspace";
import {
  FinanceOverview,
} from "../components/finance-overview";
import {
  InvoicesWorkspace,
} from "../components/invoices-workspace";
import {
  PaymentsWorkspace,
} from "../components/payments-workspace";
import {
  TransactionsWorkspace,
} from "../components/transactions-workspace";
import {
  financeQueryKeys,
} from "../hooks";
import type {
  FinanceSection,
} from "../types";

const sections: Array<{
  id: FinanceSection;
  label: string;
  icon: typeof CircleDollarSign;
}> = [
  {
    id: "overview",
    label: "Overview",
    icon: CircleDollarSign,
  },
  {
    id: "accounts",
    label: "Accounts",
    icon: Building2,
  },
  {
    id: "transactions",
    label: "Transactions",
    icon: BookOpen,
  },
  {
    id: "invoices",
    label: "Invoices",
    icon: FileText,
  },
  {
    id: "payments",
    label: "Payments",
    icon: CreditCard,
  },
  {
    id: "expenses",
    label: "Expenses",
    icon: Receipt,
  },
];

export function FinancePage() {
  const [
    section,
    setSection,
  ] = useState<FinanceSection>(
    "overview",
  );

  const queryClient = useQueryClient();

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Financial operations"
          title="Finance"
          description="Review financial position, chart of accounts, double-entry transactions, invoices, customer payments, expenses, receivables, and profitability."
        />

        <Button
          variant="outline"
          onClick={() => {
            void queryClient.invalidateQueries({
              queryKey:
                financeQueryKeys.all,
            });
          }}
          className="self-start dark:border-slate-700 dark:text-slate-200"
        >
          <RefreshCw size={16} />
          Refresh finance
        </Button>
      </div>

      <nav className="overflow-x-auto rounded-xl border border-slate-200 bg-white p-2 dark:border-slate-800 dark:bg-slate-900">
        <div className="flex min-w-max gap-1">
          {sections.map((item) => {
            const Icon = item.icon;
            const active =
              item.id === section;

            return (
              <button
                key={item.id}
                type="button"
                onClick={() => {
                  setSection(item.id);
                }}
                className={
                  active
                    ? "flex items-center gap-2 rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white dark:bg-white dark:text-slate-950"
                    : "flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium text-slate-600 transition hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
                }
              >
                <Icon size={16} />
                {item.label}
              </button>
            );
          })}
        </div>
      </nav>

      {section === "overview" && (
        <FinanceOverview />
      )}

      {section === "accounts" && (
        <AccountsWorkspace />
      )}

      {section === "transactions" && (
        <TransactionsWorkspace />
      )}

      {section === "invoices" && (
        <InvoicesWorkspace />
      )}

      {section === "payments" && (
        <PaymentsWorkspace />
      )}

      {section === "expenses" && (
        <ExpensesWorkspace />
      )}
    </section>
  );
}
