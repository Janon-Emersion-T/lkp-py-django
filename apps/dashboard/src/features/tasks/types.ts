export const taskStatuses = [
  "todo",
  "in_progress",
  "testing",
  "review",
  "completed",
  "cancelled",
] as const;

export type TaskStatus =
  (typeof taskStatuses)[number];

export const taskPriorities = [
  "low",
  "normal",
  "high",
  "urgent",
] as const;

export type TaskPriority =
  (typeof taskPriorities)[number];

export const taskOrderingOptions = [
  "sort_order",
  "-sort_order",
  "title",
  "-title",
  "status",
  "-status",
  "priority",
  "-priority",
  "start_date",
  "-start_date",
  "due_date",
  "-due_date",
  "progress",
  "-progress",
  "created_at",
  "-created_at",
  "updated_at",
  "-updated_at",
] as const;

export type TaskOrdering =
  (typeof taskOrderingOptions)[number];

export interface UserSummary {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

export interface TaskAssignee {
  id: string;
  user: UserSummary;
  created_at: string;
}

export interface TaskWatcher {
  id: string;
  user: UserSummary;
  created_at: string;
}

export interface TaskChecklistItem {
  id: string;
  title: string;
  is_completed: boolean;
  completed_at: string | null;
  completed_by: UserSummary | null;
  sort_order: number;
  created_at: string;
}

export interface TaskComment {
  id: string;
  content: string;
  is_internal: boolean;
  author: UserSummary | null;
  created_at: string;
}

export interface TaskDependency {
  id: string;
  related_task_id: string;
  related_task_title: string;
  dependency_type: string;
  created_at: string;
}

export interface TaskTimeLog {
  id: string;
  user: UserSummary;
  work_date: string;
  hours: string;
  description: string;
  is_billable: boolean;
  created_at: string;
}

export interface TaskEvent {
  id: string;
  event_type: string;
  description: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface Task {
  id: string;
  project_id: string | null;
  project_title: string | null;
  milestone_id: string | null;
  milestone_title: string | null;
  parent_id: string | null;
  title: string;
  description: string;
  status: TaskStatus;
  priority: TaskPriority;
  assignee: UserSummary | null;
  start_date: string | null;
  due_date: string | null;
  completed_at: string | null;
  estimated_hours: string;
  actual_hours: string;
  progress: number;
  sort_order: number;
  labels: string[];
  is_recurring: boolean;
  recurrence_rule: string;
  additional_assignees: TaskAssignee[];
  watchers: TaskWatcher[];
  checklist_items: TaskChecklistItem[];
  comments: TaskComment[];
  dependencies: TaskDependency[];
  time_logs: TaskTimeLog[];
  events: TaskEvent[];
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedTasks {
  items: Task[];
  pagination: PaginationMeta;
}

export interface TaskFilters {
  page: number;
  pageSize: number;
  search: string;
  status: TaskStatus | "";
  priority: TaskPriority | "";
  projectId: string;
  milestoneId: string;
  assigneeId: string;
  ordering: TaskOrdering;
}
