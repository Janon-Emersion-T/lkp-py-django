export const projectStatuses = [
  "planning",
  "development",
  "testing",
  "review",
  "completed",
  "cancelled",
] as const;

export type ProjectStatus =
  (typeof projectStatuses)[number];

export const projectPriorities = [
  "low",
  "normal",
  "high",
  "urgent",
] as const;

export type ProjectPriority =
  (typeof projectPriorities)[number];

export const milestoneStatuses = [
  "pending",
  "in_progress",
  "completed",
  "cancelled",
] as const;

export type MilestoneStatus =
  (typeof milestoneStatuses)[number];

export const projectOrderingOptions = [
  "-created_at",
  "created_at",
  "project_code",
  "-project_code",
  "title",
  "-title",
  "status",
  "-status",
  "priority",
  "-priority",
  "budget",
  "-budget",
  "progress",
  "-progress",
  "start_date",
  "-start_date",
  "deadline",
  "-deadline",
  "updated_at",
  "-updated_at",
] as const;

export type ProjectOrdering =
  (typeof projectOrderingOptions)[number];

export interface UserSummary {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
}

export interface ProjectTeamMember {
  id: string;
  user: UserSummary;
  role: string;
  allocation_percentage: number;
  is_active: boolean;
  created_at: string;
}

export interface ProjectMilestone {
  id: string;
  title: string;
  description: string;
  status: MilestoneStatus;
  start_date: string | null;
  due_date: string | null;
  completed_at: string | null;
  progress: number;
  sort_order: number;
  amount: string;
  created_at: string;
  updated_at: string;
}

export interface ProjectNote {
  id: string;
  content: string;
  is_pinned: boolean;
  is_client_visible: boolean;
  created_at: string;
}

export interface ProjectEvent {
  id: string;
  event_type: string;
  description: string;
  metadata: Record<string, unknown>;
  created_at: string;
}

export interface Project {
  id: string;
  project_code: string;
  client_id: string;
  client_name: string;
  quotation_id: string | null;
  title: string;
  description: string;
  status: ProjectStatus;
  priority: ProjectPriority;
  budget: string;
  currency: string;
  start_date: string | null;
  deadline: string | null;
  completed_at: string | null;
  progress: number;
  project_manager: UserSummary | null;
  repository_url: string;
  staging_url: string;
  production_url: string;
  notes: string;
  tags: string[];
  team_members: ProjectTeamMember[];
  milestones: ProjectMilestone[];
  project_notes: ProjectNote[];
  events: ProjectEvent[];
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
}

export interface PaginatedProjects {
  items: Project[];
  pagination: PaginationMeta;
}

export interface ProjectFilters {
  page: number;
  pageSize: number;
  search: string;
  status: ProjectStatus | "";
  priority: ProjectPriority | "";
  clientId: string;
  projectManagerId: string;
  ordering: ProjectOrdering;
}
