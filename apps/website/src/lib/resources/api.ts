import type {
  PublicResource,
  PublicResourcesResponse,
  ResourceType,
} from "./types";

const API_BASE_URL =
  import.meta.env.API_BASE_URL
  ?? import.meta.env.PUBLIC_API_BASE_URL
  ?? "http://127.0.0.1:8082/api/v1";

const ENDPOINT =
  `${API_BASE_URL}/resources/public`;

export async function getResources(
  resourceType?: ResourceType,
): Promise<PublicResource[]> {
  try {
    const url = new URL(ENDPOINT);

    if (resourceType) {
      url.searchParams.set(
        "resource_type",
        resourceType,
      );
    }

    const response = await fetch(url, {
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      console.error(
        `[Resources] API returned ${response.status}`,
      );

      return [];
    }

    const data: PublicResourcesResponse =
      await response.json();

    return Array.isArray(data.items)
      ? data.items
      : [];
  } catch (error) {
    console.error(
      "[Resources] Failed to load resources:",
      error,
    );

    return [];
  }
}

export async function getResource(
  slug: string,
): Promise<PublicResource | null> {
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

    const data: PublicResource =
      await response.json();

    return data;
  } catch (error) {
    console.error(
      "[Resources] Failed to load resource:",
      error,
    );

    return null;
  }
}
