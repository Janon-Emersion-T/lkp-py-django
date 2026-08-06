import {
  apiRequest,
} from "../../lib/http";
import {
  invalidationResultSchema,
  publicPreviewSchema,
  publicWebsiteSnapshotSchema,
  refreshAllResultSchema,
  snapshotListSchema,
} from "./schemas";
import type {
  GenerateSnapshotPayload,
  InvalidateSnapshotsPayload,
  InvalidationResult,
  PreviewableSnapshotType,
  PublicWebsiteSnapshot,
  RefreshAllResult,
  RefreshAllSnapshotsPayload,
  SnapshotFilters,
} from "./types";

const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL ??
  "http://127.0.0.1:8082/api/v1";

function buildSnapshotQuery(
  filters: SnapshotFilters,
): string {
  const params =
    new URLSearchParams();

  if (filters.snapshotType) {
    params.set(
      "snapshot_type",
      filters.snapshotType,
    );
  }

  if (filters.environment.trim()) {
    params.set(
      "environment",
      filters.environment.trim(),
    );
  }

  if (filters.activeState !== "all") {
    params.set(
      "is_active",
      String(
        filters.activeState === "active",
      ),
    );
  }

  return params.toString();
}

export async function getSnapshots(
  filters: SnapshotFilters,
): Promise<PublicWebsiteSnapshot[]> {
  const query =
    buildSnapshotQuery(filters);

  const response =
    await apiRequest<unknown>(
      `/public-website/snapshots${
        query ? `?${query}` : ""
      }`,
    );

  return snapshotListSchema.parse(
    response,
  );
}

export async function generateSnapshot(
  payload: GenerateSnapshotPayload,
): Promise<PublicWebsiteSnapshot> {
  const response =
    await apiRequest<unknown>(
      "/public-website/snapshots/generate",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );

  return publicWebsiteSnapshotSchema.parse(
    response,
  );
}

export async function invalidateSnapshots(
  payload: InvalidateSnapshotsPayload,
): Promise<InvalidationResult> {
  const response =
    await apiRequest<unknown>(
      "/public-website/snapshots/invalidate",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );

  return invalidationResultSchema.parse(
    response,
  );
}

export async function refreshAllSnapshots(
  payload: RefreshAllSnapshotsPayload,
): Promise<RefreshAllResult> {
  const response =
    await apiRequest<unknown>(
      "/public-website/snapshots/refresh-all",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );

  return refreshAllResultSchema.parse(
    response,
  );
}

export async function getPublicPreview(
  type: PreviewableSnapshotType,
  environment: string,
): Promise<Record<string, unknown>> {
  const response =
    await apiRequest<unknown>(
      `/public-website/${type}?environment=${encodeURIComponent(
        environment,
      )}`,
    );

  return publicPreviewSchema.parse(
    response,
  );
}

export function getRawPreviewUrl(
  type: PreviewableSnapshotType,
  environment: string,
): string {
  return `${apiBaseUrl}/public-website/${type}?environment=${encodeURIComponent(
    environment,
  )}`;
}
