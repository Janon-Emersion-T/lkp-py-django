export const snapshotTypes = [
  "bootstrap",
  "homepage",
  "catalog",
  "content",
] as const;

export type SnapshotType =
  (typeof snapshotTypes)[number];

export const previewableSnapshotTypes = [
  "bootstrap",
  "homepage",
  "catalog",
  "content",
] as const;

export type PreviewableSnapshotType =
  (typeof previewableSnapshotTypes)[number];

export interface PublicWebsiteSnapshot {
  id: string;
  snapshot_type: SnapshotType;
  environment: string;
  version: number;
  payload: unknown;
  generated_at: string;
  expires_at: string | null;
  is_active: boolean;
  is_expired: boolean;
  checksum: string;
}

export interface SnapshotFilters {
  snapshotType: SnapshotType | "";
  environment: string;
  activeState: "all" | "active" | "inactive";
}

export interface GenerateSnapshotPayload {
  snapshot_type: SnapshotType;
  environment: string;
  ttl_minutes: number;
}

export interface InvalidateSnapshotsPayload {
  snapshot_type: SnapshotType | null;
  environment: string | null;
}

export interface RefreshAllSnapshotsPayload {
  environment: string;
  ttl_minutes: number;
}

export interface InvalidationResult {
  invalidated_count: number;
}

export interface RefreshAllResult {
  environment: string;
  snapshot_count: number;
  snapshots: PublicWebsiteSnapshot[];
}
