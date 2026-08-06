import {
  z,
} from "zod";

const recordObjectSchema = z.record(
  z.string(),
  z.unknown(),
);

const recordArraySchema = z.array(
  recordObjectSchema,
);

const nullableUuidSchema = z
  .string()
  .uuid()
  .nullable();

const commonSchema = z.object({
  id: z.string().uuid(),
  status: z.string(),
  is_active: z.boolean(),
  is_featured: z.boolean().optional(),
  is_publicly_available:
    z.boolean().optional(),
  published_at: z.string().nullable(),
  scheduled_for: z.string().nullable(),
  created_at: z.string(),
  updated_at: z.string(),
});

export const cmsPageSchema =
  commonSchema.extend({
    title: z.string(),
    slug: z.string(),
    page_type: z.string(),
    excerpt: z.string(),
    content: recordObjectSchema,
    featured_image_id:
      nullableUuidSchema,
    is_indexable: z.boolean(),
    is_visible_in_navigation:
      z.boolean(),
    navigation_label: z.string(),
    navigation_order: z.number().int(),
    current_revision_number:
      z.number().int(),
    seo: recordObjectSchema.nullable(),
    revisions: recordArraySchema,
  });

export const cmsServiceSchema =
  commonSchema.extend({
    title: z.string(),
    slug: z.string(),
    short_description: z.string(),
    description: recordObjectSchema,
    icon: z.string(),
    hero_title: z.string(),
    hero_description: z.string(),
    hero_image_id: nullableUuidSchema,
    sort_order: z.number().int(),
    view_count: z.number().int(),
    current_revision_number:
      z.number().int(),
    features: recordArraySchema,
    technologies: recordArraySchema,
    process_steps: recordArraySchema,
    faqs: recordArraySchema,
    seo: recordObjectSchema.nullable(),
    revisions: recordArraySchema,
  });

export const cmsPackageSchema =
  commonSchema.extend({
    name: z.string(),
    slug: z.string(),
    category: z.string(),
    service_id: nullableUuidSchema,
    service_title: z.string().nullable(),
    short_description: z.string(),
    description: recordObjectSchema,
    pricing_type: z.string(),
    price: z.string(),
    compare_at_price:
      z.string().nullable(),
    currency: z.string(),
    billing_cycle: z.string(),
    delivery_time: z.string(),
    revisions_included:
      z.number().int(),
    support_period_days:
      z.number().int(),
    is_popular: z.boolean(),
    sort_order: z.number().int(),
    badge_text: z.string(),
    cta_label: z.string(),
    cta_url: z.string(),
    current_revision_number:
      z.number().int(),
    features: recordArraySchema,
    addons: recordArraySchema,
    target_audiences:
      recordArraySchema,
    faqs: recordArraySchema,
    seo: recordObjectSchema.nullable(),
    revisions: recordArraySchema,
  });

export const cmsIndustrySchema =
  commonSchema.extend({
    name: z.string(),
    slug: z.string(),
    short_description: z.string(),
    description: recordObjectSchema,
    hero_title: z.string(),
    hero_description: z.string(),
    hero_image_id: nullableUuidSchema,
    icon: z.string(),
    sort_order: z.number().int(),
    challenges: z.array(z.unknown()),
    solutions: z.array(z.unknown()),
    benefits: z.array(z.unknown()),
    cta_title: z.string(),
    cta_text: z.string(),
    cta_label: z.string(),
    cta_url: z.string(),
    current_revision_number:
      z.number().int(),
    services: recordArraySchema,
    faqs: recordArraySchema,
    seo: recordObjectSchema.nullable(),
    revisions: recordArraySchema,
  });

export const cmsInsightSchema =
  commonSchema.extend({
    title: z.string(),
    slug: z.string(),
    excerpt: z.string(),
    content: recordObjectSchema,
    category_id: nullableUuidSchema,
    category_name: z.string().nullable(),
    author_id: z.number().int().nullable(),
    author_email: z.string().nullable(),
    featured_image_id:
      nullableUuidSchema,
    reading_time_minutes:
      z.number().int(),
    word_count: z.number().int(),
    view_count: z.number().int(),
    allow_comments: z.boolean(),
    current_revision_number:
      z.number().int(),
    tags: recordArraySchema,
    related_articles:
      recordArraySchema,
    internal_links: recordArraySchema,
    seo: recordObjectSchema.nullable(),
    revisions: recordArraySchema,
    publishing_events:
      recordArraySchema,
  });

export const cmsCaseStudySchema =
  commonSchema.extend({
    title: z.string(),
    slug: z.string(),
    client_id: nullableUuidSchema,
    client_name: z.string(),
    linked_client_name:
      z.string().nullable(),
    project_id: nullableUuidSchema,
    project_name: z.string().nullable(),
    industry_id: nullableUuidSchema,
    industry_name: z.string().nullable(),
    location: z.string(),
    website_url: z.string(),
    short_description: z.string(),
    overview: recordObjectSchema,
    challenge: recordObjectSchema,
    solution: recordObjectSchema,
    implementation: recordObjectSchema,
    results: recordObjectSchema,
    testimonial: z.string(),
    testimonial_author: z.string(),
    testimonial_position: z.string(),
    featured_image_id:
      nullableUuidSchema,
    project_start_date:
      z.string().nullable(),
    project_completion_date:
      z.string().nullable(),
    project_duration: z.string(),
    sort_order: z.number().int(),
    view_count: z.number().int(),
    current_revision_number:
      z.number().int(),
    services: recordArraySchema,
    technologies: recordArraySchema,
    media_items: recordArraySchema,
    metrics: recordArraySchema,
    milestones: recordArraySchema,
    seo: recordObjectSchema.nullable(),
    revisions: recordArraySchema,
  });

export const cmsTestimonialSchema =
  commonSchema.extend({
    title: z.string().optional(),
    author_name: z.string(),
    author_position: z.string(),
    company_name: z.string(),
    content: z.string(),
    rating: z.number().int(),
    source: z.string(),
    client_id: nullableUuidSchema,
    project_id: nullableUuidSchema,
    is_verified: z.boolean(),
    sort_order: z.number().int(),
  });

export const paginationSchema = z.object({
  page: z.number().int(),
  page_size: z.number().int(),
  total_items: z.number().int(),
  total_pages: z.number().int(),
});
