import {
  cn,
} from "../../../lib/utils";
import {
  accountTypeLabels,
  expenseStatusLabels,
  invoiceStatusLabels,
  paymentStatusLabels,
  transactionTypeLabels,
} from "../formatters";
import type {
  AccountType,
  ExpenseStatus,
  InvoiceStatus,
  PaymentStatus,
  TransactionType,
} from "../types";

const neutral =
  "bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-300";

const positive =
  "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300";

const warning =
  "bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300";

const danger =
  "bg-red-50 text-red-700 dark:bg-red-950/60 dark:text-red-300";

const info =
  "bg-blue-50 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300";

function Badge({
  label,
  className,
}: {
  label: string;
  className: string;
}) {
  return (
    <span
      className={cn(
        "inline-flex rounded-full px-2.5 py-1 text-xs font-semibold",
        className,
      )}
    >
      {label}
    </span>
  );
}

export function AccountTypeBadge({
  type,
}: {
  type: AccountType;
}) {
  const classes: Record<
    AccountType,
    string
  > = {
    asset: info,
    liability: warning,
    equity: neutral,
    income: positive,
    expense: danger,
  };

  return (
    <Badge
      label={accountTypeLabels[type]}
      className={classes[type]}
    />
  );
}

export function TransactionTypeBadge({
  type,
}: {
  type: TransactionType;
}) {
  const classes: Record<
    TransactionType,
    string
  > = {
    income: positive,
    expense: danger,
    transfer: info,
    adjustment: warning,
  };

  return (
    <Badge
      label={transactionTypeLabels[type]}
      className={classes[type]}
    />
  );
}

export function InvoiceStatusBadge({
  status,
}: {
  status: InvoiceStatus;
}) {
  const classes: Record<
    InvoiceStatus,
    string
  > = {
    draft: neutral,
    sent: info,
    partially_paid: warning,
    paid: positive,
    overdue: danger,
    cancelled: neutral,
  };

  return (
    <Badge
      label={invoiceStatusLabels[status]}
      className={classes[status]}
    />
  );
}

export function PaymentStatusBadge({
  status,
}: {
  status: PaymentStatus;
}) {
  const classes: Record<
    PaymentStatus,
    string
  > = {
    pending: warning,
    completed: positive,
    failed: danger,
    refunded: info,
    voided: neutral,
  };

  return (
    <Badge
      label={paymentStatusLabels[status]}
      className={classes[status]}
    />
  );
}

export function ExpenseStatusBadge({
  status,
}: {
  status: ExpenseStatus;
}) {
  const classes: Record<
    ExpenseStatus,
    string
  > = {
    draft: neutral,
    approved: info,
    paid: positive,
    rejected: danger,
    voided: neutral,
  };

  return (
    <Badge
      label={expenseStatusLabels[status]}
      className={classes[status]}
    />
  );
}
