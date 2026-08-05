import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  saveTokens,
  type AuthTokens,
} from "./tokens";

const apiBaseUrl =
  import.meta.env.VITE_API_BASE_URL ??
  "http://127.0.0.1:8082/api/v1";

interface ApiErrorBody {
  detail?: string;
  message?: string;
}

export class ApiError extends Error {
  readonly status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function parseError(response: Response): Promise<ApiError> {
  const body = (await response.json().catch(() => ({}))) as ApiErrorBody;

  return new ApiError(
    body.detail ??
      body.message ??
      `Request failed with status ${response.status}`,
    response.status,
  );
}

async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    return null;
  }

  const response = await fetch(`${apiBaseUrl}/auth/refresh`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      refresh: refreshToken,
    }),
  });

  if (!response.ok) {
    clearTokens();
    return null;
  }

  const tokens = (await response.json()) as AuthTokens;
  saveTokens(tokens);

  return tokens.access;
}

export async function apiRequest<T>(
  path: string,
  options: RequestInit = {},
  retryAfterRefresh = true,
): Promise<T> {
  const accessToken = getAccessToken();

  const headers = new Headers(options.headers);

  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }

  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }

  const response = await fetch(`${apiBaseUrl}${path}`, {
    ...options,
    headers,
  });

  if (response.status === 401 && retryAfterRefresh) {
    const refreshedAccessToken = await refreshAccessToken();

    if (refreshedAccessToken) {
      return apiRequest<T>(path, options, false);
    }
  }

  if (!response.ok) {
    throw await parseError(response);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}
