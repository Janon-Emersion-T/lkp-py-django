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

export function FinancePagination({
  pagination,
  onPageChange,
}: {
  pagination: PaginationMeta;
  onPageChange: (page: number) => void;
}) {
  return (
    <div className="flex items-center justify-between gap-4 rounded-xl border border-slate-200 bg-white px-4 py-3 dark:border-slate-800 dark:bg-slate-900">
      <p className="text-sm text-slate-500 dark:text-slate-400">
        {pagination.total_items} records
      </p>

      <div className="flex items-center gap-2">
        <Button
          variant="outline"
          size="icon"
          disabled={pagination.page <= 1}
          onClick={() => {
            onPageChange(
              pagination.page - 1,
            );
          }}
          aria-label="Previous page"
          className="dark:border-slate-700"
        >
          <ChevronLeft size={16} />
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
          className="dark:border-slate-700"
        >
          <ChevronRight size={16} />
        </Button>
      </div>
    </div>
  );
}
