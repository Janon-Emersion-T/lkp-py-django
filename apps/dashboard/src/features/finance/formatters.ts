import type {
  AccountType,
  ExpenseCategory,
  ExpenseStatus,
  InvoiceStatus,
  PaymentMethod,
  PaymentStatus,
  TransactionType,
} from "./types";

export const accountTypeLabels: Record<
  AccountType,
  string
> = {
  asset: "Asset",
  liability: "Liability",
  equity: "Equity",
  income: "Income",
  expense: "Expense",
};

export const transactionTypeLabels: Record<
  TransactionType,
  string
> = {
  income: "Income",
  expense: "Expense",
  transfer: "Transfer",
  adjustment: "Adjustment",
};

export const invoiceStatusLabels: Record<
  InvoiceStatus,
  string
> = {
  draft: "Draft",
  sent: "Sent",
  partially_paid: "Partially Paid",
  paid: "Paid",
  overdue: "Overdue",
  cancelled: "Cancelled",
};

export const paymentMethodLabels: Record<
  PaymentMethod,
  string
> = {
  cash: "Cash",
  bank_transfer: "Bank Transfer",
  card: "Card",
  paypal: "PayPal",
  stripe: "Stripe",
  crypto: "Cryptocurrency",
  other: "Other",
};

export const paymentStatusLabels: Record<
  PaymentStatus,
  string
> = {
  pending: "Pending",
  completed: "Completed",
  failed: "Failed",
  refunded: "Refunded",
  voided: "Voided",
};

export const expenseCategoryLabels: Record<
  ExpenseCategory,
  string
> = {
  hosting: "Hosting",
  office: "Office",
  salary: "Salary",
  marketing: "Marketing",
  software: "Software",
  equipment: "Equipment",
  miscellaneous: "Miscellaneous",
};

export const expenseStatusLabels: Record<
  ExpenseStatus,
  string
> = {
  draft: "Draft",
  approved: "Approved",
  paid: "Paid",
  rejected: "Rejected",
  voided: "Voided",
};

export function formatCurrency(
  value: string,
  currency = "LKR",
): string {
  const amount = Number(value);

  if (!Number.isFinite(amount)) {
    return `${currency} ${value}`;
  }

  try {
    return new Intl.NumberFormat(
      "en-GB",
      {
        style: "currency",
        currency,
        maximumFractionDigits: 2,
      },
    ).format(amount);
  } catch {
    return `${currency} ${amount.toLocaleString(
      "en-GB",
      {
        maximumFractionDigits: 2,
      },
    )}`;
  }
}

export function formatDate(
  value: string | null,
): string {
  if (!value) {
    return "Not set";
  }

  const date = new Date(
    value.includes("T")
      ? value
      : `${value}T00:00:00`,
  );

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(
    "en-GB",
    {
      dateStyle: "medium",
    },
  ).format(date);
}

export function formatDateTime(
  value: string | null,
): string {
  if (!value) {
    return "Not recorded";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(
    "en-GB",
    {
      dateStyle: "medium",
      timeStyle: "short",
    },
  ).format(date);
}

export function isInvoiceOverdue(
  dueDate: string | null,
  status: InvoiceStatus,
): boolean {
  if (
    !dueDate
    || status === "paid"
    || status === "cancelled"
  ) {
    return false;
  }

  const date = new Date(
    `${dueDate}T23:59:59`,
  );

  return (
    !Number.isNaN(date.getTime())
    && date.getTime() < Date.now()
  );
}
