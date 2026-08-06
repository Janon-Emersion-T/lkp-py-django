import {
  apiRequest,
} from "../../lib/http";
import {
  teamListSchema,
  teamManagementDashboardSchema,
  teamMemberListSchema,
  teamMemberSchema,
  teamSchema,
} from "./schemas";
import type {
  MemberFilters,
  MemberStatusPayload,
  ReportingLinePayload,
  Team,
  TeamFilters,
  TeamManagementDashboard,
  TeamManagerPayload,
  TeamMember,
  TeamMemberPayload,
  TeamPayload,
} from "./types";

function addBooleanFilter(
  params: URLSearchParams,
  key: string,
  value: string,
  trueValue: string,
) {
  if (value === "all") {
    return;
  }

  params.set(
    key,
    String(value === trueValue),
  );
}

function buildTeamQuery(
  filters: TeamFilters,
): string {
  const params =
    new URLSearchParams();

  if (filters.search.trim()) {
    params.set(
      "search",
      filters.search.trim(),
    );
  }

  if (filters.teamType) {
    params.set(
      "team_type",
      filters.teamType,
    );
  }

  if (filters.parentId) {
    params.set(
      "parent_id",
      filters.parentId,
    );
  }

  addBooleanFilter(
    params,
    "is_active",
    filters.activeState,
    "active",
  );

  addBooleanFilter(
    params,
    "is_public",
    filters.publicState,
    "public",
  );

  if (filters.ordering) {
    params.set(
      "ordering",
      filters.ordering,
    );
  }

  return params.toString();
}

function buildMemberQuery(
  filters: MemberFilters,
): string {
  const params =
    new URLSearchParams();

  if (filters.search.trim()) {
    params.set(
      "search",
      filters.search.trim(),
    );
  }

  if (filters.employmentStatus) {
    params.set(
      "employment_status",
      filters.employmentStatus,
    );
  }

  if (filters.engagementType) {
    params.set(
      "engagement_type",
      filters.engagementType,
    );
  }

  if (filters.workLocationType) {
    params.set(
      "work_location_type",
      filters.workLocationType,
    );
  }

  if (filters.country.trim()) {
    params.set(
      "country",
      filters.country.trim(),
    );
  }

  if (filters.teamId) {
    params.set(
      "team_id",
      filters.teamId,
    );
  }

  if (filters.reportsToId) {
    params.set(
      "reports_to_id",
      filters.reportsToId,
    );
  }

  addBooleanFilter(
    params,
    "is_public",
    filters.publicState,
    "public",
  );

  addBooleanFilter(
    params,
    "is_featured",
    filters.featuredState,
    "featured",
  );

  if (filters.ordering) {
    params.set(
      "ordering",
      filters.ordering,
    );
  }

  return params.toString();
}

export async function getTeamDashboard():
Promise<TeamManagementDashboard> {
  const response =
    await apiRequest<unknown>(
      "/team-management/dashboard",
    );

  return teamManagementDashboardSchema.parse(
    response,
  );
}

export async function getTeams(
  filters: TeamFilters,
): Promise<Team[]> {
  const query =
    buildTeamQuery(filters);

  const response =
    await apiRequest<unknown>(
      `/team-management/teams${
        query ? `?${query}` : ""
      }`,
    );

  return teamListSchema.parse(
    response,
  );
}

export async function getTeam(
  teamId: string,
): Promise<Team> {
  const response =
    await apiRequest<unknown>(
      `/team-management/teams/${teamId}`,
    );

  return teamSchema.parse(response);
}

export async function createTeam(
  payload: TeamPayload,
): Promise<Team> {
  const response =
    await apiRequest<unknown>(
      "/team-management/teams",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );

  return teamSchema.parse(response);
}

export async function updateTeam({
  teamId,
  payload,
}: {
  teamId: string;
  payload: TeamPayload;
}): Promise<Team> {
  const response =
    await apiRequest<unknown>(
      `/team-management/teams/${teamId}`,
      {
        method: "PUT",
        body: JSON.stringify(payload),
      },
    );

  return teamSchema.parse(response);
}

export async function updateTeamManager({
  teamId,
  payload,
}: {
  teamId: string;
  payload: TeamManagerPayload;
}): Promise<Team> {
  const response =
    await apiRequest<unknown>(
      `/team-management/teams/${teamId}/manager`,
      {
        method: "PUT",
        body: JSON.stringify(payload),
      },
    );

  return teamSchema.parse(response);
}

export async function getMembers(
  filters: MemberFilters,
): Promise<TeamMember[]> {
  const query =
    buildMemberQuery(filters);

  const response =
    await apiRequest<unknown>(
      `/team-management/members${
        query ? `?${query}` : ""
      }`,
    );

  return teamMemberListSchema.parse(
    response,
  );
}

export async function getMember(
  memberId: string,
): Promise<TeamMember> {
  const response =
    await apiRequest<unknown>(
      `/team-management/members/${memberId}`,
    );

  return teamMemberSchema.parse(
    response,
  );
}

export async function createTeamMember(
  payload: TeamMemberPayload,
): Promise<TeamMember> {
  const response =
    await apiRequest<unknown>(
      "/team-management/members",
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );

  return teamMemberSchema.parse(
    response,
  );
}

export async function updateTeamMember({
  memberId,
  payload,
}: {
  memberId: string;
  payload: TeamMemberPayload;
}): Promise<TeamMember> {
  const response =
    await apiRequest<unknown>(
      `/team-management/members/${memberId}`,
      {
        method: "PUT",
        body: JSON.stringify(payload),
      },
    );

  return teamMemberSchema.parse(
    response,
  );
}

export async function updateMemberStatus({
  memberId,
  payload,
}: {
  memberId: string;
  payload: MemberStatusPayload;
}): Promise<TeamMember> {
  const response =
    await apiRequest<unknown>(
      `/team-management/members/${memberId}/status`,
      {
        method: "POST",
        body: JSON.stringify(payload),
      },
    );

  return teamMemberSchema.parse(
    response,
  );
}

export async function updateReportingLine({
  memberId,
  payload,
}: {
  memberId: string;
  payload: ReportingLinePayload;
}): Promise<TeamMember> {
  const response =
    await apiRequest<unknown>(
      `/team-management/members/${memberId}/reporting-line`,
      {
        method: "PUT",
        body: JSON.stringify(payload),
      },
    );

  return teamMemberSchema.parse(
    response,
  );
}
