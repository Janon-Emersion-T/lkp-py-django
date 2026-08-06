import type {
  MediaType,
} from "./types";

export const mediaTypeLabels:
Record<MediaType, string> = {
  image: "Image",
  video: "Video",
  document: "Document",
  pdf: "PDF",
  icon: "Icon",
  logo: "Logo",
  other: "Other",
};

export function formatBytes(
  bytes: number,
): string {
  if (bytes < 1024) {
    return `${bytes} B`;
  }

  if (bytes < 1024 * 1024) {
    return `${(
      bytes / 1024
    ).toFixed(1)} KB`;
  }

  return `${(
    bytes / 1024 / 1024
  ).toFixed(2)} MB`;
}

export function formatDateTime(
  value: string,
): string {
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

export function resolveMediaUrl(
  value: string | null,
): string {
  if (!value) {
    return "";
  }

  if (/^https?:\/\//i.test(value)) {
    return value;
  }

  const apiBaseUrl =
    import.meta.env.VITE_API_BASE_URL ??
    "http://127.0.0.1:8082/api/v1";

  const apiUrl = new URL(apiBaseUrl);

  return new URL(
    value,
    apiUrl.origin,
  ).toString();
}

export function isImageAsset(
  mediaType: MediaType,
): boolean {
  return [
    "image",
    "icon",
    "logo",
  ].includes(mediaType);
}
