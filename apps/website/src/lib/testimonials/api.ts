import type {
  PublicTestimonial,
  PublicWebsiteContent,
} from "./types";

const API_BASE_URL =
  import.meta.env.API_BASE_URL
  ?? import.meta.env.PUBLIC_API_BASE_URL
  ?? "http://127.0.0.1:8082/api/v1";

const CONTENT_ENDPOINT =
  `${API_BASE_URL}/public-website/content`;

export async function getTestimonials(): Promise<
  PublicTestimonial[]
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
        `[Testimonials] API returned ${response.status}`,
      );

      return [];
    }

    const data =
      await response.json() as PublicWebsiteContent;

    return Array.isArray(data.testimonials)
      ? data.testimonials
      : [];
  } catch (error) {
    console.error(
      "[Testimonials] Failed to load:",
      error,
    );

    return [];
  }
}
