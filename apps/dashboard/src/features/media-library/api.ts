import {
  apiRequest,
} from "../../lib/http";
import {
  mediaAssetSchema,
  mediaFolderListSchema,
  mediaFolderSchema,
  messageSchema,
  paginatedMediaAssetsSchema,
} from "./schemas";
import type {
  CreateFolderPayload,
  MediaAsset,
  MediaFilters,
  MediaFolder,
  PaginatedMediaAssets,
  UpdateMediaAssetPayload,
  UploadMediaAssetPayload,
} from "./types";

function buildAssetQuery(
  filters: MediaFilters,
): string {
  const params =
    new URLSearchParams();

  params.set(
    "page",
    String(filters.page),
  );

  params.set(
    "page_size",
    String(filters.pageSize),
  );

  if (filters.search.trim()) {
    params.set(
      "search",
      filters.search.trim(),
    );
  }

  if (filters.mediaType) {
    params.set(
      "media_type",
      filters.mediaType,
    );
  }

  if (filters.folderId) {
    params.set(
      "folder_id",
      filters.folderId,
    );
  }

  if (filters.visibility !== "all") {
    params.set(
      "is_public",
      String(
        filters.visibility === "public",
      ),
    );
  }

  if (filters.ordering) {
    params.set(
      "ordering",
      filters.ordering,
    );
  }

  return params.toString();
}

export async function getMediaFolders():
Promise<MediaFolder[]> {
  const response =
    await apiRequest<unknown>(
      "/media/folders",
    );

  return mediaFolderListSchema.parse(
    response,
  );
}

export async function createMediaFolder(
  payload: CreateFolderPayload,
): Promise<MediaFolder> {
  const response =
    await apiRequest<unknown>(
      "/media/folders",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );

  return mediaFolderSchema.parse(
    response,
  );
}

export async function getMediaAssets(
  filters: MediaFilters,
): Promise<PaginatedMediaAssets> {
  const response =
    await apiRequest<unknown>(
      `/media/assets?${buildAssetQuery(
        filters,
      )}`,
    );

  return paginatedMediaAssetsSchema.parse(
    response,
  );
}

export async function getMediaAsset(
  assetId: string,
): Promise<MediaAsset> {
  const response =
    await apiRequest<unknown>(
      `/media/assets/${assetId}`,
    );

  return mediaAssetSchema.parse(
    response,
  );
}

export async function uploadMediaAsset(
  payload: UploadMediaAssetPayload,
): Promise<MediaAsset> {
  const formData =
    new FormData();

  formData.set(
    "file",
    payload.file,
  );

  formData.set(
    "title",
    payload.title,
  );

  formData.set(
    "folder_id",
    payload.folderId,
  );

  formData.set(
    "media_type",
    payload.mediaType,
  );

  formData.set(
    "alt_text",
    payload.altText,
  );

  formData.set(
    "caption",
    payload.caption,
  );

  formData.set(
    "description",
    payload.description,
  );

  formData.set(
    "is_public",
    String(payload.isPublic),
  );

  const response =
    await apiRequest<unknown>(
      "/media/assets/upload",
      {
        method: "POST",
        body: formData,
      },
    );

  return mediaAssetSchema.parse(
    response,
  );
}

export async function updateMediaAsset({
  assetId,
  payload,
}: {
  assetId: string;
  payload: UpdateMediaAssetPayload;
}): Promise<MediaAsset> {
  const response =
    await apiRequest<unknown>(
      `/media/assets/${assetId}`,
      {
        method: "PUT",
        body: JSON.stringify(payload),
      },
    );

  return mediaAssetSchema.parse(
    response,
  );
}

export async function deleteMediaAsset(
  assetId: string,
): Promise<string> {
  const response =
    await apiRequest<unknown>(
      `/media/assets/${assetId}`,
      {
        method: "DELETE",
      },
    );

  return messageSchema.parse(
    response,
  ).message;
}
