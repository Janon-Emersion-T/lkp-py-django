import {
  z,
} from "zod";

import {
  milestoneStatuses,
  projectPriorities,
  projectStatuses,
} from "./types";

const userSummarySchema = z.object({
  id: z.number().int(),
  email: z.string(),
  first_name: z.string(),
  last_name: z.string(),
});

const teamMemberSchema = z.object({
  id: z.string().uuid(),
  user: userSummarySchema,
  role: z.string(),
  allocation_percentage:
    z.number().int().min(1).max(100),
  is_active: z.boolean(),
  created_at: z.string(),
});

const milestoneSchema = z.object({
  id: z.string().uuid(),
  title: z.string(),
  description: z.string(),
  status: z.enum(milestoneStatuses),
  start_date: z.string().nullable(),
  due_date: z.string().nullable(),
  completed_at: z.string().nullable(),
  progress: z.number().int().min(0).max(100),
  sort_order: z.number().int().nonnegative(),
  amount: z.string(),
  created_at: z.string(),
  updated_at: z.string(),
});

const projectNoteSchema = z.object({
  id: z.string().uuid(),
  content: z.string(),
  is_pinned: z.boolean(),
  is_client_visible: z.boolean(),
  created_at: z.string(),
});

const projectEventSchema = z.object({
  id: z.string().uuid(),
  event_type: z.string(),
  description: z.string(),
  metadata: z.record(
    z.string(),
    z.unknown(),
  ),
  created_at: z.string(),
});

export const projectSchema = z.object({
  id: z.string().uuid(),
  project_code: z.string(),
  client_id: z.string().uuid(),
  client_name: z.string(),
  quotation_id: z.string().uuid().nullable(),
  title: z.string(),
  description: z.string(),
  status: z.enum(projectStatuses),
  priority: z.enum(projectPriorities),
  budget: z.string(),
  currency: z.string(),
  start_date: z.string().nullable(),
  deadline: z.string().nullable(),
  completed_at: z.string().nullable(),
  progress: z.number().int().min(0).max(100),
  project_manager: userSummarySchema.nullable(),
  repository_url: z.string(),
  staging_url: z.string(),
  production_url: z.string(),
  notes: z.string(),
  tags: z.array(z.string()),
  team_members: z.array(teamMemberSchema),
  milestones: z.array(milestoneSchema),
  project_notes: z.array(projectNoteSchema),
  events: z.array(projectEventSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

export const paginatedProjectsSchema = z.object({
  items: z.array(projectSchema),
  pagination: z.object({
    page: z.number().int().positive(),
    page_size: z.number().int().positive(),
    total_items: z.number().int().nonnegative(),
    total_pages: z.number().int().nonnegative(),
  }),
});
