import type {
  AggregatedFaq,
  PublicCatalogResponse,
} from "./types";

const API_BASE_URL =
  import.meta.env.API_BASE_URL
  ?? import.meta.env.PUBLIC_API_BASE_URL
  ?? "http://127.0.0.1:8082/api/v1";

const ENDPOINT =
  `${API_BASE_URL}/public-website/catalog`;

export async function getFaqs(): Promise<
  AggregatedFaq[]
> {
  try {
    const response = await fetch(
      `${ENDPOINT}?environment=production`,
      {
        headers: {
          Accept: "application/json",
        },
      },
    );

    if (!response.ok) {
      console.error(
        `[FAQ] API returned ${response.status}`,
      );

      return [];
    }

    const data =
      await response.json() as PublicCatalogResponse;

    const services =
      Array.isArray(data.services)
        ? data.services
        : [];

    return services.flatMap((service) =>
      (service.faqs ?? []).map((faq) => ({
        id: faq.id,
        question: faq.question,
        answer: faq.answer,
        serviceTitle: service.title,
        serviceSlug: service.slug,
      })),
    );
  } catch (error) {
    console.error(
      "[FAQ] Failed to load FAQs:",
      error,
    );

    return [];
  }
}
