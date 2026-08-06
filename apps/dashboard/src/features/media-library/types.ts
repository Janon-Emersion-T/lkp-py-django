export const mediaTypes = [
  "image",
  "video",
  "document",
  "pdf",
  "icon",
  "logo",
  "other",
] as const;

export type MediaType =
  (typeof mediaTypes)[number];

export interface MediaFolder {
  id: string;
  name: string;
  slug: string;
  parent_id: string | null;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface MediaUsage {
  id: string;
  application: string;
  model_name: string;
  object_id: string;
  field_name: string;
  usage_context: string;
  created_at: string;
}

export interface MediaAsset {
  id: string;
  folder_id: string | null;
  folder_name: string | null;
  title: string;
  file_url: string;
  original_name: string;
  media_type: MediaType;
  mime_type: string;
  extension: string;
  size: number;
  width: number | null;
  height: number | null;
  duration_seconds: number | null;
  alt_text: string;
  caption: string;
  description: string;
  tags: string[];
  checksum: string;
  is_optimized: boolean;
  optimized_file_url: string | null;
  webp_file_url: string | null;
  is_public: boolean;
  usages: MediaUsage[];
  created_at: string;
  updated_at: string;
}

export interface MediaPagination {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedMediaAssets {
  items: MediaAsset[];
  pagination: MediaPagination;
}

export interface MediaFilters {
  page: number;
  pageSize: number;
  search: string;
  mediaType: MediaType | "";
  folderId: string;
  visibility: "all" | "public" | "private";
  ordering: string;
}

export interface CreateFolderPayload {
  name: string;
  parent_id: string | null;
  description: string;
}

export interface UpdateMediaAssetPayload {
  folder_id: string | null;
  title: string;
  media_type: MediaType;
  alt_text: string;
  caption: string;
  description: string;
  tags: string[];
  is_public: boolean;
}

export interface UploadMediaAssetPayload {
  file: File;
  title: string;
  folderId: string;
  mediaType: MediaType | "";
  altText: string;
  caption: string;
  description: string;
  isPublic: boolean;
}
