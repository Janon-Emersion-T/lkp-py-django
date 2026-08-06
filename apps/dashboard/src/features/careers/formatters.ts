import type {
  ApplicationSource,
  ApplicationStatus,
  InterviewStatus,
  InterviewType,
  JobListingStatus,
} from "./types";

export const listingStatusLabels: Record<JobListingStatus, string> = {
  draft: "Draft",
  review: "In Review",
  scheduled: "Scheduled",
  published: "Published",
  closed: "Closed",
  archived: "Archived",
};

export const applicationStatusLabels: Record<ApplicationStatus, string> = {
  new: "New",
  screening: "Screening",
  shortlisted: "Shortlisted",
  interview: "Interview",
  assessment: "Assessment",
  offered: "Offered",
  hired: "Hired",
  rejected: "Rejected",
  withdrawn: "Withdrawn",
  archived: "Archived",
};

export const applicationSourceLabels: Record<ApplicationSource, string> = {
  careers_page: "Careers Page",
  linkedin: "LinkedIn",
  facebook: "Facebook",
  referral: "Referral",
  email: "Email",
  manual: "Manual",
  other: "Other",
};

export const interviewStatusLabels: Record<InterviewStatus, string> = {
  scheduled: "Scheduled",
  confirmed: "Confirmed",
  completed: "Completed",
  cancelled: "Cancelled",
  no_show: "No Show",
  rescheduled: "Rescheduled",
};

export const interviewTypeLabels: Record<InterviewType, string> = {
  phone: "Phone",
  video: "Video",
  onsite: "On-site",
  technical: "Technical",
  hr: "HR",
  final: "Final",
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

export function formatMoney(amount: string | null, currency: string): string {
  if (!amount) {
    return "Not supplied";
  }

  const numeric = Number(amount);

  return `${currency} ${
    Number.isFinite(numeric) ? new Intl.NumberFormat().format(numeric) : amount
  }`;
}

export function statusClasses(status: string): string {
  if (
    status === "published" ||
    status === "hired" ||
    status === "completed" ||
    status === "confirmed"
  ) {
    return "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300";
  }

  if (
    status === "scheduled" ||
    status === "interview" ||
    status === "shortlisted" ||
    status === "offered"
  ) {
    return "border-blue-200 bg-blue-50 text-blue-700 dark:border-blue-900 dark:bg-blue-950/40 dark:text-blue-300";
  }

  if (status === "rejected" || status === "cancelled" || status === "no_show") {
    return "border-rose-200 bg-rose-50 text-rose-700 dark:border-rose-900 dark:bg-rose-950/40 dark:text-rose-300";
  }

  if (status === "archived" || status === "closed" || status === "withdrawn") {
    return "border-slate-300 bg-slate-100 text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300";
  }

  return "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300";
}
