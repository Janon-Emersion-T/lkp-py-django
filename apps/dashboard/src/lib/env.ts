import { z } from "zod";

const envSchema = z.object({
  VITE_API_BASE_URL: z.string().min(1).default("/api"),
  VITE_SENTRY_DSN: z.string().optional()
});

export const env = envSchema.parse(import.meta.env);
