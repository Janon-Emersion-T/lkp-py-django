import type {
  LeadPriority,
  LeadSource,
  LeadStatus,
  UserSummary,
} from "./types";

export const leadStatusLabels: Record<
  LeadStatus,
  string
> = {
  new: "New",
  contacted: "Contacted",
  follow_up: "Follow Up",
  proposal_sent: "Proposal Sent",
  negotiation: "Negotiation",
  won: "Won",
  lost: "Lost",
  spam: "Spam",
};

export const leadSourceLabels: Record<
  LeadSource,
  string
> = {
  google: "Google",
  organic_search: "Organic Search",
  facebook: "Facebook",
  instagram: "Instagram",
  linkedin: "LinkedIn",
  tiktok: "TikTok",
  referral: "Referral",
  whatsapp: "WhatsApp",
  email: "Email",
  manual: "Manual",
  other: "Other",
};

export const leadPriorityLabels: Record<
  LeadPriority,
  string
> = {
  low: "Low",
  normal: "Normal",
  high: "High",
  urgent: "Urgent",
};

export function formatCount(
  value: number,
): string {
  return new Intl.NumberFormat(
    "en-GB",
  ).format(value);
}

export function formatPercentage(
  value: number,
): string {
  return `${new Intl.NumberFormat("en-GB", {
    maximumFractionDigits: 2,
  }).format(value)}%`;
}

export function formatLeadValue(
  value: string | null,
  currency: string,
): string {
  if (value === null) {
    return "Not estimated";
  }

  const numericValue = Number(value);

  if (!Number.isFinite(numericValue)) {
    return `${currency} ${value}`;
  }

  try {
    return new Intl.NumberFormat("en-GB", {
      style: "currency",
      currency,
      maximumFractionDigits: 2,
    }).format(numericValue);
  } catch {
    return `${currency} ${numericValue.toLocaleString(
      "en-GB",
    )}`;
  }
}

export function formatDateTime(
  value: string | null,
): string {
  if (!value) {
    return "Not scheduled";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function formatUserName(
  user: UserSummary | null,
): string {
  if (!user) {
    return "Unassigned";
  }

  return (
    [
      user.first_name,
      user.last_name,
    ]
      .filter(Boolean)
      .join(" ")
    || user.email
  );
}

export function normalizeExternalUrl(
  value: string,
): string {
  if (
    value.startsWith("http://") ||
    value.startsWith("https://")
  ) {
    return value;
  }

  return `https://${value}`;
}

export function whatsappUrl(
  value: string,
): string {
  const digits = value.replace(/\D/g, "");

  return `https://wa.me/${digits}`;
}
