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
    title: "Client Portal",
    path: "client-portal",
    eyebrow: "Client Access",
    summary:
      "Secure client access to projects, invoices, support requests and shared documents.",
    parentPath: null,
    childPaths: [
      "client-portal/login",
      "client-portal/dashboard",
      "client-portal/projects",
      "client-portal/invoices",
      "client-portal/support-tickets",
      "client-portal/documents",
    ],
    noindex: true,
  },
  {
    title: "Login",
    path: "client-portal/login",
    eyebrow: "Client Portal",
    summary:
      "Learn more about login within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Dashboard",
    path: "client-portal/dashboard",
    eyebrow: "Client Portal",
    summary:
      "Learn more about dashboard within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Projects",
    path: "client-portal/projects",
    eyebrow: "Client Portal",
    summary:
      "Learn more about projects within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Invoices",
    path: "client-portal/invoices",
    eyebrow: "Client Portal",
    summary:
      "Learn more about invoices within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Support Tickets",
    path: "client-portal/support-tickets",
    eyebrow: "Client Portal",
    summary:
      "Learn more about support tickets within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
  {
    title: "Documents",
    path: "client-portal/documents",
    eyebrow: "Client Portal",
    summary:
      "Learn more about documents within the LKProfessionals client portal section.",
    parentPath: "client-portal",
    childPaths: [],
    noindex: true,
  },
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
