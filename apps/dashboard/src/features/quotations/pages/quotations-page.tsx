import {
  BadgeCheck,
  ClockAlert,
  FileText,
  RefreshCw,
  Send,
} from "lucide-react";
import {
  useDeferredValue,
  useMemo,
  useState,
} from "react";

import {
  PageHeader,
} from "../../../components/layout/page-header";
import {
  Button,
} from "../../../components/ui/button";
import {
  QuotationDetailPanel,
} from "../components/quotation-detail-panel";
import {
  QuotationFiltersBar,
} from "../components/quotation-filters";
import {
  QuotationKpiCard,
} from "../components/quotation-kpi-card";
import {
  QuotationList,
} from "../components/quotation-list";
import {
  QuotationPagination,
} from "../components/quotation-pagination";
import {
  QuotationErrorState,
  QuotationLoadingState,
} from "../components/quotation-states";
import {
  formatCount,
  formatCurrency,
} from "../formatters";
import {
  useQuotations,
} from "../hooks";
import type {
  QuotationFilters,
} from "../types";

const initialFilters: QuotationFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  clientId: "",
  currency: "",
  ordering: "-created_at",
};

export function QuotationsPage() {
  const [
    filters,
    setFilters,
  ] = useState<QuotationFilters>(
    initialFilters,
  );

  const [
    selectedQuotationId,
    setSelectedQuotationId,
  ] = useState<string | null>(null);

  const deferredSearch =
    useDeferredValue(filters.search);

  const queryFilters = {
    ...filters,
    search: deferredSearch,
  };

  const quotationsQuery =
    useQuotations(queryFilters);

  const pageMetrics = useMemo(() => {
    const quotations =
      quotationsQuery.data?.items ?? [];

    const accepted = quotations.filter(
      (quotation) =>
        quotation.status
        === "accepted",
    );

    const pending = quotations.filter(
      (quotation) =>
        [
          "draft",
          "sent",
          "viewed",
        ].includes(quotation.status),
    );

    const expired = quotations.filter(
      (quotation) =>
        quotation.is_expired
        || quotation.status
          === "expired",
    );

    const currencies =
      new Set(
        accepted.map(
          (quotation) =>
            quotation.currency,
        ),
      );

    const acceptedValue =
      currencies.size === 1
        ? accepted.reduce(
          (total, quotation) =>
            total
            + Number(
              quotation.total_amount,
            ),
          0,
        )
        : null;

    const acceptedCurrency =
      accepted[0]?.currency ?? "LKR";

    return {
      acceptedCount: accepted.length,
      pendingCount: pending.length,
      expiredCount: expired.length,
      acceptedValue,
      acceptedCurrency,
    };
  }, [quotationsQuery.data]);

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Sales documents"
          title="Quotations"
          description="Track quotation value, validity, recipients, delivery events, acceptance status, line items, discounts, and tax."
        />

        <Button
          variant="outline"
          onClick={() => {
            void quotationsQuery.refetch();
          }}
          disabled={
            quotationsQuery.isFetching
          }
          className="self-start dark:border-slate-700 dark:text-slate-200"
        >
          <RefreshCw
            size={16}
            className={
              quotationsQuery.isFetching
                ? "animate-spin"
                : undefined
            }
          />

          Refresh quotations
        </Button>
      </div>

      {quotationsQuery.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <QuotationKpiCard
            label="Total quotations"
            value={formatCount(
              quotationsQuery.data
                .pagination
                .total_items,
            )}
            description="All quotations matching the active filters"
            icon={FileText}
          />

          <QuotationKpiCard
            label="Pending on page"
            value={formatCount(
              pageMetrics.pendingCount,
            )}
            description="Draft, sent, and viewed quotations on this page"
            icon={Send}
          />

          <QuotationKpiCard
            label="Accepted on page"
            value={formatCount(
              pageMetrics.acceptedCount,
            )}
            description={
              pageMetrics.acceptedValue
                !== null
                ? formatCurrency(
                  String(
                    pageMetrics.acceptedValue,
                  ),
                  pageMetrics
                    .acceptedCurrency,
                )
                : "Accepted quotations span multiple currencies"
            }
            icon={BadgeCheck}
          />

          <QuotationKpiCard
            label="Expired on page"
            value={formatCount(
              pageMetrics.expiredCount,
            )}
            description="Expired or past-validity quotations requiring review"
            icon={ClockAlert}
            attention={
              pageMetrics.expiredCount > 0
            }
          />
        </div>
      )}

      <QuotationFiltersBar
        filters={filters}
        onChange={setFilters}
      />

      {quotationsQuery.isLoading && (
        <QuotationLoadingState />
      )}

      {quotationsQuery.isError && (
        <QuotationErrorState
          error={
            quotationsQuery.error
            instanceof Error
              ? quotationsQuery.error
              : new Error(
                "An unknown quotation error occurred.",
              )
          }
          onRetry={() => {
            void quotationsQuery.refetch();
          }}
        />
      )}

      {quotationsQuery.data && (
        <>
          <QuotationList
            quotations={
              quotationsQuery.data.items
            }
            onSelect={
              setSelectedQuotationId
            }
          />

          <QuotationPagination
            pagination={
              quotationsQuery.data
                .pagination
            }
            onPageChange={(page) => {
              setFilters(
                (current) => ({
                  ...current,
                  page,
                }),
              );
            }}
            onPageSizeChange={(
              pageSize,
            ) => {
              setFilters(
                (current) => ({
                  ...current,
                  page: 1,
                  pageSize,
                }),
              );
            }}
          />
        </>
      )}

      <QuotationDetailPanel
        quotationId={
          selectedQuotationId
        }
        onClose={() => {
          setSelectedQuotationId(
            null,
          );
        }}
      />
    </section>
  );
}
