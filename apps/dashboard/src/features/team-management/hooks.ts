import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";

import {
  createTeam,
  createTeamMember,
  getMember,
  getMembers,
  getTeamDashboard,
  getTeams,
  updateMemberStatus,
  updateReportingLine,
  updateTeam,
  updateTeamManager,
  updateTeamMember,
} from "./api";
import {
  getActiveServices,
  getProfileImages,
} from "./selectors";
import type {
  MemberFilters,
  TeamFilters,
} from "./types";

export const teamManagementQueryKeys = {
  all: [
    "team-management",
  ] as const,
  dashboard: [
    "team-management",
    "dashboard",
  ] as const,
  services: [
    "team-management",
    "selectors",
    "services",
  ] as const,
  profileImages: [
    "team-management",
    "selectors",
    "profile-images",
  ] as const,
  teams: () => [
    "team-management",
    "teams",
  ] as const,
  teamList: (
    filters: TeamFilters,
  ) => [
    ...teamManagementQueryKeys.teams(),
    "list",
    filters,
  ] as const,
  members: () => [
    "team-management",
    "members",
  ] as const,
  memberList: (
    filters: MemberFilters,
  ) => [
    ...teamManagementQueryKeys.members(),
    "list",
    filters,
  ] as const,
  member: (memberId: string) => [
    ...teamManagementQueryKeys.members(),
    "detail",
    memberId,
  ] as const,
};

export function useTeamMemberServices() {
  return useQuery({
    queryKey:
      teamManagementQueryKeys.services,
    queryFn: getActiveServices,
    staleTime: 5 * 60 * 1000,
  });
}

export function useTeamMemberProfileImages() {
  return useQuery({
    queryKey:
      teamManagementQueryKeys.profileImages,
    queryFn: getProfileImages,
    staleTime: 5 * 60 * 1000,
  });
}

export function useTeamDashboard() {
  return useQuery({
    queryKey:
      teamManagementQueryKeys.dashboard,
    queryFn: getTeamDashboard,
  });
}

export function useTeams(
  filters: TeamFilters,
) {
  return useQuery({
    queryKey:
      teamManagementQueryKeys.teamList(
        filters,
      ),
    queryFn: () =>
      getTeams(filters),
  });
}

export function useMembers(
  filters: MemberFilters,
) {
  return useQuery({
    queryKey:
      teamManagementQueryKeys.memberList(
        filters,
      ),
    queryFn: () =>
      getMembers(filters),
  });
}

export function useMember(
  memberId: string,
  enabled: boolean,
) {
  return useQuery({
    queryKey:
      teamManagementQueryKeys.member(
        memberId,
      ),
    queryFn: () =>
      getMember(memberId),
    enabled,
  });
}

function useInvalidateTeamManagement() {
  const queryClient =
    useQueryClient();

  return async () => {
    await queryClient.invalidateQueries({
      queryKey:
        teamManagementQueryKeys.all,
    });
  };
}

export function useCreateTeam() {
  const invalidate =
    useInvalidateTeamManagement();

  return useMutation({
    mutationFn: createTeam,
    onSuccess: invalidate,
  });
}

export function useUpdateTeam() {
  const invalidate =
    useInvalidateTeamManagement();

  return useMutation({
    mutationFn: updateTeam,
    onSuccess: invalidate,
  });
}

export function useUpdateTeamManager() {
  const invalidate =
    useInvalidateTeamManagement();

  return useMutation({
    mutationFn: updateTeamManager,
    onSuccess: invalidate,
  });
}

export function useCreateTeamMember() {
  const invalidate =
    useInvalidateTeamManagement();

  return useMutation({
    mutationFn:
      createTeamMember,
    onSuccess: invalidate,
  });
}

export function useUpdateTeamMember() {
  const invalidate =
    useInvalidateTeamManagement();

  return useMutation({
    mutationFn:
      updateTeamMember,
    onSuccess: invalidate,
  });
}

export function useUpdateMemberStatus() {
  const invalidate =
    useInvalidateTeamManagement();

  return useMutation({
    mutationFn: updateMemberStatus,
    onSuccess: invalidate,
  });
}

export function useUpdateReportingLine() {
  const invalidate =
    useInvalidateTeamManagement();

  return useMutation({
    mutationFn: updateReportingLine,
    onSuccess: invalidate,
  });
}
