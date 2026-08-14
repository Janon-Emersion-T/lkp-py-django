export interface PublicInsightTag {
  id: string;
  name: string;
  slug: string;
}

export interface PublicInsightSeo {
  meta_title?: string;
  meta_description?: string;
  canonical_url?: string;
  robots_index?: boolean;
  robots_follow?: boolean;
  open_graph_title?: string;
  open_graph_description?: string;
  open_graph_image_id?: string | null;
  twitter_title?: string;
  twitter_description?: string;
  article_schema?: Record<string, unknown>;
  faq_schema?: unknown[];
}

export interface PublicInsight {
  resource_type: string;

  id: string;
  slug: string;
  title: string;
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

  status?: string;

  published_at?: string | null;
  created_at?: string;
  updated_at?: string;

  is_featured?: boolean;

  reading_time_minutes?: number;
  word_count?: number;
  view_count?: number;

  category_id?: string | null;
  category_name?: string | null;
  category_slug?: string | null;

  author_id?: number | null;
  author_email?: string | null;

  featured_image_id?: string | null;

  tags?: PublicInsightTag[];

  seo?: PublicInsightSeo | null;
}

export interface PublicContentResponse {
  environment: string;
  generated_at: string;

  insights: PublicInsight[];

  case_studies?: unknown[];
  testimonials?: unknown[];
  career_listings?: unknown[];

  snapshot?: {
    id: string;
    version: number;
    generated_at: string;
    expires_at: string | null;
    checksum: string;
  };
}
