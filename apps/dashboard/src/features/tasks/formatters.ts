import type {
  TaskPriority,
  TaskStatus,
  UserSummary,
} from "./types";

export const taskStatusLabels: Record<
  TaskStatus,
  string
> = {
  todo: "To Do",
  in_progress: "In Progress",
  testing: "Testing",
  review: "Review",
  completed: "Completed",
  cancelled: "Cancelled",
};

export const taskPriorityLabels: Record<
  TaskPriority,
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

export function formatHours(
  value: string,
): string {
  const hours = Number(value);

  if (!Number.isFinite(hours)) {
    return `${value}h`;
  }

  return `${new Intl.NumberFormat(
    "en-GB",
    {
      maximumFractionDigits: 2,
    },
  ).format(hours)}h`;
}

export function isTaskOverdue(
  dueDate: string | null,
  status: TaskStatus,
): boolean {
  if (
    !dueDate
    || status === "completed"
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
