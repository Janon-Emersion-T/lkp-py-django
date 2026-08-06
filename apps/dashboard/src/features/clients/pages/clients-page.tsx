import {
  Building2,
  Globe2,
  RefreshCw,
  UserRoundCheck,
  UsersRound,
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
  ClientDetailPanel,
} from "../components/client-detail-panel";
import {
  ClientFiltersBar,
} from "../components/client-filters";
import {
  ClientKpiCard,
} from "../components/client-kpi-card";
import {
  ClientList,
} from "../components/client-list";
import {
  ClientPagination,
} from "../components/client-pagination";
import {
  ClientErrorState,
  ClientLoadingState,
} from "../components/client-states";
import {
  formatCount,
} from "../formatters";
import {
  useClients,
} from "../hooks";
import type {
  ClientFilters,
} from "../types";

const initialFilters: ClientFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  clientType: "",
  country: "",
  industry: "",
  ordering: "company_name",
};

export function ClientsPage() {
  const [
    filters,
    setFilters,
  ] = useState<ClientFilters>(
    initialFilters,
  );

  const [
    selectedClientId,
    setSelectedClientId,
  ] = useState<string | null>(null);

  const deferredSearch =
    useDeferredValue(filters.search);

  const queryFilters = {
    ...filters,
    search: deferredSearch,
  };

  const clientsQuery =
    useClients(queryFilters);

  const clientMetrics = useMemo(() => {
    const clients =
      clientsQuery.data?.items ?? [];

    return {
      active: clients.filter(
        (client) =>
          client.status === "active",
      ).length,
      contacts: clients.reduce(
        (total, client) =>
          total
          + client.contacts.length,
        0,
      ),
      websites: clients.reduce(
        (total, client) =>
          total
          + client.websites.length,
        0,
      ),
    };
  }, [clientsQuery.data]);

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Account management"
          title="Clients"
          description="Manage client organisations, commercial details, contacts, managed websites, payment terms, and lead conversion history."
        />

        <Button
          variant="outline"
          onClick={() => {
            void clientsQuery.refetch();
          }}
          disabled={
            clientsQuery.isFetching
          }
          className="self-start dark:border-slate-700 dark:text-slate-200"
        >
          <RefreshCw
            size={16}
            className={
              clientsQuery.isFetching
                ? "animate-spin"
                : undefined
            }
          />

          Refresh clients
        </Button>
      </div>

      {clientsQuery.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <ClientKpiCard
            label="Total clients"
            value={formatCount(
              clientsQuery.data
                .pagination
                .total_items,
            )}
            description="All client records matching the active filters"
            icon={Building2}
          />

          <ClientKpiCard
            label="Active on page"
            value={formatCount(
              clientMetrics.active,
            )}
            description="Active client accounts in the current result page"
            icon={UserRoundCheck}
          />

          <ClientKpiCard
            label="Contacts on page"
            value={formatCount(
              clientMetrics.contacts,
            )}
            description="Recorded client contacts in the current result page"
            icon={UsersRound}
          />

          <ClientKpiCard
            label="Websites on page"
            value={formatCount(
              clientMetrics.websites,
            )}
            description="Managed website records in the current result page"
            icon={Globe2}
          />
        </div>
      )}

      <ClientFiltersBar
        filters={filters}
        onChange={setFilters}
      />

      {clientsQuery.isLoading && (
        <ClientLoadingState />
      )}

      {clientsQuery.isError && (
        <ClientErrorState
          error={
            clientsQuery.error
            instanceof Error
              ? clientsQuery.error
              : new Error(
                "An unknown client error occurred.",
              )
          }
          onRetry={() => {
            void clientsQuery.refetch();
          }}
        />
      )}

      {clientsQuery.data && (
        <>
          <ClientList
            clients={
              clientsQuery.data.items
            }
            onSelect={
              setSelectedClientId
            }
          />

          <ClientPagination
            pagination={
              clientsQuery.data
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

      <ClientDetailPanel
        clientId={selectedClientId}
        onClose={() => {
          setSelectedClientId(null);
        }}
      />
    </section>
  );
}
