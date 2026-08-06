import {
  z,
} from "zod";

import {
  engagementTypes,
  employmentStatuses,
  teamTypes,
  workLocationTypes,
} from "./types";

const metadataSchema =
  z.record(
    z.string(),
    z.unknown(),
  );

const countMapSchema =
  z.record(
    z.string(),
    z.number().int().nonnegative(),
  );

export const teamSchema =
  z.object({
    id: z.string().uuid(),
    name: z.string(),
    slug: z.string(),
    team_type: z.enum(teamTypes),
    description: z.string(),
    parent_id:
      z.string().uuid().nullable(),
    parent_name:
      z.string().nullable(),
    manager_id:
      z.string().uuid().nullable(),
    manager_name:
      z.string().nullable(),
    is_active: z.boolean(),
    is_public: z.boolean(),
    sort_order:
      z.number().int().nonnegative(),
    metadata: metadataSchema,
    member_count:
      z.number().int().nonnegative(),
  });

export const teamMembershipSchema =
  z.object({
    id: z.string().uuid(),
    team_id: z.string().uuid(),
    team_name: z.string(),
    role_title: z.string(),
    is_primary: z.boolean(),
    is_active: z.boolean(),
    joined_at: z.string(),
    left_at: z.string().nullable(),
    sort_order:
      z.number().int().nonnegative(),
  });

export const teamMemberServiceSchema =
  z.object({
    id: z.string().uuid(),
    service_id: z.string().uuid(),
    service_title: z.string(),
    expertise_level: z.string(),
    years_of_experience:
      z.union([
        z.number(),
        z.string(),
      ]).nullable(),
    is_primary: z.boolean(),
    is_public: z.boolean(),
    sort_order:
      z.number().int().nonnegative(),
  });

export const teamMemberSchema =
  z.object({
    id: z.string().uuid(),
    user_id:
      z.string().uuid().nullable(),
    employee_code: z.string(),
    first_name: z.string(),
    last_name: z.string(),
    full_name: z.string(),
    preferred_name: z.string(),
    display_name: z.string(),
    job_title: z.string(),
    professional_title: z.string(),
    email: z.string(),
    phone: z.string(),
    public_email: z.string(),
    public_phone: z.string(),
    profile_image_id:
      z.string().uuid().nullable(),
    bio: z.string(),
    short_bio: z.string(),
    qualifications: z.string(),
    years_of_experience:
      z.number().int().nonnegative().nullable(),
    engagement_type:
      z.enum(engagementTypes),
    employment_status:
      z.enum(employmentStatuses),
    work_location_type:
      z.enum(workLocationTypes),
    office_location: z.string(),
    country: z.string(),
    timezone_name: z.string(),
    joined_at: z.string().nullable(),
    employment_ended_at:
      z.string().nullable(),
    reports_to_id:
      z.string().uuid().nullable(),
    reports_to_name:
      z.string().nullable(),
    linkedin_url: z.string(),
    github_url: z.string(),
    portfolio_url: z.string(),
    website_url: z.string(),
    is_leadership: z.boolean(),
    is_public: z.boolean(),
    is_featured: z.boolean(),
    is_current: z.boolean(),
    sort_order:
      z.number().int().nonnegative(),
    metadata: metadataSchema,
    memberships:
      z.array(teamMembershipSchema),
    services:
      z.array(teamMemberServiceSchema),
  });

export const teamListSchema =
  z.array(teamSchema);

export const teamMemberListSchema =
  z.array(teamMemberSchema);

export const teamManagementDashboardSchema =
  z.object({
    total_teams:
      z.number().int().nonnegative(),
    active_teams:
      z.number().int().nonnegative(),
    public_teams:
      z.number().int().nonnegative(),
    total_members:
      z.number().int().nonnegative(),
    active_members:
      z.number().int().nonnegative(),
    members_on_leave:
      z.number().int().nonnegative(),
    inactive_members:
      z.number().int().nonnegative(),
    public_members:
      z.number().int().nonnegative(),
    featured_members:
      z.number().int().nonnegative(),
    leadership_members:
      z.number().int().nonnegative(),
    members_without_primary_team:
      z.number().int().nonnegative(),
    members_without_manager:
      z.number().int().nonnegative(),
    members_by_status:
      countMapSchema,
    members_by_engagement:
      countMapSchema,
    members_by_location:
      countMapSchema,
    members_by_country:
      countMapSchema,
    team_sizes:
      countMapSchema,
  });
