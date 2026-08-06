import {
  z,
} from "zod";

import {
  mediaTypes,
} from "./types";

export const mediaFolderSchema =
  z.object({
    id: z.string().uuid(),
    name: z.string(),
    slug: z.string(),
    parent_id:
      z.string().uuid().nullable(),
    description: z.string(),
    created_at: z.string(),
    updated_at: z.string(),
  });

export const mediaUsageSchema =
  z.object({
    id: z.string().uuid(),
    application: z.string(),
    model_name: z.string(),
    object_id: z.string(),
    field_name: z.string(),
    usage_context: z.string(),
    created_at: z.string(),
  });

export const mediaAssetSchema =
  z.object({
    id: z.string().uuid(),
    folder_id:
      z.string().uuid().nullable(),
    folder_name:
      z.string().nullable(),
    title: z.string(),
    file_url: z.string(),
    original_name: z.string(),
    media_type: z.enum(mediaTypes),
    mime_type: z.string(),
    extension: z.string(),
    size:
      z.number().int().nonnegative(),
    width:
      z.number().int().nonnegative().nullable(),
    height:
      z.number().int().nonnegative().nullable(),
    duration_seconds:
      z.number().int().nonnegative().nullable(),
    alt_text: z.string(),
    caption: z.string(),
    description: z.string(),
    tags: z.array(z.string()),
    checksum: z.string(),
    is_optimized: z.boolean(),
    optimized_file_url:
      z.string().nullable(),
    webp_file_url:
      z.string().nullable(),
    is_public: z.boolean(),
    usages:
      z.array(mediaUsageSchema),
    created_at: z.string(),
    updated_at: z.string(),
  });

export const mediaFolderListSchema =
  z.array(mediaFolderSchema);

export const paginatedMediaAssetsSchema =
  z.object({
    items: z.array(mediaAssetSchema),
    pagination: z.object({
      page:
        z.number().int().positive(),
      page_size:
        z.number().int().positive(),
      total_items:
        z.number().int().nonnegative(),
      total_pages:
        z.number().int().nonnegative(),
    }),
  });

export const messageSchema =
  z.object({
    status: z.string(),
    message: z.string(),
  });
