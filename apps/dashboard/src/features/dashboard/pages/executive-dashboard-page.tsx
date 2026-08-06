import {
  BriefcaseBusiness,
  Building2,
  CircleDollarSign,
  ClockAlert,
  FileCheck2,
  FileText,
  FolderKanban,
  Inbox,
  ListChecks,
  Mail,
  Target,
  TrendingUp,
  UsersRound,
} from "lucide-react";
import {
  useMemo,
  useState,
} from "react";

import {
  PageHeader,
} from "../../../components/layout/page-header";
import {
  DashboardErrorState,
} from "../components/dashboard-error-state";
import {
  DashboardPeriodFilter,
} from "../components/dashboard-period-filter";
import {
  DashboardSkeleton,
} from "../components/dashboard-skeleton";
import {
  CurrencyList,
} from "../components/currency-list";
import {
  KpiCard,
} from "../components/kpi-card";
import {
  MetricPanel,
  MetricRow,
} from "../components/metric-panel";
import {
  formatCurrencyAmount,
  formatDashboardDate,
  formatGeneratedDate,
  formatNumber,
  formatPercentage,
} from "../formatters";
import {
  useExecutiveDashboard,
} from "../hooks";
import type {
  DashboardPeriodPreset,
} from "../types";

function getTodayDateInput(): string {
  return new Date().toISOString().slice(0, 10);
}

function getMonthStartDateInput(): string {
  const today = new Date();

  return [
    today.getFullYear(),
    String(today.getMonth() + 1).padStart(2, "0"),
    "01",
  ].join("-");
}

export function ExecutiveDashboardPage() {
  const [preset, setPreset] =
    useState<DashboardPeriodPreset>("this_month");

  const [dateFrom, setDateFrom] =
    useState(getMonthStartDateInput);

  const [dateTo, setDateTo] =
    useState(getTodayDateInput);

  const query = useMemo(
    () => ({
      preset,
      dateFrom:
        preset === "custom"
          ? dateFrom
          : undefined,
      dateTo:
        preset === "custom"
          ? dateTo
          : undefined,
      environment: "production",
    }),
    [
      preset,
      dateFrom,
      dateTo,
    ],
  );

  const dashboard = useExecutiveDashboard(query);

  const report = dashboard.data;
  const data = report?.data;

  return (
    <section className="space-y-6">
      <PageHeader
        eyebrow="Enterprise reporting"
        title="Executive Dashboard"
        description="A consolidated operating view of client growth, sales performance, delivery, finance, enquiries, and workforce capacity."
      />

      <DashboardPeriodFilter
        preset={preset}
        dateFrom={dateFrom}
        dateTo={dateTo}
        isFetching={dashboard.isFetching}
        onPresetChange={setPreset}
        onDateFromChange={setDateFrom}
        onDateToChange={setDateTo}
        onRefresh={() => {
          void dashboard.refetch();
        }}
      />

      {dashboard.isLoading && (
        <DashboardSkeleton />
      )}

      {dashboard.isError && (
        <DashboardErrorState
          error={
            dashboard.error instanceof Error
              ? dashboard.error
              : new Error(
                "An unknown dashboard error occurred.",
              )
          }
          onRetry={() => {
            void dashboard.refetch();
          }}
        />
      )}

      {report && data && (
        <>
          <div className="flex flex-col gap-2 rounded-xl border border-slate-200 bg-white px-5 py-4 text-sm sm:flex-row sm:items-center sm:justify-between dark:border-slate-800 dark:bg-slate-900">
            <div>
              <span className="font-medium text-slate-950 dark:text-white">
                {formatDashboardDate(
                  report.period.date_from,
                )}
                {" — "}
                {formatDashboardDate(
                  report.period.date_to,
                )}
              </span>

              <span className="ml-2 text-slate-500 dark:text-slate-400">
                · {report.timezone}
              </span>
            </div>

            <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 dark:text-slate-400">
              <span className="rounded-full bg-emerald-50 px-2.5 py-1 font-semibold text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300">
                {report.metadata.aggregation_status}
              </span>

              <span>
                Updated{" "}
                {formatGeneratedDate(
                  report.generated_at,
                )}
              </span>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <KpiCard
              label="Active clients"
              value={formatNumber(
                data.summary.active_clients,
              )}
              description={`${formatNumber(
                data.clients.new_clients,
              )} new clients in this period`}
              icon={Building2}
              status="positive"
            />

            <KpiCard
              label="Qualified leads"
              value={formatNumber(
                data.summary.qualified_leads,
              )}
              description={`${formatPercentage(
                data.summary.lead_conversion_rate,
              )}% all-time closed-lead conversion`}
              icon={Target}
              status="positive"
            />

            <KpiCard
              label="Open enquiries"
              value={formatNumber(
                data.summary.open_enquiries,
              )}
              description={`${formatNumber(
                data.enquiries.submitted_in_period,
              )} enquiries submitted in this period`}
              icon={Inbox}
            />

            <KpiCard
              label="Follow-ups overdue"
              value={formatNumber(
                data.summary.overdue_follow_ups,
              )}
              description="Combined CRM and enquiry follow-ups requiring attention"
              icon={ClockAlert}
              status={
                data.summary.overdue_follow_ups > 0
                  ? "attention"
                  : "positive"
              }
            />
          </div>

          <div className="grid gap-6 xl:grid-cols-2">
            <MetricPanel
              title="Client and CRM performance"
              description="Portfolio growth and lead outcomes"
              icon={UsersRound}
            >
              <MetricRow
                label="Total clients"
                value={formatNumber(
                  data.clients.total_clients,
                )}
              />

              <MetricRow
                label="Active clients"
                value={formatNumber(
                  data.clients.active_clients,
                )}
              />

              <MetricRow
                label="New clients in period"
                value={formatNumber(
                  data.clients.new_clients,
                )}
              />

              <MetricRow
                label="Total leads"
                value={formatNumber(
                  data.crm.total_leads,
                )}
              />

              <MetricRow
                label="Won leads"
                value={formatNumber(
                  data.crm.won_leads,
                )}
              />

              <MetricRow
                label="Lost leads"
                value={formatNumber(
                  data.crm.lost_leads,
                )}
                attention={data.crm.lost_leads > 0}
              />

              <MetricRow
                label="Conversion rate"
                value={`${formatPercentage(
                  data.crm.lead_conversion_rate,
                )}%`}
              />
            </MetricPanel>

            <MetricPanel
              title="Sales and quotations"
              description="Quotation volume and accepted business"
              icon={FileCheck2}
            >
              <MetricRow
                label="Total quotations"
                value={formatNumber(
                  data.sales.total_quotations,
                )}
              />

              <MetricRow
                label="Quotations in period"
                value={formatNumber(
                  data.sales.period_quotations,
                )}
              />

              <MetricRow
                label="Accepted quotations"
                value={formatNumber(
                  data.sales.accepted_quotations,
                )}
              />

              <div className="mt-5">
                <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Accepted quotation value
                </p>

                <CurrencyList
                  rows={
                    data.sales
                      .accepted_quotation_value_by_currency
                  }
                  emptyMessage="No accepted quotation value recorded"
                />
              </div>
            </MetricPanel>

            <MetricPanel
              title="Project delivery"
              description="Project portfolio execution status"
              icon={FolderKanban}
            >
              <MetricRow
                label="Active projects"
                value={formatNumber(
                  data.projects.active_projects,
                )}
              />

              <MetricRow
                label="Completed projects"
                value={formatNumber(
                  data.projects.completed_projects,
                )}
              />

              <MetricRow
                label="Completed in period"
                value={formatNumber(
                  data.projects.completed_in_period,
                )}
              />

              <MetricRow
                label="Overdue projects"
                value={formatNumber(
                  data.projects.overdue_projects,
                )}
                attention={
                  data.projects.overdue_projects > 0
                }
              />
            </MetricPanel>

            <MetricPanel
              title="Task execution"
              description="Workload and delivery follow-through"
              icon={ListChecks}
            >
              <MetricRow
                label="Open tasks"
                value={formatNumber(
                  data.tasks.open_tasks,
                )}
              />

              <MetricRow
                label="Completed tasks"
                value={formatNumber(
                  data.tasks.completed_tasks,
                )}
              />

              <MetricRow
                label="Completed in period"
                value={formatNumber(
                  data.tasks.completed_in_period,
                )}
              />

              <MetricRow
                label="Overdue tasks"
                value={formatNumber(
                  data.tasks.overdue_tasks,
                )}
                attention={
                  data.tasks.overdue_tasks > 0
                }
              />
            </MetricPanel>
          </div>

          <div className="grid gap-6 xl:grid-cols-[1.35fr_1fr]">
            <MetricPanel
              title="Finance overview"
              description="Revenue, receivables, and liquid account balances"
              icon={CircleDollarSign}
            >
              <div className="grid gap-5 md:grid-cols-2">
                <div>
                  <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Revenue collected
                  </p>

                  <CurrencyList
                    rows={
                      data.finance.revenue_by_currency
                    }
                    emptyMessage="No completed payments in this period"
                  />
                </div>

                <div>
                  <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
                    Outstanding receivables
                  </p>

                  <CurrencyList
                    rows={
                      data.finance
                        .outstanding_value_by_currency
                    }
                    emptyMessage="No outstanding receivables"
                  />
                </div>
              </div>

              <div className="mt-5 grid gap-4 sm:grid-cols-2">
                <div className="rounded-lg bg-slate-50 px-4 py-3 dark:bg-slate-800/70">
                  <p className="text-xs text-slate-500 dark:text-slate-400">
                    Outstanding invoices
                  </p>

                  <p className="mt-1 text-xl font-bold text-slate-950 dark:text-white">
                    {formatNumber(
                      data.finance.outstanding_invoices,
                    )}
                  </p>
                </div>

                <div className="rounded-lg bg-amber-50 px-4 py-3 dark:bg-amber-950/30">
                  <p className="text-xs text-amber-700 dark:text-amber-400">
                    Overdue invoices
                  </p>

                  <p className="mt-1 text-xl font-bold text-amber-900 dark:text-amber-300">
                    {formatNumber(
                      data.finance.overdue_invoices,
                    )}
                  </p>
                </div>
              </div>

              <div className="mt-5">
                <p className="mb-3 text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Cash and bank accounts
                </p>

                {data.finance.cash_and_bank_balances.length ===
                0 ? (
                  <p className="rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No active asset account balances
                  </p>
                ) : (
                  <div className="overflow-hidden rounded-lg border border-slate-200 dark:border-slate-700">
                    {data.finance.cash_and_bank_balances.map(
                      (account) => (
                        <div
                          key={account.id}
                          className="flex items-center justify-between gap-4 border-b border-slate-200 px-4 py-3 last:border-b-0 dark:border-slate-700"
                        >
                          <div className="min-w-0">
                            <p className="truncate text-sm font-medium text-slate-900 dark:text-white">
                              {account.name}
                            </p>

                            <p className="text-xs text-slate-500 dark:text-slate-400">
                              {account.currency}
                            </p>
                          </div>

                          <p className="shrink-0 text-sm font-semibold text-slate-950 dark:text-white">
                            {formatCurrencyAmount(
                              account.current_balance,
                              account.currency,
                            )}
                          </p>
                        </div>
                      ),
                    )}
                  </div>
                )}
              </div>
            </MetricPanel>

            <div className="space-y-6">
              <MetricPanel
                title="Enquiry operations"
                description="Contact and quotation enquiry workload"
                icon={Mail}
              >
                <MetricRow
                  label="Open enquiries"
                  value={formatNumber(
                    data.enquiries.open_enquiries,
                  )}
                />

                <MetricRow
                  label="Submitted in period"
                  value={formatNumber(
                    data.enquiries.submitted_in_period,
                  )}
                />

                <MetricRow
                  label="Overdue follow-ups"
                  value={formatNumber(
                    data.enquiries.overdue_follow_ups,
                  )}
                  attention={
                    data.enquiries.overdue_follow_ups > 0
                  }
                />

                <MetricRow
                  label="Open contact enquiries"
                  value={formatNumber(
                    data.enquiries
                      .contact_enquiries
                      .open_count,
                  )}
                />

                <MetricRow
                  label="Open quote enquiries"
                  value={formatNumber(
                    data.enquiries
                      .quote_enquiries
                      .open_count,
                  )}
                />
              </MetricPanel>

              <MetricPanel
                title="Workforce and reach"
                description="Team capacity and organisational pipeline"
                icon={BriefcaseBusiness}
              >
                <MetricRow
                  label="Active team members"
                  value={formatNumber(
                    data.workforce.active_team_members,
                  )}
                />

                <MetricRow
                  label="Open job listings"
                  value={formatNumber(
                    data.workforce.open_job_listings,
                  )}
                />

                <MetricRow
                  label="Open job positions"
                  value={formatNumber(
                    data.workforce.open_job_positions,
                  )}
                />

                <MetricRow
                  label="Newsletter subscribers"
                  value={formatNumber(
                    data.workforce
                      .newsletter_subscribers,
                  )}
                />
              </MetricPanel>
            </div>
          </div>

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            <KpiCard
              label="Total quotations"
              value={formatNumber(
                data.sales.total_quotations,
              )}
              description={`${formatNumber(
                data.sales.accepted_quotations,
              )} accepted quotations`}
              icon={FileText}
            />

            <KpiCard
              label="Active projects"
              value={formatNumber(
                data.projects.active_projects,
              )}
              description={`${formatNumber(
                data.projects.completed_in_period,
              )} completed during this period`}
              icon={FolderKanban}
            />

            <KpiCard
              label="Open tasks"
              value={formatNumber(
                data.tasks.open_tasks,
              )}
              description={`${formatNumber(
                data.tasks.overdue_tasks,
              )} currently overdue`}
              icon={ListChecks}
              status={
                data.tasks.overdue_tasks > 0
                  ? "attention"
                  : "default"
              }
            />

            <KpiCard
              label="Won leads"
              value={formatNumber(
                data.summary.won_leads,
              )}
              description={`${formatNumber(
                data.summary.lost_leads,
              )} leads recorded as lost`}
              icon={TrendingUp}
              status="positive"
            />
          </div>
        </>
      )}
    </section>
  );
}
