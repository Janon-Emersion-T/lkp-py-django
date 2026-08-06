import {
  BadgeCheck,
  CalendarClock,
  FolderKanban,
  RefreshCw,
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
  ProjectDetailPanel,
} from "../components/project-detail-panel";
import {
  ProjectFiltersBar,
} from "../components/project-filters";
import {
  ProjectKpiCard,
} from "../components/project-kpi-card";
import {
  ProjectList,
} from "../components/project-list";
import {
  ProjectPagination,
} from "../components/project-pagination";
import {
  ProjectErrorState,
  ProjectLoadingState,
} from "../components/project-states";
import {
  formatCount,
  isProjectOverdue,
} from "../formatters";
import {
  useProjects,
} from "../hooks";
import type {
  ProjectFilters,
} from "../types";

const initialFilters: ProjectFilters = {
  page: 1,
  pageSize: 25,
  search: "",
  status: "",
  priority: "",
  clientId: "",
  projectManagerId: "",
  ordering: "-created_at",
};

export function ProjectsPage() {
  const [
    filters,
    setFilters,
  ] = useState<ProjectFilters>(
    initialFilters,
  );

  const [
    selectedProjectId,
    setSelectedProjectId,
  ] = useState<string | null>(null);

  const deferredSearch =
    useDeferredValue(filters.search);

  const queryFilters = {
    ...filters,
    search: deferredSearch,
  };

  const projectsQuery =
    useProjects(queryFilters);

  const pageMetrics = useMemo(() => {
    const projects =
      projectsQuery.data?.items ?? [];

    return {
      active: projects.filter(
        (project) =>
          project.status
          !== "completed"
          && project.status
          !== "cancelled",
      ).length,
      completed: projects.filter(
        (project) =>
          project.status
          === "completed",
      ).length,
      overdue: projects.filter(
        (project) =>
          isProjectOverdue(
            project.deadline,
            project.status,
          ),
      ).length,
      teamMembers: projects.reduce(
        (total, project) =>
          total
          + project.team_members.filter(
            (member) =>
              member.is_active,
          ).length,
        0,
      ),
    };
  }, [projectsQuery.data]);

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 xl:flex-row xl:items-end xl:justify-between">
        <PageHeader
          eyebrow="Delivery operations"
          title="Projects"
          description="Manage project execution, progress, budgets, deadlines, team allocations, milestones, environments, notes, and operational events."
        />

        <Button
          variant="outline"
          onClick={() => {
            void projectsQuery.refetch();
          }}
          disabled={
            projectsQuery.isFetching
          }
          className="self-start dark:border-slate-700 dark:text-slate-200"
        >
          <RefreshCw
            size={16}
            className={
              projectsQuery.isFetching
                ? "animate-spin"
                : undefined
            }
          />

          Refresh projects
        </Button>
      </div>

      {projectsQuery.data && (
        <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <ProjectKpiCard
            label="Total projects"
            value={formatCount(
              projectsQuery.data
                .pagination
                .total_items,
            )}
            description="All projects matching the active filters"
            icon={FolderKanban}
          />

          <ProjectKpiCard
            label="Active on page"
            value={formatCount(
              pageMetrics.active,
            )}
            description="Projects still in the delivery lifecycle"
            icon={BadgeCheck}
          />

          <ProjectKpiCard
            label="Overdue on page"
            value={formatCount(
              pageMetrics.overdue,
            )}
            description="Active projects with deadlines in the past"
            icon={CalendarClock}
            attention={
              pageMetrics.overdue > 0
            }
          />

          <ProjectKpiCard
            label="Team assignments"
            value={formatCount(
              pageMetrics.teamMembers,
            )}
            description={`${formatCount(
              pageMetrics.completed,
            )} completed projects on this page`}
            icon={UsersRound}
          />
        </div>
      )}

      <ProjectFiltersBar
        filters={filters}
        onChange={setFilters}
      />

      {projectsQuery.isLoading && (
        <ProjectLoadingState />
      )}

      {projectsQuery.isError && (
        <ProjectErrorState
          error={
            projectsQuery.error
            instanceof Error
              ? projectsQuery.error
              : new Error(
                "An unknown project error occurred.",
              )
          }
          onRetry={() => {
            void projectsQuery.refetch();
          }}
        />
      )}

      {projectsQuery.data && (
        <>
          <ProjectList
            projects={
              projectsQuery.data.items
            }
            onSelect={
              setSelectedProjectId
            }
          />

          <ProjectPagination
            pagination={
              projectsQuery.data
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

      <ProjectDetailPanel
        projectId={selectedProjectId}
        onClose={() => {
          setSelectedProjectId(null);
        }}
      />
    </section>
  );
}
