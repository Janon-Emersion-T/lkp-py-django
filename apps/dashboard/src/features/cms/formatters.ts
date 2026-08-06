import type {
  CmsContentType,
  CmsRecord,
} from "./types";

export const cmsContentLabels: Record<
  CmsContentType,
  string
> = {
  pages: "Pages",
  services: "Services",
  packages: "Packages",
  industries: "Industries",
  insights: "Insights",
  "case-studies": "Case Studies",
  testimonials: "Testimonials",
};

export function getCmsTitle(
  record: CmsRecord,
): string {
  if ("title" in record) {
    return record.title || "Untitled";
  }

  if ("name" in record) {
    return record.name;
  }

  if ("author_name" in record) {
    return record.author_name;
  }

  return "Untitled content";
}

export function getCmsSubtitle(
  record: CmsRecord,
): string {
  if (
    "short_description" in record
  ) {
    return record.short_description;
  }

  if ("excerpt" in record) {
    return record.excerpt;
  }

  if ("content" in record) {
    return typeof record.content
      === "string"
      ? record.content
      : "";
  }

  return "";
}

export function getCmsSlug(
  record: CmsRecord,
): string {
  return "slug" in record
    ? record.slug
    : "";
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

export function formatCurrency(
  value: string,
  currency: string,
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
      },
    ).format(amount);
  } catch {
    return `${currency} ${amount.toLocaleString(
      "en-GB",
    )}`;
  }
}
