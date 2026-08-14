export interface PublicTestimonial {
  resource_type: string;
  id: string;

  author_name: string;
  author_position?: string;
  company_name?: string;

  content: string;
  short_content?: string;

  rating?: number;
  source?: string;
  source_url?: string;

  author_image_id?: string | null;
  company_logo_id?: string | null;

  client_id?: string | null;
  client_name?: string | null;

  project_id?: string | null;
  project_title?: string | null;

  status?: string;
  published_at?: string | null;

  is_featured?: boolean;
  is_verified?: boolean;

  sort_order?: number;
  created_at?: string;
  updated_at?: string;
}

export interface PublicWebsiteContent {
  testimonials?: PublicTestimonial[];
}
