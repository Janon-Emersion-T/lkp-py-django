import {
  z,
} from "zod";

import {
  snapshotTypes,
} from "./types";

export const snapshotTypeSchema =
  z.enum(snapshotTypes);

export const publicWebsiteSnapshotSchema =
  z.object({
    id: z.string(),
    snapshot_type: snapshotTypeSchema,
    environment: z.string(),
    version: z.number().int().nonnegative(),
    payload: z.unknown(),
    generated_at: z.string(),
    expires_at: z.string().nullable(),
    is_active: z.boolean(),
    is_expired: z.boolean(),
    checksum: z.string(),
  });

export const snapshotListSchema =
  z.array(publicWebsiteSnapshotSchema);

export const invalidationResultSchema =
  z.object({
    invalidated_count:
      z.number().int().nonnegative(),
  });

export const refreshAllResultSchema =
  z.object({
    environment: z.string(),
    snapshot_count:
      z.number().int().nonnegative(),
    snapshots:
      z.array(publicWebsiteSnapshotSchema),
  });

export const publicPreviewSchema =
  z.record(
    z.string(),
    z.unknown(),
  );
