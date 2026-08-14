import type {
  PortfolioProject,
  PortfolioResponse,
} from "./types";

const API_BASE_URL =
  import.meta.env.API_BASE_URL
  ?? import.meta.env.PUBLIC_API_BASE_URL
  ?? "http://127.0.0.1:8082/api/v1";

const ENDPOINT =
  `${API_BASE_URL}/case-studies/public`;

export async function getPortfolioProjects(
  serviceSlug?: string,
): Promise<PortfolioProject[]> {
  try {
    const url = new URL(ENDPOINT);

    if (serviceSlug) {
      url.searchParams.set(
        "service_slug",
        serviceSlug,
      );
    }

    const response = await fetch(url, {
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      console.error(
        `[Portfolio] API returned ${response.status}`,
      );

      return [];
    }

    const data =
      await response.json() as PortfolioResponse;

    return Array.isArray(data.items)
      ? data.items
      : [];
  } catch (error) {
    console.error(
      "[Portfolio] Failed to load projects:",
      error,
    );

    return [];
  }
}

export async function getPortfolioProject(
  slug: string,
): Promise<PortfolioProject | null> {
  try {
    const response = await fetch(
      `${ENDPOINT}/${encodeURIComponent(slug)}`,
      {
        headers: {
          Accept: "application/json",
        },
      },
    );

    if (!response.ok) {
      return null;
    }

    return await response.json() as PortfolioProject;
  } catch (error) {
    console.error(
      "[Portfolio] Failed to load project:",
      error,
    );

    return null;
  }
}
