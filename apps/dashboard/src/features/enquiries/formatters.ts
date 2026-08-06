import type { EnquiryPriority, EnquirySource, EnquiryStatus } from "./types";

export const enquiryStatusLabels: Record<EnquiryStatus, string> = {
  new: "New",
  assigned: "Assigned",
  contacted: "Contacted",
  qualified: "Qualified",
  proposal_sent: "Proposal Sent",
  won: "Won",
  lost: "Lost",
  spam: "Spam",
  archived: "Archived",
};

export const enquiryPriorityLabels: Record<EnquiryPriority, string> = {
  low: "Low",
  normal: "Normal",
  high: "High",
  urgent: "Urgent",
};

export const enquirySourceLabels: Record<EnquirySource, string> = {
  website: "Website",
  google: "Google",
  facebook: "Facebook",
  instagram: "Instagram",
  linkedin: "LinkedIn",
  tiktok: "TikTok",
  whatsapp: "WhatsApp",
  referral: "Referral",
  email: "Email",
  phone: "Phone",
  manual: "Manual",
  other: "Other",
};

export function formatDateTime(value: string | null): string {
  if (!value) {
    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

export function formatMoneyRange(
  minimum: string | null,
  maximum: string | null,
  currency: string,
): string {
  const formatter = new Intl.NumberFormat();

  if (!minimum && !maximum) {
    return "Budget not supplied";
  }

  if (minimum && maximum) {
    return `${currency} ${formatter.format(Number(minimum))} – ${formatter.format(Number(maximum))}`;
  }

  if (minimum) {
    return `From ${currency} ${formatter.format(Number(minimum))}`;
  }

  return `Up to ${currency} ${formatter.format(Number(maximum))}`;
}

export function statusClasses(status: EnquiryStatus) {
  if (status === "won") {
    return "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300";
  }

  if (status === "qualified" || status === "proposal_sent") {
    return "border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-900 dark:bg-blue-950/40 dark:text-blue-300";
  }

  if (status === "lost" || status === "spam") {
    return "border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-300";
  }

  if (status === "archived") {
    return "border-slate-300 bg-slate-100 text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300";
  }

  return "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300";
}

export function priorityClasses(priority: EnquiryPriority) {
  if (priority === "urgent") {
    return "bg-rose-100 text-rose-700 dark:bg-rose-950 dark:text-rose-300";
  }

  if (priority === "high") {
    return "bg-orange-100 text-orange-700 dark:bg-orange-950 dark:text-orange-300";
  }

  if (priority === "low") {
    return "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300";
  }

  return "bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300";
}
