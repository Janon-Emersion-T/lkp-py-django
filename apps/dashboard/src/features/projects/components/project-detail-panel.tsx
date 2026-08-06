import {
  Building2,
  CalendarDays,
  CheckCircle2,
  CircleDollarSign,
  Code2,
  ExternalLink,
  FileText,
  Globe2,
  Pin,
  Quote,
  Server,
  UserRound,
  UsersRound,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  formatCurrency,
  formatDate,
  formatDateTime,
  formatUserName,
  milestoneStatusLabels,
  normalizeExternalUrl,
} from "../formatters";
import {
  useProject,
} from "../hooks";
import {
  ProjectPriorityBadge,
  ProjectStatusBadge,
} from "./project-badges";
import {
  ProjectProgress,
} from "./project-progress";

interface ProjectDetailPanelProps {
  projectId: string | null;
  onClose: () => void;
}

export function ProjectDetailPanel({
  projectId,
  onClose,
}: ProjectDetailPanelProps) {
  const projectQuery =
    useProject(projectId);

  const project = projectQuery.data;

  if (!projectId) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close project details"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-3xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Project record
            </p>

            <h2 className="mt-0.5 font-semibold text-slate-950 dark:text-white">
              {project?.project_code
                ?? "Loading project"}
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            aria-label="Close project details"
            className="dark:text-slate-300"
          >
            <X size={19} />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {projectQuery.isLoading && (
            <div className="space-y-4">
              {Array.from({
                length: 8,
              }).map((_, index) => (
                <div
                  key={index}
                  className="h-16 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800"
                />
              ))}
            </div>
          )}

          {projectQuery.isError && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {projectQuery.error
                instanceof Error
                ? projectQuery.error.message
                : "Project details could not be loaded."}
            </div>
          )}

          {project && (
            <div className="space-y-6">
              <section>
                <div className="flex flex-wrap items-center gap-2">
                  <ProjectStatusBadge
                    status={project.status}
                  />

                  <ProjectPriorityBadge
                    priority={
                      project.priority
                    }
                  />

                  {project.quotation_id && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold text-violet-700 dark:bg-violet-950/60 dark:text-violet-300">
                      <Quote size={13} />
                      From quotation
                    </span>
                  )}
                </div>

                <h3 className="mt-4 text-2xl font-bold text-slate-950 dark:text-white">
                  {project.title}
                </h3>

                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                  {project.project_code}
                </p>

                <div className="mt-5">
                  <ProjectProgress
                    progress={
                      project.progress
                    }
                  />
                </div>
              </section>

              <section className="grid gap-3 sm:grid-cols-2">
                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <Building2
                    size={17}
                    className="text-slate-400"
                  />

                  <div className="min-w-0">
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Client
                    </p>

                    <p className="truncate text-sm font-medium text-slate-950 dark:text-white">
                      {project.client_name}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <UserRound
                    size={17}
                    className="text-slate-400"
                  />

                  <div className="min-w-0">
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Project manager
                    </p>

                    <p className="truncate text-sm font-medium text-slate-950 dark:text-white">
                      {formatUserName(
                        project.project_manager,
                      )}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <CalendarDays
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Schedule
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatDate(
                        project.start_date,
                      )}
                      {" — "}
                      {formatDate(
                        project.deadline,
                      )}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <CircleDollarSign
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Budget
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatCurrency(
                        project.budget,
                        project.currency,
                      )}
                    </p>
                  </div>
                </div>
              </section>

              {project.description && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Description
                  </h4>

                  <p className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-600 dark:bg-slate-800/70 dark:text-slate-300">
                    {project.description}
                  </p>
                </section>
              )}

              <section>
                <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                  Project environments
                </h4>

                <div className="mt-3 grid gap-3 sm:grid-cols-3">
                  {[
                    {
                      label: "Repository",
                      value:
                        project.repository_url,
                      icon: Code2,
                    },
                    {
                      label: "Staging",
                      value:
                        project.staging_url,
                      icon: Server,
                    },
                    {
                      label: "Production",
                      value:
                        project.production_url,
                      icon: Globe2,
                    },
                  ].map((link) => {
                    const Icon = link.icon;

                    return link.value ? (
                      <a
                        key={link.label}
                        href={normalizeExternalUrl(
                          link.value,
                        )}
                        target="_blank"
                        rel="noreferrer"
                        className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                      >
                        <Icon
                          size={16}
                          className="text-slate-400"
                        />

                        <span>
                          {link.label}
                        </span>

                        <ExternalLink
                          size={13}
                          className="ml-auto"
                        />
                      </a>
                    ) : (
                      <div
                        key={link.label}
                        className="flex items-center gap-3 rounded-lg border border-dashed border-slate-200 p-3 text-sm text-slate-400 dark:border-slate-700"
                      >
                        <Icon size={16} />
                        {link.label} unset
                      </div>
                    );
                  })}
                </div>
              </section>

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Team members
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {
                      project.team_members
                        .length
                    }
                  </span>
                </div>

                {project.team_members.length
                  === 0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No team members assigned
                  </p>
                ) : (
                  <div className="mt-3 space-y-3">
                    {project.team_members.map(
                      (member) => (
                        <article
                          key={member.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div className="min-w-0">
                              <p className="flex items-center gap-2 font-medium text-slate-950 dark:text-white">
                                <UsersRound
                                  size={15}
                                  className="text-slate-400"
                                />

                                {formatUserName(
                                  member.user,
                                )}
                              </p>

                              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                                {member.role
                                  || "No project role specified"}
                              </p>
                            </div>

                            <span
                              className={
                                member.is_active
                                  ? "rounded-full bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300"
                                  : "rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-400"
                              }
                            >
                              {
                                member.allocation_percentage
                              }
                              %
                            </span>
                          </div>
                        </article>
                      ),
                    )}
                  </div>
                )}
              </section>

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Milestones
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {
                      project.milestones
                        .length
                    }
                  </span>
                </div>

                {project.milestones.length
                  === 0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No project milestones recorded
                  </p>
                ) : (
                  <div className="mt-3 space-y-3">
                    {[...project.milestones]
                      .sort(
                        (left, right) =>
                          left.sort_order
                          - right.sort_order,
                      )
                      .map((milestone) => (
                        <article
                          key={milestone.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <div className="flex items-start justify-between gap-4">
                            <div className="min-w-0">
                              <p className="font-medium text-slate-950 dark:text-white">
                                {
                                  milestone.title
                                }
                              </p>

                              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                                {
                                  milestoneStatusLabels[
                                    milestone.status
                                  ]
                                }
                                {" · Due "}
                                {formatDate(
                                  milestone.due_date,
                                )}
                              </p>
                            </div>

                            <p className="shrink-0 text-sm font-semibold text-slate-950 dark:text-white">
                              {formatCurrency(
                                milestone.amount,
                                project.currency,
                              )}
                            </p>
                          </div>

                          {milestone.description && (
                            <p className="mt-3 text-xs leading-5 text-slate-500 dark:text-slate-400">
                              {
                                milestone.description
                              }
                            </p>
                          )}

                          <div className="mt-3">
                            <ProjectProgress
                              progress={
                                milestone.progress
                              }
                              compact
                            />
                          </div>
                        </article>
                      ))}
                  </div>
                )}
              </section>

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Project notes
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {
                      project.project_notes
                        .length
                    }
                  </span>
                </div>

                {project.project_notes.length
                  === 0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No project notes recorded
                  </p>
                ) : (
                  <div className="mt-3 space-y-3">
                    {project.project_notes.map(
                      (note) => (
                        <article
                          key={note.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <div className="flex flex-wrap items-center gap-2">
                            {note.is_pinned && (
                              <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2 py-0.5 text-xs font-semibold text-amber-700 dark:bg-amber-950/60 dark:text-amber-300">
                                <Pin size={12} />
                                Pinned
                              </span>
                            )}

                            {note.is_client_visible && (
                              <span className="rounded-full bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700 dark:bg-blue-950/60 dark:text-blue-300">
                                Client visible
                              </span>
                            )}

                            <span className="ml-auto text-xs text-slate-400">
                              {formatDateTime(
                                note.created_at,
                              )}
                            </span>
                          </div>

                          <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-600 dark:text-slate-300">
                            {note.content}
                          </p>
                        </article>
                      ),
                    )}
                  </div>
                )}
              </section>

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Activity timeline
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {project.events.length}
                  </span>
                </div>

                {project.events.length ===
                0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No project events recorded
                  </p>
                ) : (
                  <div className="mt-3 space-y-3">
                    {project.events.map(
                      (event) => (
                        <article
                          key={event.id}
                          className="flex gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                            <FileText
                              size={15}
                            />
                          </span>

                          <div className="min-w-0">
                            <p className="text-sm font-medium text-slate-950 dark:text-white">
                              {
                                event.description
                              }
                            </p>

                            <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                              {event.event_type}
                              {" · "}
                              {formatDateTime(
                                event.created_at,
                              )}
                            </p>
                          </div>
                        </article>
                      ),
                    )}
                  </div>
                )}
              </section>

              {project.completed_at && (
                <section className="rounded-xl border border-emerald-200 bg-emerald-50 p-4 dark:border-emerald-900 dark:bg-emerald-950/30">
                  <h4 className="flex items-center gap-2 text-sm font-semibold text-emerald-900 dark:text-emerald-200">
                    <CheckCircle2 size={17} />
                    Completion record
                  </h4>

                  <p className="mt-2 text-sm text-emerald-800 dark:text-emerald-300">
                    Project completed on{" "}
                    {formatDateTime(
                      project.completed_at,
                    )}.
                  </p>
                </section>
              )}

              {project.notes && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Internal notes
                  </h4>

                  <p className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-600 dark:bg-slate-800/70 dark:text-slate-300">
                    {project.notes}
                  </p>
                </section>
              )}

              {project.tags.length > 0 && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Tags
                  </h4>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {project.tags.map(
                      (tag) => (
                        <span
                          key={tag}
                          className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"
                        >
                          {tag}
                        </span>
                      ),
                    )}
                  </div>
                </section>
              )}

              <section className="border-t border-slate-200 pt-4 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
                <p>
                  Created{" "}
                  {formatDateTime(
                    project.created_at,
                  )}
                </p>

                <p className="mt-1">
                  Updated{" "}
                  {formatDateTime(
                    project.updated_at,
                  )}
                </p>
              </section>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
