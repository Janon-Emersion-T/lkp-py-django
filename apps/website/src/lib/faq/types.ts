export interface ServiceFaq {
  id: string;
  question: string;
  answer: string;
  sort_order?: number;
}

export interface PublicServiceForFaq {
  id: string;
  title: string;
  slug: string;
  short_description?: string;
  faqs?: ServiceFaq[];
}

export interface PublicCatalogResponse {
  services?: PublicServiceForFaq[];
}

export interface AggregatedFaq {
  id: string;
  question: string;
  answer: string;
  serviceTitle: string;
  serviceSlug: string;
}
