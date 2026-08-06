import {
  z,
} from "zod";

import {
  taskPriorities,
  taskStatuses,
} from "./types";

const userSummarySchema = z.object({
  id: z.number().int(),
  email: z.string(),
  first_name: z.string(),
  last_name: z.string(),
});

const taskAssigneeSchema = z.object({
  id: z.string().uuid(),
  user: userSummarySchema,
  created_at: z.string(),
});

const taskWatcherSchema = z.object({
  id: z.string().uuid(),
  user: userSummarySchema,
  created_at: z.string(),
});

const taskChecklistSchema = z.object({
  id: z.string().uuid(),
  title: z.string(),
  is_completed: z.boolean(),
  completed_at: z.string().nullable(),
  completed_by: userSummarySchema.nullable(),
  sort_order: z.number().int().nonnegative(),
  created_at: z.string(),
});

const taskCommentSchema = z.object({
  id: z.string().uuid(),
  content: z.string(),
  is_internal: z.boolean(),
  author: userSummarySchema.nullable(),
  created_at: z.string(),
});

const taskDependencySchema = z.object({
  id: z.string().uuid(),
  related_task_id: z.string().uuid(),
  related_task_title: z.string(),
  dependency_type: z.string(),
  created_at: z.string(),
});

const taskTimeLogSchema = z.object({
  id: z.string().uuid(),
  user: userSummarySchema,
  work_date: z.string(),
  hours: z.string(),
  description: z.string(),
  is_billable: z.boolean(),
  created_at: z.string(),
});

const taskEventSchema = z.object({
  id: z.string().uuid(),
  event_type: z.string(),
  description: z.string(),
  metadata: z.record(
    z.string(),
    z.unknown(),
  ),
  created_at: z.string(),
});

export const taskSchema = z.object({
  id: z.string().uuid(),
  project_id: z.string().uuid().nullable(),
  project_title: z.string().nullable(),
  milestone_id: z.string().uuid().nullable(),
  milestone_title: z.string().nullable(),
  parent_id: z.string().uuid().nullable(),
  title: z.string(),
  description: z.string(),
  status: z.enum(taskStatuses),
  priority: z.enum(taskPriorities),
  assignee: userSummarySchema.nullable(),
  start_date: z.string().nullable(),
  due_date: z.string().nullable(),
  completed_at: z.string().nullable(),
  estimated_hours: z.string(),
  actual_hours: z.string(),
  progress: z.number().int().min(0).max(100),
  sort_order: z.number().int().nonnegative(),
  labels: z.array(z.string()),
  is_recurring: z.boolean(),
  recurrence_rule: z.string(),
  additional_assignees: z.array(
    taskAssigneeSchema,
  ),
  watchers: z.array(taskWatcherSchema),
  checklist_items: z.array(
    taskChecklistSchema,
  ),
  comments: z.array(taskCommentSchema),
  dependencies: z.array(
    taskDependencySchema,
  ),
  time_logs: z.array(taskTimeLogSchema),
  events: z.array(taskEventSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedTasksSchema = z.object({
  items: z.array(taskSchema),
  pagination: z.object({
    page: z.number().int().positive(),
    page_size: z.number().int().positive(),
    total_items: z.number().int().nonnegative(),
    total_pages: z.number().int().nonnegative(),
  }),
});
