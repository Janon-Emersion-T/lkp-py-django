import type {
  MilestoneStatus,
  ProjectPriority,
  ProjectStatus,
  UserSummary,
} from "./types";

export const projectStatusLabels: Record<
  ProjectStatus,
  string
> = {
  planning: "Planning",
  development: "Development",
  testing: "Testing",
  review: "Review",
  completed: "Completed",
  cancelled: "Cancelled",
};

export const projectPriorityLabels: Record<
  ProjectPriority,
  string
> = {
  low: "Low",
  normal: "Normal",
  high: "High",
  urgent: "Urgent",
};

export const milestoneStatusLabels: Record<
  MilestoneStatus,
  string
> = {
  pending: "Pending",
  in_progress: "In Progress",
  completed: "Completed",
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
    value.startsWith("http://")
    || value.startsWith("https://")
  ) {
    return value;
  }

  return `https://${value}`;
}

export function isProjectOverdue(
  deadline: string | null,
  status: ProjectStatus,
): boolean {
  if (
    !deadline
    || status === "completed"
    || status === "cancelled"
  ) {
    return false;
  }

  const deadlineDate = new Date(
    `${deadline}T23:59:59`,
  );

  return (
    !Number.isNaN(deadlineDate.getTime())
    && deadlineDate.getTime() < Date.now()
  );
}
