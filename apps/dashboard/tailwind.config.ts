import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#f5f7fb",
        foreground: "#0f172a",
        primary: "#0f3d5e",
        accent: "#d6a35f",
        card: "#ffffff",
        border: "#d8e0eb"
      },
      boxShadow: {
        panel: "0 24px 60px -32px rgba(15, 23, 42, 0.25)"
      }
    }
  },
  plugins: []
} satisfies Config;

