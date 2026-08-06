import type {
  CampaignStatus,
  SubscriberSource,
  SubscriberStatus,
} from "./types";

export const subscriberStatusLabels: Record<SubscriberStatus, string> = {
  pending: "Pending",
  active: "Active",
  unsubscribed: "Unsubscribed",
  bounced: "Bounced",
  complained: "Complained",
  suppressed: "Suppressed",
};

export const subscriberSourceLabels: Record<SubscriberSource, string> = {
  website: "Website",
  manual: "Manual",
  import: "Import",
  contact_form: "Contact Form",
  quote_form: "Quote Form",
  careers: "Careers",
  client_portal: "Client Portal",
  other: "Other",
};

export const campaignStatusLabels: Record<CampaignStatus, string> = {
  draft: "Draft",
  review: "In Review",
  scheduled: "Scheduled",
  queued: "Queued",
  sending: "Sending",
  sent: "Sent",
  paused: "Paused",
  cancelled: "Cancelled",
  failed: "Failed",
  archived: "Archived",
};

export function formatDateTime(value: string | null): string {
  if (!value) return "—";

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) return value;

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function formatRate(value: number): string {
  return `${new Intl.NumberFormat(undefined, {
    maximumFractionDigits: 2,
  }).format(value)}%`;
}

export function statusClasses(status: string): string {
  if (["active", "sent", "delivered", "clicked", "opened"].includes(status)) {
    return "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300";
  }

  if (["scheduled", "queued", "sending", "review"].includes(status)) {
    return "border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-900 dark:bg-blue-950/40 dark:text-blue-300";
  }

  if (["bounced", "complained", "failed", "cancelled"].includes(status)) {
    return "border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-300";
  }

  if (["unsubscribed", "suppressed", "archived", "paused"].includes(status)) {
    return "border-slate-300 bg-slate-100 text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300";
  }

  return "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300";
}
