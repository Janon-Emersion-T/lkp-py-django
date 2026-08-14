export interface PortfolioService {
  id: string;
  title: string;
  slug: string;
  description?: string;
}

export interface PortfolioTechnology {
  id: string;
  name: string;
  description?: string;
  logo_url?: string | null;
}

export interface PortfolioMedia {
  id: string;
  title?: string;
  caption?: string;
  media_role?: string;
  url?: string | null;
}

export interface PortfolioMetric {
  id: string;
  label: string;
  value: string;
  description?: string;
  icon?: string;
}

export interface PortfolioSeo {
  meta_title?: string;
  meta_description?: string;
  canonical_url?: string;
  robots_index?: boolean;
  robots_follow?: boolean;
  open_graph_title?: string;
  open_graph_description?: string;
  open_graph_image_url?: string | null;
  twitter_title?: string;
  twitter_description?: string;
  structured_data?: Record<string, unknown>;
}

export interface PortfolioProject {
  id: string;
  title: string;
  slug: string;

  client_name?: string;
  industry_name?: string;
  location?: string;
  website_url?: string;

  short_description?: string;

  overview?: Record<string, unknown>;
  challenge?: Record<string, unknown>;
  solution?: Record<string, unknown>;
  implementation?: Record<string, unknown>;
  results?: Record<string, unknown>;

  testimonial?: string;
  testimonial_author?: string;
  testimonial_position?: string;

  featured_image_url?: string | null;

  project_start_date?: string | null;
  project_completion_date?: string | null;
  project_duration?: string;

  is_featured?: boolean;
  published_at?: string | null;

  services?: PortfolioService[];
  technologies?: PortfolioTechnology[];
  media_items?: PortfolioMedia[];
  metrics?: PortfolioMetric[];

  seo?: PortfolioSeo | null;
}

export interface PortfolioResponse {
  count: number;
  service_slug?: string | null;
  items: PortfolioProject[];
}
