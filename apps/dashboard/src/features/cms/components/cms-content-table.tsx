import {
  ChevronRight,
  Eye,
  Star,
} from "lucide-react";

import {
  formatCurrency,
  formatDateTime,
  getCmsSlug,
  getCmsSubtitle,
  getCmsTitle,
} from "../formatters";
import type {
  CmsContentType,
  CmsRecord,
} from "../types";
import {
  ContentStatusBadge,
} from "./content-status-badge";

function getCommercialValue(
  record: CmsRecord,
): string | null {
  if ("price" in record) {
    return formatCurrency(
      record.price,
      record.currency,
    );
  }

  if ("rating" in record) {
    return `${record.rating}/5 rating`;
  }

  if ("view_count" in record) {
    return `${record.view_count} views`;
  }

  return null;
}

export function CmsContentTable({
  type,
  records,
  onSelect,
}: {
  type: CmsContentType;
  records: CmsRecord[];
  onSelect: (
    type: CmsContentType,
    id: string,
  ) => void;
}) {
  if (records.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-16 text-center dark:border-slate-700 dark:bg-slate-900">
        <p className="font-medium text-slate-700 dark:text-slate-300">
          No content matched the filters.
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <table className="w-full min-w-[1000px]">
        <thead className="bg-slate-50 text-left text-xs uppercase tracking-wider text-slate-500 dark:bg-slate-800/70">
          <tr>
            <th className="px-5 py-3">
              Content
            </th>
            <th className="px-5 py-3">
              Status
            </th>
            <th className="px-5 py-3">
              Visibility
            </th>
            <th className="px-5 py-3">
              Commercial / engagement
            </th>
            <th className="px-5 py-3">
              Updated
            </th>
            <th className="w-12 px-3 py-3" />
          </tr>
        </thead>

        <tbody>
          {records.map((record) => {
            const subtitle =
              getCmsSubtitle(record);

            const slug =
              getCmsSlug(record);

            const commercial =
              getCommercialValue(record);

            return (
              <tr
                key={record.id}
                className="border-t border-slate-200 dark:border-slate-800"
              >
                <td className="max-w-xl px-5 py-4">
                  <button
                    type="button"
                    onClick={() => {
                      onSelect(
                        type,
                        record.id,
                      );
                    }}
                    className="text-left"
                  >
                    <p className="font-semibold text-slate-950 hover:text-blue-700 dark:text-white">
                      {getCmsTitle(record)}
                    </p>

                    {slug && (
                      <p className="mt-1 text-xs text-slate-500">
                        /{slug}
                      </p>
                    )}

                    {subtitle && (
                      <p className="mt-2 line-clamp-2 text-sm text-slate-600 dark:text-slate-300">
                        {subtitle}
                      </p>
                    )}
                  </button>
                </td>

                <td className="px-5 py-4">
                  <ContentStatusBadge
                    status={record.status}
                  />
                </td>

                <td className="px-5 py-4">
                  <div className="flex flex-wrap gap-2">
                    {record.is_active && (
                      <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-700 dark:text-emerald-400">
                        <Eye size={13} />
                        Active
                      </span>
                    )}

                    {record.is_featured && (
                      <span className="inline-flex items-center gap-1 text-xs font-medium text-amber-700 dark:text-amber-400">
                        <Star size={13} />
                        Featured
                      </span>
                    )}
                  </div>
                </td>

                <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                  {commercial ?? "—"}
                </td>

                <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                  {formatDateTime(
                    record.updated_at,
                  )}
                </td>

                <td className="px-3 py-4">
                  <button
                    type="button"
                    onClick={() => {
                      onSelect(
                        type,
                        record.id,
                      );
                    }}
                    aria-label="View content"
                  >
                    <ChevronRight
                      size={17}
                      className="text-slate-400"
                    />
                  </button>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
