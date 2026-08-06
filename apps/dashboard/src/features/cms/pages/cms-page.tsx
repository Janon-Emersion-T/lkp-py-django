import {
  BookOpenText,
  BriefcaseBusiness,
  Building2,
  FileStack,
  Layers3,
  MessageSquareQuote,
  PackageOpen,
  RefreshCw,
} from "lucide-react";
import {
  useDeferredValue,
  useState,
} from "react";

import {
  PageHeader,
} from "../../../components/layout/page-header";
import {
  Button,
} from "../../../components/ui/button";
import {
  CmsContentTable,
} from "../components/cms-content-table";
import {
  CmsDetailPanel,
} from "../components/cms-detail-panel";
import {
  CmsFiltersBar,
} from "../components/cms-filters";
import {
  CmsPagination,
} from "../components/cms-pagination";
import {
  CmsErrorState,
  CmsLoadingState,
} from "../components/cms-states";
import {
  cmsContentLabels,
} from "../formatters";
import {
  useCmsRecords,
} from "../hooks";
import type {
  CmsContentType,
  CmsDetailSelection,
  CmsFilters,
} from "../types";

const modules: Array<{
  id: CmsContentType;
  icon: typeof FileStack;
}> = [
  {
    id: "pages",
    icon: FileStack,
  },
  {
    id: "services",
    icon: BriefcaseBusiness,
  },
  {
    id: "packages",
    icon: PackageOpen,
  },
  {
    id: "industries",
    icon: Building2,
  },
  {
    id: "insights",
    icon: BookOpenText,
  },
  {
    id: "case-studies",
    icon: Layers3,
  },
  {
    id: "testimonials",
    icon: MessageSquareQuote,
  },
];

const initialFilters: CmsFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  featured: null,
  active: null,
  ordering: "-updated_at",
};

export function CmsPage() {
  const [
    type,
    setType,
  ] = useState<CmsContentType>(
    "pages",
  );

  const [
    filters,
    setFilters,
  ] = useState<CmsFilters>(
    initialFilters,
  );

  const [
    selection,
    setSelection,
  ] = useState<CmsDetailSelection | null>(
    null,
  );

  const deferredSearch =
    useDeferredValue(filters.search);

  const query = useCmsRecords(
    type,
    {
      ...filters,
      search: deferredSearch,
    },
  );

  function changeModule(
    nextType: CmsContentType,
  ) {
    setType(nextType);
    setFilters(initialFilters);
    setSelection(null);
  }

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Website content operations"
          title="CMS Content Hub"
          description="Review website pages, service catalog entries, packages, industries, insights, case studies, testimonials, publication states, visibility, and content metadata."
        />

        <Button
          variant="outline"
          onClick={() => {
            void query.refetch();
          }}
          disabled={query.isFetching}
          className="self-start dark:border-slate-700"
        >
          <RefreshCw
            size={16}
            className={
              query.isFetching
                ? "animate-spin"
                : undefined
            }
          />
          Refresh content
        </Button>
      </div>

      <nav className="overflow-x-auto rounded-xl border border-slate-200 bg-white p-2 dark:border-slate-800 dark:bg-slate-900">
        <div className="flex min-w-max gap-1">
          {modules.map((module) => {
            const Icon = module.icon;
            const active =
              module.id === type;

            return (
              <button
                key={module.id}
                type="button"
                onClick={() => {
                  changeModule(
                    module.id,
                  );
                }}
                className={
                  active
                    ? "flex items-center gap-2 rounded-lg bg-slate-950 px-4 py-2.5 text-sm font-semibold text-white dark:bg-white dark:text-slate-950"
                    : "flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium text-slate-600 transition hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
                }
              >
                <Icon size={16} />
                {
                  cmsContentLabels[
                    module.id
                  ]
                }
              </button>
            );
          })}
        </div>
      </nav>

      <CmsFiltersBar
        type={type}
        filters={filters}
        onChange={setFilters}
      />

      {query.isLoading && (
        <CmsLoadingState />
      )}

      {query.isError && (
        <CmsErrorState
          error={
            query.error
            instanceof Error
              ? query.error
              : new Error(
                "An unknown CMS error occurred.",
              )
          }
          onRetry={() => {
            void query.refetch();
          }}
        />
      )}

      {query.data && (
        <>
          <CmsContentTable
            type={type}
            records={query.data.items}
            onSelect={(
              selectedType,
              id,
            ) => {
              setSelection({
                type: selectedType,
                id,
              });
            }}
          />

          <CmsPagination
            pagination={
              query.data.pagination
            }
            onPageChange={(page) => {
              setFilters((current) => ({
                ...current,
                page,
              }));
            }}
          />
        </>
      )}

      <CmsDetailPanel
        type={selection?.type ?? type}
        recordId={selection?.id ?? null}
        onClose={() => {
          setSelection(null);
        }}
      />
    </section>
  );
}
