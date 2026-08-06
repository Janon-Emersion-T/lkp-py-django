import type {
  QuotationStatus,
} from "./types";

export const quotationStatusLabels: Record<
  QuotationStatus,
  string
> = {
  draft: "Draft",
  sent: "Sent",
  viewed: "Viewed",
  accepted: "Accepted",
  rejected: "Rejected",
  expired: "Expired",
  cancelled: "Cancelled",
};

export function formatCount(
  value: number,
): string {
  return new Intl.NumberFormat(
    "en-GB",
  ).format(value);
}

export function formatCurrency(
  value: string,
  currency: string,
): string {
  const amount = Number(value);

  if (!Number.isFinite(amount)) {
    return `${currency} ${value}`;
  }

  try {
    return new Intl.NumberFormat("en-GB", {
      style: "currency",
      currency,
      maximumFractionDigits: 2,
    }).format(amount);
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

export function formatQuantity(
  value: string,
): string {
  const quantity = Number(value);

  if (!Number.isFinite(quantity)) {
    return value;
  }

  return new Intl.NumberFormat(
    "en-GB",
    {
      maximumFractionDigits: 2,
    },
  ).format(quantity);
}
