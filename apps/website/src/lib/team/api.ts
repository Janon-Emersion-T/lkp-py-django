import type {
  PublicTeam,
} from "./types";

const API_BASE_URL =
  import.meta.env.API_BASE_URL
  ?? import.meta.env.PUBLIC_API_BASE_URL
  ?? "http://127.0.0.1:8082/api/v1";

const ENDPOINT =
  `${API_BASE_URL}/team-management/public/teams`;

export async function getPublicTeams():
Promise<PublicTeam[]> {
  try {
    const response =
      await fetch(
        ENDPOINT,
        {
          headers: {
            Accept: "application/json",
          },
        },
      );

    if (!response.ok) {
      console.error(
        `[Team] API returned ${response.status}`,
      );

      return [];
    }

    const payload: unknown =
      await response.json();

    return Array.isArray(payload)
      ? payload as PublicTeam[]
      : [];
  } catch (error) {
    console.error(
      "[Team] Failed to load public teams:",
      error,
    );

    return [];
  }
}
