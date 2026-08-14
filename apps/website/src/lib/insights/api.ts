import type {
  PublicContentResponse,
  PublicInsight,
} from "./types";

const API_BASE_URL =
  import.meta.env.API_BASE_URL
  ?? import.meta.env.PUBLIC_API_BASE_URL
  ?? "http://127.0.0.1:8082/api/v1";

const CONTENT_ENDPOINT =
  `${API_BASE_URL}/public-website/content`;

export async function getPublicInsights(): Promise<
  PublicInsight[]
> {
  try {
    const response = await fetch(
      `${CONTENT_ENDPOINT}?environment=production`,
      {
        headers: {
          Accept: "application/json",
        },
      },
    );

    if (!response.ok) {
      console.error(
        `[Insights] API returned ${response.status}`,
      );

      return [];
    }

    const data =
      await response.json() as PublicContentResponse;

    if (!Array.isArray(data.insights)) {
      return [];
    }

    return data.insights;
  } catch (error) {
    console.error(
      "[Insights] Failed to load public insights:",
      error,
    );

    return [];
  }
}

export async function getFeaturedInsights(
  limit = 1,
): Promise<PublicInsight[]> {
  const insights = await getPublicInsights();

  return insights
    .filter((item) => item.is_featured)
    .slice(0, limit);
}

export async function getInsightsByCategory(
  categorySlug: string,
): Promise<PublicInsight[]> {
  const normalized =
    categorySlug.trim().toLowerCase();

  const insights = await getPublicInsights();

  return insights.filter(
    (item) =>
      item.category_slug?.toLowerCase()
      === normalized,
  );
}

export async function getInsightBySlug(
  slug: string,
): Promise<PublicInsight | null> {
  const normalized = slug.trim();

  const insights = await getPublicInsights();

  return (
    insights.find(
      (item) => item.slug === normalized,
    )
    ?? null
  );
}
