import {
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import type {
  PaginationMeta,
} from "../types";

interface ProjectPaginationProps {
  pagination: PaginationMeta;
  onPageChange: (
    page: number,
  ) => void;
  onPageSizeChange: (
    pageSize: number,
  ) => void;
}

export function ProjectPagination({
  pagination,
  onPageChange,
  onPageSizeChange,
}: ProjectPaginationProps) {
  const firstItem =
    pagination.total_items === 0
      ? 0
      : (
        (pagination.page - 1)
        * pagination.page_size
      ) + 1;

  const lastItem = Math.min(
    pagination.page
      * pagination.page_size,
    pagination.total_items,
  );

  return (
    <div className="flex flex-col gap-3 rounded-xl border border-slate-200 bg-white px-4 py-3 sm:flex-row sm:items-center dark:border-slate-800 dark:bg-slate-900">
      <p className="text-sm text-slate-500 dark:text-slate-400">
        Showing{" "}
        <span className="font-medium text-slate-900 dark:text-white">
          {firstItem}–{lastItem}
        </span>{" "}
        of{" "}
        <span className="font-medium text-slate-900 dark:text-white">
          {pagination.total_items}
        </span>{" "}
        projects
      </p>

      <div className="flex items-center gap-2 sm:ml-auto">
        <select
          value={
            pagination.page_size
          }
          aria-label="Projects per page"
          onChange={(event) => {
            onPageSizeChange(
              Number(
                event.target.value,
              ),
            );
          }}
          className="h-9 rounded-md border border-slate-200 bg-white px-2 text-sm text-slate-700 outline-none dark:border-slate-700 dark:bg-slate-950 dark:text-slate-200"
        >
          {[10, 25, 50, 100].map(
            (pageSize) => (
              <option
                key={pageSize}
                value={pageSize}
              >
                {pageSize} per page
              </option>
            ),
          )}
        </select>

        <Button
          variant="outline"
          size="icon"
          disabled={
            pagination.page <= 1
          }
          onClick={() => {
            onPageChange(
              pagination.page - 1,
            );
          }}
          aria-label="Previous page"
          className="dark:border-slate-700 dark:text-slate-200"
        >
          <ChevronLeft size={17} />
        </Button>

        <span className="min-w-20 text-center text-sm text-slate-600 dark:text-slate-300">
          {pagination.page} /{" "}
          {Math.max(
            pagination.total_pages,
            1,
          )}
        </span>

        <Button
          variant="outline"
          size="icon"
          disabled={
            pagination.page
            >= pagination.total_pages
          }
          onClick={() => {
            onPageChange(
              pagination.page + 1,
            );
          }}
          aria-label="Next page"
          className="dark:border-slate-700 dark:text-slate-200"
        >
          <ChevronRight size={17} />
        </Button>
      </div>
    </div>
  );
}
