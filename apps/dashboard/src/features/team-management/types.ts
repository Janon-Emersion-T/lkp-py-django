export const teamTypes = [
  "executive",
  "management",
  "engineering",
  "design",
  "marketing",
  "sales",
  "finance",
  "operations",
  "support",
  "hr",
  "legal",
  "project",
  "custom",
] as const;

export type TeamType =
  (typeof teamTypes)[number];

export const employmentStatuses = [
  "active",
  "on_leave",
  "suspended",
  "resigned",
  "terminated",
  "contract_ended",
  "inactive",
] as const;

export type EmploymentStatus =
  (typeof employmentStatuses)[number];

export const engagementTypes = [
  "full_time",
  "part_time",
  "contract",
  "intern",
  "consultant",
  "volunteer",
] as const;

export type EngagementType =
  (typeof engagementTypes)[number];

export const workLocationTypes = [
  "onsite",
  "remote",
  "hybrid",
] as const;

export type WorkLocationType =
  (typeof workLocationTypes)[number];

export interface Team {
  id: string;
  name: string;
  slug: string;
  team_type: TeamType;
  description: string;
  parent_id: string | null;
  parent_name: string | null;
  manager_id: string | null;
  manager_name: string | null;
  is_active: boolean;
  is_public: boolean;
  sort_order: number;
  metadata: Record<string, unknown>;
  member_count: number;
}

export interface TeamMembership {
  id: string;
  team_id: string;
  team_name: string;
  role_title: string;
  is_primary: boolean;
  is_active: boolean;
  joined_at: string;
  left_at: string | null;
  sort_order: number;
}

export interface TeamMemberService {
  id: string;
  service_id: string;
  service_title: string;
  expertise_level: string;
  years_of_experience: number | string | null;
  is_primary: boolean;
  is_public: boolean;
  sort_order: number;
}

export interface TeamMember {
  id: string;
  user_id: string | null;
  employee_code: string;
  first_name: string;
  last_name: string;
  full_name: string;
  preferred_name: string;
  display_name: string;
  job_title: string;
  professional_title: string;
  email: string;
  phone: string;
  public_email: string;
  public_phone: string;
  profile_image_id: string | null;
  bio: string;
  short_bio: string;
  qualifications: string;
  years_of_experience: number | null;
  engagement_type: EngagementType;
  employment_status: EmploymentStatus;
  work_location_type: WorkLocationType;
  office_location: string;
  country: string;
  timezone_name: string;
  joined_at: string | null;
  employment_ended_at: string | null;
  reports_to_id: string | null;
  reports_to_name: string | null;
  linkedin_url: string;
  github_url: string;
  portfolio_url: string;
  website_url: string;
  is_leadership: boolean;
  is_public: boolean;
  is_featured: boolean;
  is_current: boolean;
  sort_order: number;
  metadata: Record<string, unknown>;
  memberships: TeamMembership[];
  services: TeamMemberService[];
}

export interface TeamManagementDashboard {
  total_teams: number;
  active_teams: number;
  public_teams: number;
  total_members: number;
  active_members: number;
  members_on_leave: number;
  inactive_members: number;
  public_members: number;
  featured_members: number;
  leadership_members: number;
  members_without_primary_team: number;
  members_without_manager: number;
  members_by_status: Record<string, number>;
  members_by_engagement: Record<string, number>;
  members_by_location: Record<string, number>;
  members_by_country: Record<string, number>;
  team_sizes: Record<string, number>;
}

export interface TeamFilters {
  search: string;
  teamType: TeamType | "";
  parentId: string;
  activeState: "all" | "active" | "inactive";
  publicState: "all" | "public" | "private";
  ordering: string;
}

export interface MemberFilters {
  search: string;
  employmentStatus: EmploymentStatus | "";
  engagementType: EngagementType | "";
  workLocationType: WorkLocationType | "";
  country: string;
  teamId: string;
  reportsToId: string;
  publicState: "all" | "public" | "private";
  featuredState: "all" | "featured" | "standard";
  ordering: string;
}

export interface TeamPayload {
  name: string;
  slug: string;
  team_type: TeamType;
  description: string;
  parent_id: string | null;
  manager_id: string | null;
  is_active: boolean;
  is_public: boolean;
  sort_order: number;
  metadata: Record<string, unknown>;
}

export interface MemberStatusPayload {
  employment_status: EmploymentStatus;
  employment_ended_at: string | null;
}

export interface ReportingLinePayload {
  reports_to_id: string | null;
}

export interface TeamManagerPayload {
  manager_id: string | null;
}
