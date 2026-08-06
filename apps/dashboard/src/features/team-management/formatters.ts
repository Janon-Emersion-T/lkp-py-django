import type {
  EngagementType,
  EmploymentStatus,
  TeamType,
  WorkLocationType,
} from "./types";

export const teamTypeLabels:
Record<TeamType, string> = {
  executive: "Executive",
  management: "Management",
  engineering: "Engineering",
  design: "Design",
  marketing: "Marketing",
  sales: "Sales",
  finance: "Finance",
  operations: "Operations",
  support: "Support",
  hr: "Human Resources",
  legal: "Legal",
  project: "Project Team",
  custom: "Custom",
};

export const employmentStatusLabels:
Record<EmploymentStatus, string> = {
  active: "Active",
  on_leave: "On Leave",
  suspended: "Suspended",
  resigned: "Resigned",
  terminated: "Terminated",
  contract_ended: "Contract Ended",
  inactive: "Inactive",
};

export const engagementTypeLabels:
Record<EngagementType, string> = {
  full_time: "Full-time",
  part_time: "Part-time",
  contract: "Contract",
  intern: "Intern",
  consultant: "Consultant",
  volunteer: "Volunteer",
};

export const workLocationTypeLabels:
Record<WorkLocationType, string> = {
  onsite: "On-site",
  remote: "Remote",
  hybrid: "Hybrid",
};

export function formatDate(
  value: string | null,
): string {
  if (!value) {
    return "—";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(
    undefined,
    {
      dateStyle: "medium",
    },
  ).format(date);
}

export function slugify(
  value: string,
): string {
  return value
    .toLowerCase()
    .trim()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function parseMetadata(
  value: string,
): Record<string, unknown> {
  const normalized = value.trim();

  if (!normalized) {
    return {};
  }

  const parsed: unknown =
    JSON.parse(normalized);

  if (
    typeof parsed !== "object"
    || parsed === null
    || Array.isArray(parsed)
  ) {
    throw new Error(
      "Metadata must be a JSON object.",
    );
  }

  return parsed as Record<string, unknown>;
}

export function formatMetadata(
  value: Record<string, unknown>,
): string {
  return JSON.stringify(
    value,
    null,
    2,
  );
}

export function statusBadgeClasses(
  status: EmploymentStatus,
): string {
  if (status === "active") {
    return "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300";
  }

  if (status === "on_leave") {
    return "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300";
  }

  if (
    status === "resigned"
    || status === "terminated"
    || status === "contract_ended"
  ) {
    return "border-red-200 bg-red-50 text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-300";
  }

  return "border-slate-300 bg-slate-100 text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300";
}
