import {
  apiRequest,
} from "../../lib/http";
import {
  paginatedMediaAssetsSchema,
} from "../media-library/schemas";
import type {
  MediaAsset,
} from "../media-library/types";
import {
  serviceSelectorResponseSchema,
} from "./schemas";
import type {
  ProfileImageSelectorItem,
  ServiceSelectorItem,
} from "./types";

export async function getActiveServices():
Promise<ServiceSelectorItem[]> {
  const response =
    await apiRequest<unknown>(
      "/services?page=1&page_size=100&is_active=true&ordering=sort_order",
    );

  return serviceSelectorResponseSchema.parse(
    response,
  ).items;
}

export async function getProfileImages():
Promise<ProfileImageSelectorItem[]> {
  const response =
    await apiRequest<unknown>(
      "/media/assets?page=1&page_size=100&media_type=image&ordering=-created_at",
    );

  const parsed =
    paginatedMediaAssetsSchema.parse(
      response,
    );

  return parsed.items
    .filter(
      (
        asset: MediaAsset,
      ) =>
        asset.media_type === "image"
        || asset.media_type === "icon"
        || asset.media_type === "logo",
    )
    .map((asset) => ({
      id: asset.id,
      title: asset.title,
      file_url: asset.file_url,
      media_type: asset.media_type as
        | "image"
        | "icon"
        | "logo",
      alt_text: asset.alt_text,
    }));
}
