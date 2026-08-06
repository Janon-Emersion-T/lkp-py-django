import type {
  PublicWebsiteSnapshot,
  SnapshotType,
} from "./types";

export const snapshotTypeLabels:
Record<SnapshotType, string> = {
  bootstrap: "Bootstrap",
  homepage: "Homepage",
  catalog: "Catalog",
  content: "Content",
};

export function formatDateTime(
  value: string | null,
): string {
  if (!value) {
    return "No expiry";
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat(
    undefined,
    {
      dateStyle: "medium",
      timeStyle: "short",
    },
  ).format(date);
}

export function formatJson(
  value: unknown,
): string {
  try {
    return JSON.stringify(
      value,
      null,
      2,
    );
  } catch {
    return String(value);
  }
}

export function formatPayloadSize(
  value: unknown,
): string {
  const bytes =
    new TextEncoder().encode(
      formatJson(value),
    ).length;

  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(
      bytes / 1024
    ).toFixed(2)} KB`;
  }

  return `${(
    bytes / 1024 / 1024
  ).toFixed(2)} MB`;
}

export function shortenChecksum(
  checksum: string,
): string {
  if (checksum.length <= 22) {
    return checksum;
  }

  return `${checksum.slice(
    0,
    12,
  )}…${checksum.slice(-8)}`;
}

export function getSnapshotState(
  snapshot: PublicWebsiteSnapshot,
) {
  if (
    snapshot.is_active
    && !snapshot.is_expired
  ) {
    return {
      label: "Active",
      className:
        "border-emerald-200 bg-emerald-50 text-emerald-700 dark:border-emerald-900 dark:bg-emerald-950/40 dark:text-emerald-300",
    };
  }

  if (
    snapshot.is_active
    && snapshot.is_expired
  ) {
    return {
      label: "Active · Expired",
      className:
        "border-amber-200 bg-amber-50 text-amber-700 dark:border-amber-900 dark:bg-amber-950/40 dark:text-amber-300",
    };
  }

  if (snapshot.is_expired) {
    return {
      label: "Inactive · Expired",
      className:
        "border-slate-300 bg-slate-100 text-slate-600 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-300",
    };
  }

  return {
    label: "Invalidated",
    className:
      "border-red-200 bg-red-50 text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-300",
  };
}

export function isPreviewable(
  type: SnapshotType,
): type is SnapshotType {
  return (
    type === "bootstrap"
    || type === "homepage"
    || type === "catalog"
    || type === "content"
  );
}
