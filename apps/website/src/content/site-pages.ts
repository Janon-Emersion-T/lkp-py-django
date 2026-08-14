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
];

export const sitePageByPath = new Map(
  sitePages.map((page) => [page.path, page]),
);
