import {
  Building2,
  CalendarClock,
  ChevronRight,
  FolderKanban,
  Inbox,
  UserRound,
  UsersRound,
} from "lucide-react";

import {
  formatCurrency,
  formatDate,
  formatUserName,
  isProjectOverdue,
} from "../formatters";
import type {
  Project,
} from "../types";
import {
  ProjectPriorityBadge,
  ProjectStatusBadge,
} from "./project-badges";
import {
  ProjectProgress,
} from "./project-progress";

interface ProjectListProps {
  projects: Project[];
  onSelect: (
    projectId: string,
  ) => void;
}

export function ProjectList({
  projects,
  onSelect,
}: ProjectListProps) {
  if (projects.length === 0) {
    return (
      <section className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center dark:border-slate-700 dark:bg-slate-900">
        <Inbox
          size={30}
          className="mx-auto text-slate-300 dark:text-slate-600"
        />

        <h2 className="mt-4 font-semibold text-slate-950 dark:text-white">
          No projects found
        </h2>

        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          No projects match the current search and filters.
        </p>
      </section>
    );
  }

  return (
    <>
      <section className="hidden overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm lg:block dark:border-slate-800 dark:bg-slate-900">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[1120px] border-collapse">
            <thead className="bg-slate-50 dark:bg-slate-800/70">
              <tr className="text-left text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                <th className="px-5 py-3">
                  Project
                </th>
                <th className="px-5 py-3">
                  Client
                </th>
                <th className="px-5 py-3">
                  Status
                </th>
                <th className="px-5 py-3">
                  Manager
                </th>
                <th className="px-5 py-3">
                  Progress
                </th>
                <th className="px-5 py-3">
                  Deadline
                </th>
                <th className="px-5 py-3">
                  Budget
                </th>
                <th className="px-5 py-3">
                  Team
                </th>
                <th className="w-12 px-3 py-3">
                  <span className="sr-only">
                    View
                  </span>
                </th>
              </tr>
            </thead>

            <tbody>
              {projects.map((project) => {
                const overdue =
                  isProjectOverdue(
                    project.deadline,
                    project.status,
                  );

                return (
                  <tr
                    key={project.id}
                    className="border-t border-slate-200 transition hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/50"
                  >
                    <td className="px-5 py-4">
                      <button
                        type="button"
                        onClick={() => {
                          onSelect(project.id);
                        }}
                        className="text-left"
                      >
                        <p className="font-medium text-slate-950 hover:text-blue-700 dark:text-white dark:hover:text-blue-400">
                          {project.title}
                        </p>

                        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                          {project.project_code}
                        </p>

                        <div className="mt-1">
                          <ProjectPriorityBadge
                            priority={
                              project.priority
                            }
                          />
                        </div>
                      </button>
                    </td>

                    <td className="px-5 py-4">
                      <span className="inline-flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                        <Building2
                          size={15}
                          className="text-slate-400"
                        />

                        <span className="max-w-44 truncate">
                          {project.client_name}
                        </span>
                      </span>
                    </td>

                    <td className="px-5 py-4">
                      <ProjectStatusBadge
                        status={project.status}
                      />
                    </td>

                    <td className="px-5 py-4">
                      <span className="inline-flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                        <UserRound
                          size={15}
                          className="text-slate-400"
                        />

                        <span className="max-w-40 truncate">
                          {formatUserName(
                            project.project_manager,
                          )}
                        </span>
                      </span>
                    </td>

                    <td className="px-5 py-4">
                      <ProjectProgress
                        progress={
                          project.progress
                        }
                        compact
                      />
                    </td>

                    <td className="px-5 py-4">
                      <p
                        className={
                          overdue
                            ? "text-sm font-semibold text-amber-700 dark:text-amber-400"
                            : "text-sm text-slate-600 dark:text-slate-300"
                        }
                      >
                        {formatDate(
                          project.deadline,
                        )}
                      </p>

                      {overdue && (
                        <p className="mt-1 text-xs text-amber-700 dark:text-amber-400">
                          Overdue
                        </p>
                      )}
                    </td>

                    <td className="px-5 py-4 text-sm font-semibold text-slate-950 dark:text-white">
                      {formatCurrency(
                        project.budget,
                        project.currency,
                      )}
                    </td>

                    <td className="px-5 py-4">
                      <span className="inline-flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                        <UsersRound
                          size={15}
                          className="text-slate-400"
                        />
                        {
                          project.team_members
                            .filter(
                              (member) =>
                                member.is_active,
                            )
                            .length
                        }
                      </span>
                    </td>

                    <td className="px-3 py-4">
                      <button
                        type="button"
                        onClick={() => {
                          onSelect(project.id);
                        }}
                        aria-label={`View ${project.project_code}`}
                        className="grid h-8 w-8 place-items-center rounded-md text-slate-400 transition hover:bg-slate-100 hover:text-slate-950 dark:hover:bg-slate-700 dark:hover:text-white"
                      >
                        <ChevronRight
                          size={17}
                        />
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid gap-3 lg:hidden">
        {projects.map((project) => {
          const overdue =
            isProjectOverdue(
              project.deadline,
              project.status,
            );

          return (
            <button
              key={project.id}
              type="button"
              onClick={() => {
                onSelect(project.id);
              }}
              className="rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:border-blue-300 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-blue-800"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="truncate font-semibold text-slate-950 dark:text-white">
                    {project.title}
                  </p>

                  <p className="mt-1 flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
                    <FolderKanban size={13} />
                    {project.project_code}
                  </p>
                </div>

                <ChevronRight
                  size={18}
                  className="shrink-0 text-slate-400"
                />
              </div>

              <div className="mt-4 flex flex-wrap items-center gap-2">
                <ProjectStatusBadge
                  status={project.status}
                />

                <ProjectPriorityBadge
                  priority={project.priority}
                />

                <span className="ml-auto text-sm font-semibold text-slate-950 dark:text-white">
                  {formatCurrency(
                    project.budget,
                    project.currency,
                  )}
                </span>
              </div>

              <div className="mt-4">
                <ProjectProgress
                  progress={project.progress}
                />
              </div>

              <div className="mt-4 grid gap-2 border-t border-slate-100 pt-3 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
                <span className="flex items-center gap-2">
                  <Building2 size={13} />
                  {project.client_name}
                </span>

                <span
                  className={
                    overdue
                      ? "flex items-center gap-2 font-semibold text-amber-700 dark:text-amber-400"
                      : "flex items-center gap-2"
                  }
                >
                  <CalendarClock size={13} />
                  Deadline{" "}
                  {formatDate(
                    project.deadline,
                  )}
                </span>
              </div>
            </button>
          );
        })}
      </section>
    </>
  );
}
