export interface SitePage {
  title: string;
  path: string;
  eyebrow: string;
  summary: string;
  parentPath: string | null;
  childPaths: string[];
  noindex: boolean;
}

export const sitePages: SitePage[] = [
  {
    title: "Legal",
    path: "legal",
    eyebrow: "Legal",
    summary:
      "Policies and terms governing LKProfessionals websites and commercial engagements.",
    parentPath: null,
    childPaths: [
      "legal/privacy-policy",
      "legal/terms-conditions",
      "legal/cookie-policy",
      "legal/refund-policy",
      "legal/sitemap",
    ],
    noindex: false,
  },
  {
    title: "Privacy Policy",
    path: "legal/privacy-policy",
    eyebrow: "Legal",
    summary:
      "Learn more about privacy policy within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Terms & Conditions",
    path: "legal/terms-conditions",
    eyebrow: "Legal",
    summary:
      "Learn more about terms & conditions within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Cookie Policy",
    path: "legal/cookie-policy",
    eyebrow: "Legal",
    summary:
      "Learn more about cookie policy within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Refund Policy",
    path: "legal/refund-policy",
    eyebrow: "Legal",
    summary:
      "Learn more about refund policy within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
  {
    title: "Sitemap",
    path: "legal/sitemap",
    eyebrow: "Legal",
    summary:
      "Learn more about sitemap within the LKProfessionals legal section.",
    parentPath: "legal",
    childPaths: [],
    noindex: false,
  },
];

export const sitePageByPath = new Map(
  sitePages.map((page) => [page.path, page]),
);
