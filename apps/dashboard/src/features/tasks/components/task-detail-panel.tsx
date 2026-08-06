import {
  CalendarDays,
  CheckCircle2,
  CheckSquare2,
  Clock3,
  Eye,
  FileText,
  Link2,
  MessageSquare,
  Repeat2,
  UserRound,
  UsersRound,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  formatDate,
  formatDateTime,
  formatHours,
  formatUserName,
} from "../formatters";
import {
  useTask,
} from "../hooks";
import {
  TaskPriorityBadge,
  TaskStatusBadge,
} from "./task-badges";
import {
  TaskProgress,
} from "./task-progress";

export function TaskDetailPanel({
  taskId,
  onClose,
}: {
  taskId: string | null;
  onClose: () => void;
}) {
  const taskQuery = useTask(taskId);
  const task = taskQuery.data;

  if (!taskId) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close task details"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-3xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Task record
            </p>

            <h2 className="mt-0.5 font-semibold text-slate-950 dark:text-white">
              {task?.title
                ?? "Loading task"}
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            aria-label="Close task details"
            className="dark:text-slate-300"
          >
            <X size={19} />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {taskQuery.isLoading && (
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

          {taskQuery.isError && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {taskQuery.error
                instanceof Error
                ? taskQuery.error.message
                : "Task details could not be loaded."}
            </div>
          )}

          {task && (
            <div className="space-y-6">
              <section>
                <div className="flex flex-wrap items-center gap-2">
                  <TaskStatusBadge
                    status={task.status}
                  />

                  <TaskPriorityBadge
                    priority={task.priority}
                  />

                  {task.is_recurring && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold text-violet-700 dark:bg-violet-950/60 dark:text-violet-300">
                      <Repeat2 size={13} />
                      Recurring
                    </span>
                  )}
                </div>

                <h3 className="mt-4 text-2xl font-bold text-slate-950 dark:text-white">
                  {task.title}
                </h3>

                {task.project_title && (
                  <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                    {task.project_title}
                    {task.milestone_title
                      ? ` · ${task.milestone_title}`
                      : ""}
                  </p>
                )}

                <div className="mt-5">
                  <TaskProgress
                    progress={task.progress}
                  />
                </div>
              </section>

              <section className="grid gap-3 sm:grid-cols-2">
                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <UserRound
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Primary assignee
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatUserName(
                        task.assignee,
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
                        task.start_date,
                      )}
                      {" — "}
                      {formatDate(
                        task.due_date,
                      )}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <Clock3
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Estimated time
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatHours(
                        task.estimated_hours,
                      )}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700">
                  <CheckCircle2
                    size={17}
                    className="text-slate-400"
                  />

                  <div>
                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      Actual time
                    </p>

                    <p className="text-sm font-medium text-slate-950 dark:text-white">
                      {formatHours(
                        task.actual_hours,
                      )}
                    </p>
                  </div>
                </div>
              </section>

              {task.description && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Description
                  </h4>

                  <p className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-600 dark:bg-slate-800/70 dark:text-slate-300">
                    {task.description}
                  </p>
                </section>
              )}

              {task.labels.length > 0 && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Labels
                  </h4>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {task.labels.map(
                      (label) => (
                        <span
                          key={label}
                          className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"
                        >
                          {label}
                        </span>
                      ),
                    )}
                  </div>
                </section>
              )}

              <section>
                <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-950 dark:text-white">
                  <CheckSquare2 size={16} />
                  Checklist
                </h4>

                {task.checklist_items.length
                  === 0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No checklist items
                  </p>
                ) : (
                  <div className="mt-3 space-y-2">
                    {[...task.checklist_items]
                      .sort(
                        (left, right) =>
                          left.sort_order
                          - right.sort_order,
                      )
                      .map((item) => (
                        <div
                          key={item.id}
                          className="flex items-start gap-3 rounded-lg border border-slate-200 p-3 dark:border-slate-700"
                        >
                          <span
                            className={
                              item.is_completed
                                ? "mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded bg-emerald-600 text-white"
                                : "mt-0.5 h-5 w-5 shrink-0 rounded border border-slate-300 dark:border-slate-600"
                            }
                          >
                            {item.is_completed
                              ? "✓"
                              : ""}
                          </span>

                          <div>
                            <p
                              className={
                                item.is_completed
                                  ? "text-sm text-slate-400 line-through"
                                  : "text-sm text-slate-700 dark:text-slate-300"
                              }
                            >
                              {item.title}
                            </p>

                            {item.completed_at && (
                              <p className="mt-1 text-xs text-slate-400">
                                Completed{" "}
                                {formatDateTime(
                                  item.completed_at,
                                )}
                              </p>
                            )}
                          </div>
                        </div>
                      ))}
                  </div>
                )}
              </section>

              <section>
                <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-950 dark:text-white">
                  <UsersRound size={16} />
                  Participants
                </h4>

                <div className="mt-3 grid gap-3 sm:grid-cols-2">
                  <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                    <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                      Additional assignees
                    </p>

                    <div className="mt-3 space-y-2">
                      {task.additional_assignees.length
                        === 0 ? (
                        <p className="text-sm text-slate-500">
                          None
                        </p>
                      ) : (
                        task.additional_assignees.map(
                          (assignment) => (
                            <p
                              key={assignment.id}
                              className="text-sm text-slate-700 dark:text-slate-300"
                            >
                              {formatUserName(
                                assignment.user,
                              )}
                            </p>
                          ),
                        )
                      )}
                    </div>
                  </div>

                  <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                    <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-400">
                      <Eye size={13} />
                      Watchers
                    </p>

                    <div className="mt-3 space-y-2">
                      {task.watchers.length
                        === 0 ? (
                        <p className="text-sm text-slate-500">
                          None
                        </p>
                      ) : (
                        task.watchers.map(
                          (watcher) => (
                            <p
                              key={watcher.id}
                              className="text-sm text-slate-700 dark:text-slate-300"
                            >
                              {formatUserName(
                                watcher.user,
                              )}
                            </p>
                          ),
                        )
                      )}
                    </div>
                  </div>
                </div>
              </section>

              <section>
                <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-950 dark:text-white">
                  <MessageSquare size={16} />
                  Comments
                </h4>

                <div className="mt-3 space-y-3">
                  {task.comments.length ===
                  0 ? (
                    <p className="rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700">
                      No comments
                    </p>
                  ) : (
                    task.comments.map(
                      (comment) => (
                        <article
                          key={comment.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <div className="flex items-center gap-2">
                            <p className="text-sm font-semibold text-slate-950 dark:text-white">
                              {formatUserName(
                                comment.author,
                              )}
                            </p>

                            {comment.is_internal && (
                              <span className="rounded-full bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-700 dark:bg-amber-950/60 dark:text-amber-300">
                                Internal
                              </span>
                            )}

                            <span className="ml-auto text-xs text-slate-400">
                              {formatDateTime(
                                comment.created_at,
                              )}
                            </span>
                          </div>

                          <p className="mt-3 whitespace-pre-wrap text-sm leading-6 text-slate-600 dark:text-slate-300">
                            {comment.content}
                          </p>
                        </article>
                      ),
                    )
                  )}
                </div>
              </section>

              <section>
                <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-950 dark:text-white">
                  <Link2 size={16} />
                  Dependencies
                </h4>

                <div className="mt-3 space-y-2">
                  {task.dependencies.length
                    === 0 ? (
                    <p className="rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700">
                      No dependencies
                    </p>
                  ) : (
                    task.dependencies.map(
                      (dependency) => (
                        <div
                          key={dependency.id}
                          className="rounded-lg border border-slate-200 p-3 dark:border-slate-700"
                        >
                          <p className="text-sm font-medium text-slate-950 dark:text-white">
                            {
                              dependency.related_task_title
                            }
                          </p>

                          <p className="mt-1 text-xs text-slate-500">
                            {
                              dependency.dependency_type
                            }
                          </p>
                        </div>
                      ),
                    )
                  )}
                </div>
              </section>

              <section>
                <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-950 dark:text-white">
                  <Clock3 size={16} />
                  Time logs
                </h4>

                <div className="mt-3 space-y-2">
                  {task.time_logs.length ===
                  0 ? (
                    <p className="rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700">
                      No time recorded
                    </p>
                  ) : (
                    task.time_logs.map(
                      (timeLog) => (
                        <div
                          key={timeLog.id}
                          className="flex items-start justify-between gap-4 rounded-lg border border-slate-200 p-3 dark:border-slate-700"
                        >
                          <div>
                            <p className="text-sm font-medium text-slate-950 dark:text-white">
                              {formatUserName(
                                timeLog.user,
                              )}
                            </p>

                            <p className="mt-1 text-xs text-slate-500">
                              {formatDate(
                                timeLog.work_date,
                              )}
                              {timeLog.description
                                ? ` · ${timeLog.description}`
                                : ""}
                            </p>
                          </div>

                          <div className="text-right">
                            <p className="text-sm font-semibold text-slate-950 dark:text-white">
                              {formatHours(
                                timeLog.hours,
                              )}
                            </p>

                            <p className="text-xs text-slate-400">
                              {timeLog.is_billable
                                ? "Billable"
                                : "Non-billable"}
                            </p>
                          </div>
                        </div>
                      ),
                    )
                  )}
                </div>
              </section>

              <section>
                <h4 className="flex items-center gap-2 text-sm font-semibold text-slate-950 dark:text-white">
                  <FileText size={16} />
                  Activity timeline
                </h4>

                <div className="mt-3 space-y-3">
                  {task.events.length === 0 ? (
                    <p className="rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700">
                      No task events
                    </p>
                  ) : (
                    task.events.map(
                      (event) => (
                        <article
                          key={event.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <p className="text-sm font-medium text-slate-950 dark:text-white">
                            {event.description}
                          </p>

                          <p className="mt-1 text-xs text-slate-500">
                            {event.event_type}
                            {" · "}
                            {formatDateTime(
                              event.created_at,
                            )}
                          </p>
                        </article>
                      ),
                    )
                  )}
                </div>
              </section>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
