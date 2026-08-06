import {
  ClockAlert,
  RefreshCw,
  Target,
  Trophy,
  UserRoundX,
  UsersRound,
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
  CrmKpiCard,
} from "../components/crm-kpi-card";
import {
  CrmErrorState,
  CrmLoadingState,
} from "../components/crm-states";
import {
  LeadDetailPanel,
} from "../components/lead-detail-panel";
import {
  LeadFiltersBar,
} from "../components/lead-filters";
import {
  LeadList,
} from "../components/lead-list";
import {
  LeadPagination,
} from "../components/lead-pagination";
import {
  formatCount,
  formatPercentage,
} from "../formatters";
import {
  useCrmReport,
  useLeads,
} from "../hooks";
import type {
  LeadFilters,
} from "../types";

const initialFilters: LeadFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  source: "",
  country: "",
  ordering: "-created_at",
};

export function CrmPage() {
  const [
    filters,
    setFilters,
  ] = useState<LeadFilters>(
    initialFilters,
  );

  const [
    selectedLeadId,
    setSelectedLeadId,
  ] = useState<string | null>(null);

  const deferredSearch =
    useDeferredValue(filters.search);

  const queryFilters = {
    ...filters,
    search: deferredSearch,
  };

  const leadsQuery =
    useLeads(queryFilters);

  const reportQuery =
    useCrmReport();

  const summary =
    reportQuery.data?.data.summary;

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Sales operations"
          title="CRM Leads"
          description="Manage prospects, lead quality, sales follow-ups, opportunity value, ownership, and conversion progress."
        />

        <Button
          variant="outline"
          onClick={() => {
            void Promise.all([
              leadsQuery.refetch(),
              reportQuery.refetch(),
            ]);
          }}
          disabled={
            leadsQuery.isFetching
            || reportQuery.isFetching
          }
          className="self-start dark:border-slate-700 dark:text-slate-200"
        >
          <RefreshCw
            size={16}
            className={
              leadsQuery.isFetching
              || reportQuery.isFetching
                ? "animate-spin"
                : undefined
            }
          />
          Refresh CRM
        </Button>
      </div>

      {summary && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">
          <CrmKpiCard
            label="Leads this month"
            value={formatCount(
              summary.total_leads,
            )}
            description={`${formatCount(
              summary.new_leads,
            )} currently at the new stage`}
            icon={UsersRound}
          />

          <CrmKpiCard
            label="Won leads"
            value={formatCount(
              summary.won_leads,
            )}
            description={`${formatPercentage(
              summary.conversion_rate,
            )} conversion rate`}
            icon={Trophy}
          />

          <CrmKpiCard
            label="In negotiation"
            value={formatCount(
              summary.negotiation_leads,
            )}
            description={`${formatCount(
              summary.proposal_sent_leads,
            )} proposals sent`}
            icon={Target}
          />

          <CrmKpiCard
            label="Overdue follow-ups"
            value={formatCount(
              summary.overdue_follow_ups,
            )}
            description="Open sales actions requiring attention"
            icon={ClockAlert}
            attention={
              summary.overdue_follow_ups > 0
            }
          />

          <CrmKpiCard
            label="Unassigned leads"
            value={formatCount(
              summary.unassigned_leads,
            )}
            description="Leads without an accountable owner"
            icon={UserRoundX}
            attention={
              summary.unassigned_leads > 0
            }
          />
        </div>
      )}

      <LeadFiltersBar
        filters={filters}
        onChange={setFilters}
      />

      {leadsQuery.isLoading && (
        <CrmLoadingState />
      )}

      {leadsQuery.isError && (
        <CrmErrorState
          error={
            leadsQuery.error instanceof Error
              ? leadsQuery.error
              : new Error(
                "An unknown CRM error occurred.",
              )
          }
          onRetry={() => {
            void leadsQuery.refetch();
          }}
        />
      )}

      {leadsQuery.data && (
        <>
          <LeadList
            leads={leadsQuery.data.items}
            onSelect={setSelectedLeadId}
          />

          <LeadPagination
            pagination={
              leadsQuery.data.pagination
            }
            onPageChange={(page) => {
              setFilters((current) => ({
                ...current,
                page,
              }));
            }}
            onPageSizeChange={(pageSize) => {
              setFilters((current) => ({
                ...current,
                page: 1,
                pageSize,
              }));
            }}
          />
        </>
      )}

      <LeadDetailPanel
        leadId={selectedLeadId}
        onClose={() => {
          setSelectedLeadId(null);
        }}
      />
    </section>
  );
}
