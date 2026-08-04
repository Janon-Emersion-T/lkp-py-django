export const colors = {
  brand: {
    primary: "#0B2F8F",
    primaryDark: "#071A3D",
    secondary: "#1746C7",
    gold: "#D4AF37",
    goldLight: "#F2D675",
  },

  background: {
    primary: "#F8F8F5",
    secondary: "#FFFFFF",
    tertiary: "#F1F5F9",
    dark: "#071A3D",
  },

  surface: {
    primary: "#FFFFFF",
    secondary: "#F8F8F5",
    elevated: "#FFFFFF",
  },

  text: {
    primary: "#111827",
    secondary: "#5B6472",
    muted: "#8B94A7",
    inverse: "#FFFFFF",
  },

  border: {
    light: "#E5E7EB",
    default: "#D1D5DB",
    dark: "#94A3B8",
  },

  state: {
    success: "#16803C",
    warning: "#B7791F",
    danger: "#C53030",
    info: "#1746C7",
  },
} as const;

export type Colors = typeof colors;
