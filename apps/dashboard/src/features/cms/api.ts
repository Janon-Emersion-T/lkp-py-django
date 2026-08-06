import {
  z,
} from "zod";

import {
  apiRequest,
} from "../../lib/http";
import {
  cmsCaseStudySchema,
  cmsIndustrySchema,
  cmsInsightSchema,
  cmsPackageSchema,
  cmsPageSchema,
  cmsServiceSchema,
  cmsTestimonialSchema,
  paginationSchema,
} from "./schemas";
import type {
  CmsContentType,
  CmsFilters,
  CmsRecord,
  PaginatedCmsRecords,
} from "./types";

const endpointByType: Record<
  CmsContentType,
  string
> = {
  pages: "/cms/pages",
  services: "/services",
  packages: "/packages",
  industries: "/industries",
  insights: "/insights",
  "case-studies": "/case-studies",
  testimonials: "/testimonials",
};

const schemaByType = {
  pages: cmsPageSchema,
  services: cmsServiceSchema,
  packages: cmsPackageSchema,
  industries: cmsIndustrySchema,
  insights: cmsInsightSchema,
  "case-studies": cmsCaseStudySchema,
  testimonials: cmsTestimonialSchema,
} satisfies Record<
  CmsContentType,
  z.ZodType<CmsRecord>
>;

function buildQueryString(
  type: CmsContentType,
  filters: CmsFilters,
): string {
  const params = new URLSearchParams();

  params.set(
    "page",
    String(filters.page),
  );

  params.set(
    "page_size",
    String(filters.pageSize),
  );

  const search = filters.search.trim();

  if (search) {
    params.set("search", search);
  }

  if (filters.status) {
    params.set("status", filters.status);
  }

  if (
    filters.featured !== null
    && type !== "pages"
  ) {
    params.set(
      "is_featured",
      String(filters.featured),
    );
  }

  if (
    filters.active !== null
    && type !== "pages"
  ) {
    params.set(
      "is_active",
      String(filters.active),
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

export async function getCmsRecords(
  type: CmsContentType,
  filters: CmsFilters,
): Promise<PaginatedCmsRecords> {
  const endpoint = endpointByType[type];
  const query = buildQueryString(
    type,
    filters,
  );

  const response = await apiRequest<unknown>(
    `${endpoint}?${query}`,
  );

  const parsed = z.object({
    items: z.array(schemaByType[type]),
    pagination: paginationSchema,
  }).parse(response);

  return {
    items: parsed.items,
    pagination: parsed.pagination,
  };
}

export async function getCmsRecord(
  type: CmsContentType,
  id: string,
): Promise<CmsRecord> {
  const endpoint = endpointByType[type];

  const response = await apiRequest<unknown>(
    `${endpoint}/${id}`,
  );

  return schemaByType[type].parse(
    response,
  );
}
