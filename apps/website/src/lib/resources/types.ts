export type ResourceType =
  | "download"
  | "guide"
  | "checklist"
  | "template";

export interface ResourceSeo {
  meta_title?: string;
  meta_description?: string;
  canonical_url?: string;
  robots_index?: boolean;
  robots_follow?: boolean;
  open_graph_title?: string;
  open_graph_description?: string;
  structured_data?: Record<string, unknown>;
}

export interface PublicResource {
  id: string;
  title: string;
  slug: string;
  resource_type: ResourceType;

  excerpt?: string;

  content?: {
    intro?: string;
    sections?: Array<{
      heading?: string;
      body?: string;
      [key: string]: unknown;
    }>;
    [key: string]: unknown;
  };

  file_url?: string | null;
  external_url?: string;
  resource_url?: string;

  featured_image_url?: string | null;

  status?: string;
  published_at?: string | null;

  is_featured?: boolean;

  download_count?: number;
  sort_order?: number;

  seo?: ResourceSeo | null;
}

export interface PublicResourcesResponse {
  count: number;
  resource_type?: ResourceType | null;
  items: PublicResource[];
}
