import { env } from "./env";

export interface LoginPayload {
  email: string;
  password: string;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

export interface RefreshPayload {
  refresh: string;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${env.VITE_API_BASE_URL}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...init?.headers
    },
    ...init
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export const api = {
  login: (payload: LoginPayload) =>
    request<TokenPair>("/auth/login", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  refresh: (payload: RefreshPayload) =>
    request<TokenPair>("/auth/refresh", {
      method: "POST",
      body: JSON.stringify(payload)
    }),
  health: () => request<{ status: string }>("/health")
};
