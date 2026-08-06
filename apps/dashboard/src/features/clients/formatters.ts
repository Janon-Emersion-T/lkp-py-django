import type {
  ClientContact,
  ClientStatus,
  ClientType,
} from "./types";

export const clientStatusLabels: Record<
  ClientStatus,
  string
> = {
  prospect: "Prospect",
  active: "Active",
  inactive: "Inactive",
  suspended: "Suspended",
  archived: "Archived",
};

export const clientTypeLabels: Record<
  ClientType,
  string
> = {
  company: "Company",
  individual: "Individual",
  non_profit: "Non-profit",
  government: "Government",
};

export function formatCount(
  value: number,
): string {
  return new Intl.NumberFormat(
    "en-GB",
  ).format(value);
}

export function formatDateTime(
  value: string,
): string {
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

export function formatContactName(
  contact: ClientContact,
): string {
  return (
    [
      contact.first_name,
      contact.last_name,
    ]
      .filter(Boolean)
      .join(" ")
    || "Unnamed contact"
  );
}

export function normalizeExternalUrl(
  value: string,
): string {
  if (
    value.startsWith("http://")
    || value.startsWith("https://")
  ) {
    return value;
  }

  return `https://${value}`;
}

export function whatsappUrl(
  value: string,
): string {
  const digits = value.replace(
    /\D/g,
    "",
  );

  return `https://wa.me/${digits}`;
}
