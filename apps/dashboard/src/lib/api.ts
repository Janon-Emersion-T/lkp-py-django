import { z } from "zod";

import { apiRequest } from "./http";
import {
  clearTokens,
  getAccessToken,
  getRefreshToken,
  saveTokens,
  type AuthTokens,
} from "./tokens";

const tokenResponseSchema = z.object({
  access: z.string(),
  refresh: z.string(),
});

const userResponseSchema = z.object({
  id: z.number(),
  email: z.string().email(),
  username: z.string(),
  first_name: z.string(),
  last_name: z.string(),
  is_staff: z.boolean(),
});

export type TokenResponse = z.infer<typeof tokenResponseSchema>;
export type CurrentUser = z.infer<typeof userResponseSchema>;

interface LoginPayload {
  email: string;
  password: string;
}

export async function loginRequest(
  payload: LoginPayload,
): Promise<TokenResponse> {
  const response = await apiRequest<unknown>("/auth/login", {
    method: "POST",
    body: JSON.stringify(payload),
  });

  return tokenResponseSchema.parse(response);
}

export async function currentUserRequest(): Promise<CurrentUser> {
  if (!getAccessToken()) {
    throw new Error("Authentication required");
  }

  const response = await apiRequest<unknown>("/auth/me");

  return userResponseSchema.parse(response);
}

export async function logoutRequest(): Promise<void> {
  const refreshToken = getRefreshToken();

  if (!refreshToken) {
    clearTokens();
    return;
  }

  try {
    await apiRequest("/auth/logout", {
      method: "POST",
      body: JSON.stringify({
        refresh: refreshToken,
      }),
    });
  } finally {
    clearTokens();
  }
}

export {
  clearTokens,
  getAccessToken,
  saveTokens,
};

export type {
  AuthTokens,
};
