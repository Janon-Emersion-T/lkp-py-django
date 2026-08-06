import {
  BriefcaseBusiness,
  Building2,
  CheckCircle2,
  FilterX,
  GitBranch,
  Globe2,
  LoaderCircle,
  Pencil,
  Search,
  ShieldCheck,
  Star,
  UserPlus,
  UserRoundCog,
  UsersRound,
  X,
} from "lucide-react";
import {
  useMemo,
  useState,
} from "react";

import {
  MemberManagementDialog,
} from "../components/member-management-dialog";
import {
  employmentStatusLabels,
  engagementTypeLabels,
  formatDate,
  formatMetadata,
  parseMetadata,
  slugify,
  statusBadgeClasses,
  teamTypeLabels,
  workLocationTypeLabels,
} from "../formatters";
import {
  useCreateTeam,
  useMember,
  useMembers,
  useTeamDashboard,
  useTeamMemberProfileImages,
  useTeamMemberServices,
  useTeams,
  useUpdateMemberStatus,
  useUpdateReportingLine,
  useUpdateTeam,
  useUpdateTeamManager,
} from "../hooks";
import {
  engagementTypes,
  employmentStatuses,
  teamTypes,
  workLocationTypes,
  type EmploymentStatus,
  type MemberFilters,
  type Team,
  type TeamFilters,
  type TeamMember,
  type TeamPayload,
  type TeamType,
} from "../types";

const defaultTeamFilters:
TeamFilters = {
  search: "",
  teamType: "",
  parentId: "",
  activeState: "all",
  publicState: "all",
  ordering: "sort_order",
};

const defaultMemberFilters:
MemberFilters = {
  search: "",
  employmentStatus: "",
  engagementType: "",
  workLocationType: "",
  country: "",
  teamId: "",
  reportsToId: "",
  publicState: "all",
  featuredState: "all",
  ordering: "sort_order",
};

type WorkspaceTab =
  | "overview"
  | "teams"
  | "members";

type Dialog =
  | "team"
  | "manager"
  | "status"
  | "reporting"
  | null;

export function TeamManagementPage() {
  const [
    tab,
    setTab,
  ] = useState<WorkspaceTab>(
    "overview",
  );

  const [
    teamFilters,
    setTeamFilters,
  ] = useState(defaultTeamFilters);

  const [
    memberFilters,
    setMemberFilters,
  ] = useState(defaultMemberFilters);

  const [
    selectedTeam,
    setSelectedTeam,
  ] = useState<Team | null>(null);

  const [
    selectedMemberId,
    setSelectedMemberId,
  ] = useState("");

  const [
    dialog,
    setDialog,
  ] = useState<Dialog>(null);

  const [
    notice,
    setNotice,
  ] = useState("");

  const [
    memberEditorOpen,
    setMemberEditorOpen,
  ] = useState(false);

  const dashboardQuery =
    useTeamDashboard();

  const teamsQuery =
    useTeams(teamFilters);

  const membersQuery =
    useMembers(memberFilters);

  const memberServicesQuery =
    useTeamMemberServices();

  const memberImagesQuery =
    useTeamMemberProfileImages();

  const memberDetailQuery =
    useMember(
      selectedMemberId,
      selectedMemberId !== "",
    );

  const teams = useMemo(
    () => teamsQuery.data ?? [],
    [teamsQuery.data],
  );

  const members = useMemo(
    () => membersQuery.data ?? [],
    [membersQuery.data],
  );

  const member =
    memberDetailQuery.data ?? null;

  return (
    <div className="space-y-6 pb-10">
      <header className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            People and organization
          </p>

          <h1 className="mt-2 text-2xl font-bold text-slate-950 dark:text-white">
            Team Management
          </h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500 dark:text-slate-400">
            Manage organizational teams, public team
            visibility, managers, employment status,
            reporting lines, and staff profiles consumed
            by internal operations and the Astro website.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => {
              setSelectedMemberId("");
              setMemberEditorOpen(true);
            }}
            className="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
          >
            <UserPlus size={16} />
            Create member
          </button>

          <button
            type="button"
            onClick={() => {
              setSelectedTeam(null);
              setDialog("team");
            }}
            className="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-semibold dark:border-slate-700"
          >
            <Building2 size={16} />
            Create team
          </button>
        </div>
      </header>

      {notice && (
        <div className="flex items-center justify-between rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm font-medium text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950/30 dark:text-emerald-300">
          <span className="flex items-center gap-2">
            <CheckCircle2 size={18} />
            {notice}
          </span>

          <button
            type="button"
            onClick={() =>
              setNotice("")
            }
            aria-label="Dismiss notice"
          >
            <X size={17} />
          </button>
        </div>
      )}

      <nav className="flex flex-wrap gap-2 rounded-xl border border-slate-200 bg-white p-2 dark:border-slate-800 dark:bg-slate-900">
        <TabButton
          active={tab === "overview"}
          label="Overview"
          onClick={() =>
            setTab("overview")
          }
        />

        <TabButton
          active={tab === "teams"}
          label="Teams"
          onClick={() =>
            setTab("teams")
          }
        />

        <TabButton
          active={tab === "members"}
          label="Members"
          onClick={() =>
            setTab("members")
          }
        />
      </nav>

      {tab === "overview" && (
        <Overview
          loading={
            dashboardQuery.isLoading
          }
          error={
            dashboardQuery.isError
              ? dashboardQuery.error.message
              : ""
          }
          data={
            dashboardQuery.data ?? null
          }
        />
      )}

      {tab === "teams" && (
        <TeamsWorkspace
          teams={teams}
          filters={teamFilters}
          loading={teamsQuery.isLoading}
          error={
            teamsQuery.isError
              ? teamsQuery.error.message
              : ""
          }
          onFilters={setTeamFilters}
          onEdit={(team) => {
            setSelectedTeam(team);
            setDialog("team");
          }}
          onManager={(team) => {
            setSelectedTeam(team);
            setDialog("manager");
          }}
        />
      )}

      {tab === "members" && (
        <MembersWorkspace
          members={members}
          teams={teams}
          filters={memberFilters}
          loading={membersQuery.isLoading}
          error={
            membersQuery.isError
              ? membersQuery.error.message
              : ""
          }
          onFilters={setMemberFilters}
          onInspect={(item) =>
            setSelectedMemberId(item.id)
          }
          onEdit={(item) => {
            setSelectedMemberId(item.id);
            setMemberEditorOpen(true);
          }}
          onStatus={(item) => {
            setSelectedMemberId(item.id);
            setDialog("status");
          }}
          onReporting={(item) => {
            setSelectedMemberId(item.id);
            setDialog("reporting");
          }}
        />
      )}

      {!memberEditorOpen && (
        <MemberPanel
          member={member}
          loading={
            memberDetailQuery.isLoading
          }
          onClose={() =>
            setSelectedMemberId("")
          }
        />
      )}

      <MemberManagementDialog
        key={
          memberEditorOpen
            ? selectedMemberId || "new"
            : "closed"
        }
        open={memberEditorOpen}
        member={member}
        memberLoading={
          selectedMemberId !== ""
          && memberDetailQuery.isLoading
        }
        teams={teams}
        members={members}
        services={
          memberServicesQuery.data
          ?? []
        }
        profileImages={
          memberImagesQuery.data
          ?? []
        }
        selectorsLoading={
          memberServicesQuery.isLoading
          || memberImagesQuery.isLoading
        }
        onClose={() => {
          setMemberEditorOpen(false);
          setSelectedMemberId("");
        }}
        onSaved={(message) => {
          setNotice(message);
          setMemberEditorOpen(false);
          setSelectedMemberId("");
        }}
      />

      <TeamManagementDialog
        dialog={dialog}
        team={selectedTeam}
        member={member}
        teams={teams}
        members={members}
        onClose={() =>
          setDialog(null)
        }
        onNotice={setNotice}
      />
    </div>
  );
}

function TabButton({
  active,
  label,
  onClick,
}: {
  active: boolean;
  label: string;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-lg px-4 py-2 text-sm font-semibold ${
        active
          ? "bg-slate-950 text-white dark:bg-white dark:text-slate-950"
          : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
      }`}
    >
      {label}
    </button>
  );
}

function Overview({
  loading,
  error,
  data,
}: {
  loading: boolean;
  error: string;
  data: import("../types").TeamManagementDashboard | null;
}) {
  if (loading) {
    return (
      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        {Array.from({
          length: 8,
        }).map((_, index) => (
          <div
            key={index}
            className="h-28 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800"
          />
        ))}
      </div>
    );
  }

  if (error) {
    return <ErrorBox value={error} />;
  }

  if (!data) {
    return null;
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <SummaryCard
          label="Total teams"
          value={data.total_teams}
          icon={Building2}
        />
        <SummaryCard
          label="Active teams"
          value={data.active_teams}
          icon={ShieldCheck}
        />
        <SummaryCard
          label="Total members"
          value={data.total_members}
          icon={UsersRound}
        />
        <SummaryCard
          label="Active members"
          value={data.active_members}
          icon={CheckCircle2}
        />
        <SummaryCard
          label="Public members"
          value={data.public_members}
          icon={Globe2}
        />
        <SummaryCard
          label="Featured"
          value={data.featured_members}
          icon={Star}
        />
        <SummaryCard
          label="Without primary team"
          value={
            data.members_without_primary_team
          }
          icon={BriefcaseBusiness}
        />
        <SummaryCard
          label="Without manager"
          value={
            data.members_without_manager
          }
          icon={GitBranch}
        />
      </section>

      <section className="grid gap-5 xl:grid-cols-3">
        <BreakdownCard
          title="Employment status"
          values={data.members_by_status}
        />
        <BreakdownCard
          title="Engagement"
          values={
            data.members_by_engagement
          }
        />
        <BreakdownCard
          title="Work location"
          values={
            data.members_by_location
          }
        />
      </section>

      <section className="grid gap-5 xl:grid-cols-2">
        <BreakdownCard
          title="Members by country"
          values={
            data.members_by_country
          }
        />
        <BreakdownCard
          title="Team sizes"
          values={data.team_sizes}
        />
      </section>
    </div>
  );
}

function SummaryCard({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: number;
  icon: typeof Building2;
}) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
      <div className="flex items-center justify-between">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
          {label}
        </p>
        <Icon
          size={17}
          className="text-slate-400"
        />
      </div>

      <p className="mt-3 text-2xl font-bold">
        {value}
      </p>
    </article>
  );
}

function BreakdownCard({
  title,
  values,
}: {
  title: string;
  values: Record<string, number>;
}) {
  const entries =
    Object.entries(values);

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
      <h2 className="font-semibold">
        {title}
      </h2>

      {entries.length === 0 ? (
        <p className="mt-4 text-sm text-slate-500">
          No data available.
        </p>
      ) : (
        <div className="mt-4 space-y-3">
          {entries.map(
            ([label, value]) => (
              <div
                key={label}
                className="flex items-center justify-between gap-3"
              >
                <span className="text-sm capitalize text-slate-600 dark:text-slate-300">
                  {label.replaceAll(
                    "_",
                    " ",
                  )}
                </span>
                <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold dark:bg-slate-800">
                  {value}
                </span>
              </div>
            ),
          )}
        </div>
      )}
    </article>
  );
}

function TeamsWorkspace({
  teams,
  filters,
  loading,
  error,
  onFilters,
  onEdit,
  onManager,
}: {
  teams: Team[];
  filters: TeamFilters;
  loading: boolean;
  error: string;
  onFilters: (
    value: TeamFilters,
  ) => void;
  onEdit: (team: Team) => void;
  onManager: (team: Team) => void;
}) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <div className="grid gap-3 border-b border-slate-200 p-4 lg:grid-cols-[2fr_1fr_1fr_1fr_1fr_auto] dark:border-slate-800">
        <SearchInput
          value={filters.search}
          placeholder="Search teams…"
          onChange={(search) =>
            onFilters({
              ...filters,
              search,
            })
          }
        />

        <select
          value={filters.teamType}
          onChange={(event) =>
            onFilters({
              ...filters,
              teamType:
                event.target.value as TeamType | "",
            })
          }
          className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            All team types
          </option>
          {teamTypes.map((type) => (
            <option
              key={type}
              value={type}
            >
              {teamTypeLabels[type]}
            </option>
          ))}
        </select>

        <select
          value={filters.parentId}
          onChange={(event) =>
            onFilters({
              ...filters,
              parentId:
                event.target.value,
            })
          }
          className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            All parent levels
          </option>
          <option value="root">
            Root teams
          </option>
          {teams.map((team) => (
            <option
              key={team.id}
              value={team.id}
            >
              Children of {team.name}
            </option>
          ))}
        </select>

        <select
          value={filters.activeState}
          onChange={(event) =>
            onFilters({
              ...filters,
              activeState:
                event.target.value as TeamFilters["activeState"],
            })
          }
          className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="all">
            All activity
          </option>
          <option value="active">
            Active
          </option>
          <option value="inactive">
            Inactive
          </option>
        </select>

        <select
          value={filters.publicState}
          onChange={(event) =>
            onFilters({
              ...filters,
              publicState:
                event.target.value as TeamFilters["publicState"],
            })
          }
          className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="all">
            All visibility
          </option>
          <option value="public">
            Public
          </option>
          <option value="private">
            Private
          </option>
        </select>

        <button
          type="button"
          onClick={() =>
            onFilters(
              defaultTeamFilters,
            )
          }
          className="inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 text-sm font-semibold dark:border-slate-700"
        >
          <FilterX size={16} />
          Clear
        </button>
      </div>

      {loading && <LoadingRows />}

      {error && (
        <div className="p-5">
          <ErrorBox value={error} />
        </div>
      )}

      {!loading
      && !error
      && teams.length === 0 && (
        <EmptyState
          title="No teams found"
          message="Create a team or adjust the active filters."
        />
      )}

      {teams.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
            <thead className="bg-slate-50 dark:bg-slate-950/40">
              <tr className="text-left text-xs font-semibold uppercase tracking-wider text-slate-400">
                <th className="px-4 py-3">
                  Team
                </th>
                <th className="px-4 py-3">
                  Type
                </th>
                <th className="px-4 py-3">
                  Manager
                </th>
                <th className="px-4 py-3">
                  Members
                </th>
                <th className="px-4 py-3">
                  State
                </th>
                <th className="px-4 py-3 text-right">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {teams.map((team) => (
                <tr
                  key={team.id}
                  className="text-sm"
                >
                  <td className="px-4 py-4">
                    <p className="font-semibold">
                      {team.name}
                    </p>
                    <p className="mt-1 text-xs text-slate-500">
                      /{team.slug}
                      {team.parent_name
                        ? ` · ${team.parent_name}`
                        : ""}
                    </p>
                  </td>

                  <td className="px-4 py-4">
                    {teamTypeLabels[
                      team.team_type
                    ]}
                  </td>

                  <td className="px-4 py-4">
                    {team.manager_name
                      ?? "Not assigned"}
                  </td>

                  <td className="px-4 py-4">
                    {team.member_count}
                  </td>

                  <td className="px-4 py-4">
                    <div className="flex flex-wrap gap-2">
                      <StateBadge
                        active={
                          team.is_active
                        }
                        trueLabel="Active"
                        falseLabel="Inactive"
                      />
                      <StateBadge
                        active={
                          team.is_public
                        }
                        trueLabel="Public"
                        falseLabel="Private"
                      />
                    </div>
                  </td>

                  <td className="px-4 py-4">
                    <div className="flex justify-end gap-2">
                      <button
                        type="button"
                        onClick={() =>
                          onManager(team)
                        }
                        className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
                      >
                        <UserRoundCog
                          size={14}
                        />
                        Manager
                      </button>

                      <button
                        type="button"
                        onClick={() =>
                          onEdit(team)
                        }
                        className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
                      >
                        <Pencil size={14} />
                        Edit
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function MembersWorkspace({
  members,
  teams,
  filters,
  loading,
  error,
  onFilters,
  onInspect,
  onEdit,
  onStatus,
  onReporting,
}: {
  members: TeamMember[];
  teams: Team[];
  filters: MemberFilters;
  loading: boolean;
  error: string;
  onFilters: (
    value: MemberFilters,
  ) => void;
  onInspect: (
    member: TeamMember,
  ) => void;
  onEdit: (
    member: TeamMember,
  ) => void;
  onStatus: (
    member: TeamMember,
  ) => void;
  onReporting: (
    member: TeamMember,
  ) => void;
}) {
  return (
    <section className="rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <div className="grid gap-3 border-b border-slate-200 p-4 xl:grid-cols-[2fr_1fr_1fr_1fr_1fr_auto] dark:border-slate-800">
        <SearchInput
          value={filters.search}
          placeholder="Search members…"
          onChange={(search) =>
            onFilters({
              ...filters,
              search,
            })
          }
        />

        <select
          value={filters.employmentStatus}
          onChange={(event) =>
            onFilters({
              ...filters,
              employmentStatus:
                event.target.value as EmploymentStatus | "",
            })
          }
          className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            All statuses
          </option>
          {employmentStatuses.map(
            (status) => (
              <option
                key={status}
                value={status}
              >
                {employmentStatusLabels[
                  status
                ]}
              </option>
            ),
          )}
        </select>

        <select
          value={filters.engagementType}
          onChange={(event) =>
            onFilters({
              ...filters,
              engagementType:
                event.target.value as MemberFilters[
                  "engagementType"
                ],
            })
          }
          className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            All engagements
          </option>
          {engagementTypes.map(
            (type) => (
              <option
                key={type}
                value={type}
              >
                {engagementTypeLabels[
                  type
                ]}
              </option>
            ),
          )}
        </select>

        <select
          value={filters.workLocationType}
          onChange={(event) =>
            onFilters({
              ...filters,
              workLocationType:
                event.target.value as MemberFilters[
                  "workLocationType"
                ],
            })
          }
          className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            All locations
          </option>
          {workLocationTypes.map(
            (type) => (
              <option
                key={type}
                value={type}
              >
                {workLocationTypeLabels[
                  type
                ]}
              </option>
            ),
          )}
        </select>

        <select
          value={filters.teamId}
          onChange={(event) =>
            onFilters({
              ...filters,
              teamId:
                event.target.value,
            })
          }
          className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            All teams
          </option>
          {teams.map((team) => (
            <option
              key={team.id}
              value={team.id}
            >
              {team.name}
            </option>
          ))}
        </select>

        <button
          type="button"
          onClick={() =>
            onFilters(
              defaultMemberFilters,
            )
          }
          className="inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 text-sm font-semibold dark:border-slate-700"
        >
          <FilterX size={16} />
          Clear
        </button>
      </div>

      {loading && <LoadingRows />}

      {error && (
        <div className="p-5">
          <ErrorBox value={error} />
        </div>
      )}

      {!loading
      && !error
      && members.length === 0 && (
        <EmptyState
          title="No team members found"
          message="Adjust the filters or add members in the next Team Management milestone."
        />
      )}

      {members.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
            <thead className="bg-slate-50 dark:bg-slate-950/40">
              <tr className="text-left text-xs font-semibold uppercase tracking-wider text-slate-400">
                <th className="px-4 py-3">
                  Member
                </th>
                <th className="px-4 py-3">
                  Primary team
                </th>
                <th className="px-4 py-3">
                  Reports to
                </th>
                <th className="px-4 py-3">
                  Status
                </th>
                <th className="px-4 py-3">
                  Visibility
                </th>
                <th className="px-4 py-3 text-right">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {members.map((item) => {
                const primaryTeam =
                  item.memberships.find(
                    (membership) =>
                      membership.is_primary
                      && membership.is_active,
                  );

                return (
                  <tr
                    key={item.id}
                    className="text-sm"
                  >
                    <td className="px-4 py-4">
                      <button
                        type="button"
                        onClick={() =>
                          onInspect(item)
                        }
                        className="text-left"
                      >
                        <p className="font-semibold">
                          {item.display_name}
                        </p>
                        <p className="mt-1 text-xs text-slate-500">
                          {item.employee_code}
                          {" · "}
                          {item.job_title}
                        </p>
                      </button>
                    </td>

                    <td className="px-4 py-4">
                      {primaryTeam?.team_name
                        ?? "Not assigned"}
                    </td>

                    <td className="px-4 py-4">
                      {item.reports_to_name
                        ?? "Not assigned"}
                    </td>

                    <td className="px-4 py-4">
                      <span
                        className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${statusBadgeClasses(item.employment_status)}`}
                      >
                        {employmentStatusLabels[
                          item.employment_status
                        ]}
                      </span>
                    </td>

                    <td className="px-4 py-4">
                      <div className="flex flex-wrap gap-2">
                        {item.is_public && (
                          <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-950/40 dark:text-blue-300">
                            Public
                          </span>
                        )}
                        {item.is_featured && (
                          <span className="rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-700 dark:bg-amber-950/40 dark:text-amber-300">
                            Featured
                          </span>
                        )}
                        {item.is_leadership && (
                          <span className="rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold text-violet-700 dark:bg-violet-950/40 dark:text-violet-300">
                            Leadership
                          </span>
                        )}
                      </div>
                    </td>

                    <td className="px-4 py-4">
                      <div className="flex justify-end gap-2">
                        <button
                          type="button"
                          onClick={() =>
                            onReporting(item)
                          }
                          className="rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
                        >
                          Reporting line
                        </button>

                        <button
                          type="button"
                          onClick={() =>
                            onStatus(item)
                          }
                          className="rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
                        >
                          Status
                        </button>

                        <button
                          type="button"
                          onClick={() =>
                            onEdit(item)
                          }
                          className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
                        >
                          <Pencil size={13} />
                          Edit
                        </button>

                        <button
                          type="button"
                          onClick={() =>
                            onInspect(item)
                          }
                          className="rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
                        >
                          Inspect
                        </button>
                      </div>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

function SearchInput({
  value,
  placeholder,
  onChange,
}: {
  value: string;
  placeholder: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="relative">
      <Search
        size={16}
        className="absolute left-3 top-3 text-slate-400"
      />

      <input
        value={value}
        placeholder={placeholder}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="h-10 w-full rounded-lg border border-slate-200 bg-white pl-9 pr-3 text-sm dark:border-slate-700 dark:bg-slate-950"
      />
    </label>
  );
}

function StateBadge({
  active,
  trueLabel,
  falseLabel,
}: {
  active: boolean;
  trueLabel: string;
  falseLabel: string;
}) {
  return (
    <span
      className={`rounded-full px-2.5 py-1 text-xs font-semibold ${
        active
          ? "bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300"
          : "bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300"
      }`}
    >
      {active
        ? trueLabel
        : falseLabel}
    </span>
  );
}

function LoadingRows() {
  return (
    <div className="space-y-3 p-5">
      {Array.from({
        length: 6,
      }).map((_, index) => (
        <div
          key={index}
          className="h-16 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800"
        />
      ))}
    </div>
  );
}

function EmptyState({
  title,
  message,
}: {
  title: string;
  message: string;
}) {
  return (
    <div className="px-5 py-16 text-center">
      <UsersRound
        size={34}
        className="mx-auto text-slate-300"
      />
      <h2 className="mt-4 font-semibold">
        {title}
      </h2>
      <p className="mt-2 text-sm text-slate-500">
        {message}
      </p>
    </div>
  );
}

function ErrorBox({
  value,
}: {
  value: string;
}) {
  return (
    <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
      {value}
    </div>
  );
}

function MemberPanel({
  member,
  loading,
  onClose,
}: {
  member: TeamMember | null;
  loading: boolean;
  onClose: () => void;
}) {
  if (!member && !loading) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close member details"
        className="fixed inset-0 z-40 bg-slate-950/50"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-4xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-950">
        <header className="flex items-center justify-between border-b border-slate-200 p-5 dark:border-slate-800">
          <h2 className="font-semibold">
            Team member details
          </h2>
          <button
            type="button"
            onClick={onClose}
            aria-label="Close member details"
          >
            <X size={19} />
          </button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {loading && (
            <div className="h-96 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
          )}

          {member && (
            <>
              <div>
                <h3 className="text-2xl font-bold">
                  {member.display_name}
                </h3>
                <p className="mt-1 text-sm text-slate-500">
                  {member.employee_code}
                  {" · "}
                  {member.job_title}
                </p>
              </div>

              <div className="mt-5 grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
                <Meta
                  label="Status"
                  value={
                    employmentStatusLabels[
                      member.employment_status
                    ]
                  }
                />
                <Meta
                  label="Engagement"
                  value={
                    engagementTypeLabels[
                      member.engagement_type
                    ]
                  }
                />
                <Meta
                  label="Work location"
                  value={
                    workLocationTypeLabels[
                      member.work_location_type
                    ]
                  }
                />
                <Meta
                  label="Reports to"
                  value={
                    member.reports_to_name
                    ?? "Not assigned"
                  }
                />
              </div>

              <section className="mt-6 grid gap-5 lg:grid-cols-2">
                <DetailSection
                  title="Contact and employment"
                  rows={[
                    ["Email", member.email],
                    ["Phone", member.phone],
                    [
                      "Public email",
                      member.public_email,
                    ],
                    [
                      "Public phone",
                      member.public_phone,
                    ],
                    [
                      "Office",
                      member.office_location,
                    ],
                    ["Country", member.country],
                    [
                      "Timezone",
                      member.timezone_name,
                    ],
                    [
                      "Joined",
                      formatDate(
                        member.joined_at,
                      ),
                    ],
                    [
                      "Employment ended",
                      formatDate(
                        member.employment_ended_at,
                      ),
                    ],
                  ]}
                />

                <DetailSection
                  title="Public profile"
                  rows={[
                    [
                      "Professional title",
                      member.professional_title,
                    ],
                    [
                      "Experience",
                      member.years_of_experience
                        === null
                        ? "—"
                        : `${member.years_of_experience} years`,
                    ],
                    [
                      "Leadership",
                      member.is_leadership
                        ? "Yes"
                        : "No",
                    ],
                    [
                      "Public",
                      member.is_public
                        ? "Yes"
                        : "No",
                    ],
                    [
                      "Featured",
                      member.is_featured
                        ? "Yes"
                        : "No",
                    ],
                    [
                      "LinkedIn",
                      member.linkedin_url,
                    ],
                    [
                      "GitHub",
                      member.github_url,
                    ],
                    [
                      "Portfolio",
                      member.portfolio_url,
                    ],
                    [
                      "Website",
                      member.website_url,
                    ],
                  ]}
                />
              </section>

              <section className="mt-6">
                <h4 className="font-semibold">
                  Team memberships
                </h4>
                <div className="mt-3 space-y-2">
                  {member.memberships.length
                    === 0 ? (
                    <p className="text-sm text-slate-500">
                      No team memberships.
                    </p>
                  ) : (
                    member.memberships.map(
                      (membership) => (
                        <div
                          key={membership.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-800"
                        >
                          <div className="flex flex-wrap items-center justify-between gap-3">
                            <div>
                              <p className="font-semibold">
                                {membership.team_name}
                              </p>
                              <p className="mt-1 text-sm text-slate-500">
                                {membership.role_title
                                  || "No role title"}
                              </p>
                            </div>
                            <div className="flex gap-2">
                              {membership.is_primary && (
                                <span className="rounded-full bg-blue-50 px-2.5 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-950/40 dark:text-blue-300">
                                  Primary
                                </span>
                              )}
                              <StateBadge
                                active={
                                  membership.is_active
                                }
                                trueLabel="Active"
                                falseLabel="Inactive"
                              />
                            </div>
                          </div>
                        </div>
                      ),
                    )
                  )}
                </div>
              </section>

              <section className="mt-6">
                <h4 className="font-semibold">
                  Service expertise
                </h4>
                <div className="mt-3 space-y-2">
                  {member.services.length
                    === 0 ? (
                    <p className="text-sm text-slate-500">
                      No service assignments.
                    </p>
                  ) : (
                    member.services.map(
                      (service) => (
                        <div
                          key={service.id}
                          className="flex flex-wrap items-center justify-between gap-3 rounded-xl border border-slate-200 p-4 dark:border-slate-800"
                        >
                          <div>
                            <p className="font-semibold">
                              {service.service_title}
                            </p>
                            <p className="mt-1 text-sm capitalize text-slate-500">
                              {service.expertise_level}
                              {service.years_of_experience
                                !== null
                                ? ` · ${service.years_of_experience} years`
                                : ""}
                            </p>
                          </div>

                          {service.is_primary && (
                            <span className="rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold text-violet-700 dark:bg-violet-950/40 dark:text-violet-300">
                              Primary expertise
                            </span>
                          )}
                        </div>
                      ),
                    )
                  )}
                </div>
              </section>

              <section className="mt-6 space-y-4">
                <TextSection
                  title="Short biography"
                  value={member.short_bio}
                />
                <TextSection
                  title="Biography"
                  value={member.bio}
                />
                <TextSection
                  title="Qualifications"
                  value={member.qualifications}
                />
              </section>
            </>
          )}
        </div>
      </aside>
    </>
  );
}

function Meta({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-slate-200 p-4 dark:border-slate-800">
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
        {label}
      </p>
      <p className="mt-2 text-sm font-semibold">
        {value}
      </p>
    </div>
  );
}

function DetailSection({
  title,
  rows,
}: {
  title: string;
  rows: [string, string][];
}) {
  return (
    <div className="rounded-xl border border-slate-200 p-5 dark:border-slate-800">
      <h4 className="font-semibold">
        {title}
      </h4>

      <dl className="mt-4 space-y-3">
        {rows.map(([label, value]) => (
          <div
            key={label}
            className="grid grid-cols-[130px_1fr] gap-3 text-sm"
          >
            <dt className="text-slate-500">
              {label}
            </dt>
            <dd className="break-all">
              {value || "—"}
            </dd>
          </div>
        ))}
      </dl>
    </div>
  );
}

function TextSection({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div>
      <h4 className="font-semibold">
        {title}
      </h4>
      <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-600 dark:text-slate-300">
        {value || "—"}
      </p>
    </div>
  );
}

function TeamManagementDialog({
  dialog,
  team,
  member,
  teams,
  members,
  onClose,
  onNotice,
}: {
  dialog: Dialog;
  team: Team | null;
  member: TeamMember | null;
  teams: Team[];
  members: TeamMember[];
  onClose: () => void;
  onNotice: (value: string) => void;
}) {
  const createTeamMutation =
    useCreateTeam();
  const updateTeamMutation =
    useUpdateTeam();
  const managerMutation =
    useUpdateTeamManager();
  const statusMutation =
    useUpdateMemberStatus();
  const reportingMutation =
    useUpdateReportingLine();

  if (!dialog) {
    return null;
  }

  const pending =
    createTeamMutation.isPending
    || updateTeamMutation.isPending
    || managerMutation.isPending
    || statusMutation.isPending
    || reportingMutation.isPending;

  return (
    <>
      <button
        type="button"
        onClick={
          pending
            ? undefined
            : onClose
        }
        aria-label="Close team management dialog"
        className="fixed inset-0 z-[60] bg-slate-950/60"
      />

      <div
        role="dialog"
        aria-modal="true"
        className="fixed left-1/2 top-1/2 z-[70] max-h-[90vh] w-[calc(100%-2rem)] max-w-xl -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl dark:border-slate-800 dark:bg-slate-900"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">
            {dialog === "team"
              ? team
                ? "Edit team"
                : "Create team"
              : dialog === "manager"
                ? "Assign team manager"
                : dialog === "status"
                  ? "Change employment status"
                  : "Change reporting line"}
          </h2>

          <button
            type="button"
            onClick={onClose}
            disabled={pending}
            aria-label="Close dialog"
          >
            <X size={18} />
          </button>
        </div>

        {dialog === "team" && (
          <TeamForm
            team={team}
            teams={teams}
            members={members}
            pending={pending}
            onSubmit={async (
              payload,
            ) => {
              const result = team
                ? await updateTeamMutation.mutateAsync({
                    teamId: team.id,
                    payload,
                  })
                : await createTeamMutation.mutateAsync(
                    payload,
                  );

              onNotice(
                `Team “${result.name}” was ${team ? "updated" : "created"}.`,
              );
              onClose();
            }}
          />
        )}

        {dialog === "manager"
        && team && (
          <ManagerForm
            team={team}
            members={members}
            pending={pending}
            onSubmit={async (
              managerId,
            ) => {
              const result =
                await managerMutation.mutateAsync({
                  teamId: team.id,
                  payload: {
                    manager_id:
                      managerId || null,
                  },
                });

              onNotice(
                `Manager assignment for “${result.name}” was updated.`,
              );
              onClose();
            }}
          />
        )}

        {dialog === "status"
        && member && (
          <StatusForm
            member={member}
            pending={pending}
            onSubmit={async (
              status,
              endedAt,
            ) => {
              const result =
                await statusMutation.mutateAsync({
                  memberId: member.id,
                  payload: {
                    employment_status:
                      status,
                    employment_ended_at:
                      endedAt || null,
                  },
                });

              onNotice(
                `${result.display_name} is now ${employmentStatusLabels[result.employment_status]}.`,
              );
              onClose();
            }}
          />
        )}

        {dialog === "reporting"
        && member && (
          <ReportingForm
            member={member}
            members={members}
            pending={pending}
            onSubmit={async (
              managerId,
            ) => {
              const result =
                await reportingMutation.mutateAsync({
                  memberId: member.id,
                  payload: {
                    reports_to_id:
                      managerId || null,
                  },
                });

              onNotice(
                `Reporting line for ${result.display_name} was updated.`,
              );
              onClose();
            }}
          />
        )}
      </div>
    </>
  );
}

function TeamForm({
  team,
  teams,
  members,
  pending,
  onSubmit,
}: {
  team: Team | null;
  teams: Team[];
  members: TeamMember[];
  pending: boolean;
  onSubmit: (
    payload: TeamPayload,
  ) => Promise<void>;
}) {
  const [
    name,
    setName,
  ] = useState(
    team?.name ?? "",
  );

  const [
    slug,
    setSlug,
  ] = useState(
    team?.slug ?? "",
  );

  const [
    teamType,
    setTeamType,
  ] = useState<TeamType>(
    team?.team_type ?? "custom",
  );

  const [
    description,
    setDescription,
  ] = useState(
    team?.description ?? "",
  );

  const [
    parentId,
    setParentId,
  ] = useState(
    team?.parent_id ?? "",
  );

  const [
    managerId,
    setManagerId,
  ] = useState(
    team?.manager_id ?? "",
  );

  const [
    isActive,
    setIsActive,
  ] = useState(
    team?.is_active ?? true,
  );

  const [
    isPublic,
    setIsPublic,
  ] = useState(
    team?.is_public ?? false,
  );

  const [
    sortOrder,
    setSortOrder,
  ] = useState(
    team?.sort_order ?? 0,
  );

  const [
    metadata,
    setMetadata,
  ] = useState(
    formatMetadata(
      team?.metadata ?? {},
    ),
  );

  const [
    error,
    setError,
  ] = useState("");

  return (
    <form
      className="mt-5 space-y-4"
      onSubmit={(event) => {
        event.preventDefault();
        setError("");

        try {
          const payload: TeamPayload = {
            name: name.trim(),
            slug:
              slugify(
                slug || name,
              ),
            team_type: teamType,
            description,
            parent_id:
              parentId || null,
            manager_id:
              managerId || null,
            is_active: isActive,
            is_public: isPublic,
            sort_order: sortOrder,
            metadata:
              parseMetadata(metadata),
          };

          void onSubmit(payload).catch(
            (caught: unknown) => {
              setError(
                caught instanceof Error
                  ? caught.message
                  : "Team operation failed.",
              );
            },
          );
        } catch (caught) {
          setError(
            caught instanceof Error
              ? caught.message
              : "Invalid team data.",
          );
        }
      }}
    >
      <FormInput
        label="Team name"
        value={name}
        required
        onChange={(value) => {
          setName(value);

          if (!team) {
            setSlug(
              slugify(value),
            );
          }
        }}
      />

      <FormInput
        label="Slug"
        value={slug}
        required
        onChange={setSlug}
      />

      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          Team type
        </span>
        <select
          value={teamType}
          onChange={(event) =>
            setTeamType(
              event.target.value as TeamType,
            )
          }
          className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          {teamTypes.map((type) => (
            <option
              key={type}
              value={type}
            >
              {teamTypeLabels[type]}
            </option>
          ))}
        </select>
      </label>

      <FormTextarea
        label="Description"
        value={description}
        onChange={setDescription}
      />

      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          Parent team
        </span>
        <select
          value={parentId}
          onChange={(event) =>
            setParentId(
              event.target.value,
            )
          }
          className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            No parent
          </option>
          {teams
            .filter(
              (item) =>
                item.id !== team?.id,
            )
            .map((item) => (
              <option
                key={item.id}
                value={item.id}
              >
                {item.name}
              </option>
            ))}
        </select>
      </label>

      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          Manager
        </span>
        <select
          value={managerId}
          onChange={(event) =>
            setManagerId(
              event.target.value,
            )
          }
          className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            No manager
          </option>
          {members.map((item) => (
            <option
              key={item.id}
              value={item.id}
            >
              {item.display_name}
            </option>
          ))}
        </select>
        <p className="text-xs text-slate-500">
          The backend requires the manager to be
          an active primary member of this team.
        </p>
      </label>

      <FormInput
        label="Sort order"
        type="number"
        value={String(sortOrder)}
        onChange={(value) =>
          setSortOrder(
            Math.max(
              0,
              Number(value) || 0,
            ),
          )
        }
      />

      <FormTextarea
        label="Metadata JSON"
        value={metadata}
        onChange={setMetadata}
        rows={5}
      />

      <FormCheckbox
        label="Active team"
        checked={isActive}
        onChange={setIsActive}
      />

      <FormCheckbox
        label="Publicly visible team"
        checked={isPublic}
        onChange={setIsPublic}
      />

      {error && (
        <ErrorBox value={error} />
      )}

      <SubmitButton
        pending={pending}
        label={
          team
            ? "Save team"
            : "Create team"
        }
      />
    </form>
  );
}

function ManagerForm({
  team,
  members,
  pending,
  onSubmit,
}: {
  team: Team;
  members: TeamMember[];
  pending: boolean;
  onSubmit: (
    managerId: string,
  ) => Promise<void>;
}) {
  const [
    managerId,
    setManagerId,
  ] = useState(
    team.manager_id ?? "",
  );

  const [
    error,
    setError,
  ] = useState("");

  const eligible =
    members.filter(
      (member) =>
        member.memberships.some(
          (membership) =>
            membership.team_id
              === team.id
            && membership.is_primary
            && membership.is_active,
        ),
    );

  return (
    <form
      className="mt-5 space-y-4"
      onSubmit={(event) => {
        event.preventDefault();
        setError("");

        void onSubmit(managerId).catch(
          (caught: unknown) => {
            setError(
              caught instanceof Error
                ? caught.message
                : "Manager update failed.",
            );
          },
        );
      }}
    >
      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          Team manager
        </span>
        <select
          value={managerId}
          onChange={(event) =>
            setManagerId(
              event.target.value,
            )
          }
          className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            No manager
          </option>
          {eligible.map((member) => (
            <option
              key={member.id}
              value={member.id}
            >
              {member.display_name}
            </option>
          ))}
        </select>
      </label>

      {eligible.length === 0 && (
        <p className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-800 dark:border-amber-900 dark:bg-amber-950/30 dark:text-amber-300">
          No member currently has an active primary
          membership in this team.
        </p>
      )}

      {error && (
        <ErrorBox value={error} />
      )}

      <SubmitButton
        pending={pending}
        label="Update manager"
      />
    </form>
  );
}

function StatusForm({
  member,
  pending,
  onSubmit,
}: {
  member: TeamMember;
  pending: boolean;
  onSubmit: (
    status: EmploymentStatus,
    endedAt: string,
  ) => Promise<void>;
}) {
  const [
    status,
    setStatus,
  ] = useState(
    member.employment_status,
  );

  const [
    endedAt,
    setEndedAt,
  ] = useState(
    member.employment_ended_at
      ?? "",
  );

  const [
    error,
    setError,
  ] = useState("");

  return (
    <form
      className="mt-5 space-y-4"
      onSubmit={(event) => {
        event.preventDefault();
        setError("");

        void onSubmit(
          status,
          endedAt,
        ).catch(
          (caught: unknown) => {
            setError(
              caught instanceof Error
                ? caught.message
                : "Status update failed.",
            );
          },
        );
      }}
    >
      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          Employment status
        </span>
        <select
          value={status}
          onChange={(event) =>
            setStatus(
              event.target.value as EmploymentStatus,
            )
          }
          className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          {employmentStatuses.map(
            (value) => (
              <option
                key={value}
                value={value}
              >
                {employmentStatusLabels[
                  value
                ]}
              </option>
            ),
          )}
        </select>
      </label>

      <FormInput
        label="Employment end date"
        type="date"
        value={endedAt}
        onChange={setEndedAt}
      />

      {error && (
        <ErrorBox value={error} />
      )}

      <SubmitButton
        pending={pending}
        label="Update status"
      />
    </form>
  );
}

function ReportingForm({
  member,
  members,
  pending,
  onSubmit,
}: {
  member: TeamMember;
  members: TeamMember[];
  pending: boolean;
  onSubmit: (
    managerId: string,
  ) => Promise<void>;
}) {
  const [
    managerId,
    setManagerId,
  ] = useState(
    member.reports_to_id ?? "",
  );

  const [
    error,
    setError,
  ] = useState("");

  return (
    <form
      className="mt-5 space-y-4"
      onSubmit={(event) => {
        event.preventDefault();
        setError("");

        void onSubmit(managerId).catch(
          (caught: unknown) => {
            setError(
              caught instanceof Error
                ? caught.message
                : "Reporting-line update failed.",
            );
          },
        );
      }}
    >
      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          Reports to
        </span>
        <select
          value={managerId}
          onChange={(event) =>
            setManagerId(
              event.target.value,
            )
          }
          className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            No reporting manager
          </option>
          {members
            .filter(
              (item) =>
                item.id !== member.id,
            )
            .map((item) => (
              <option
                key={item.id}
                value={item.id}
              >
                {item.display_name}
              </option>
            ))}
        </select>
      </label>

      <p className="text-xs leading-5 text-slate-500">
        The backend rejects self-reporting and circular
        reporting-line assignments.
      </p>

      {error && (
        <ErrorBox value={error} />
      )}

      <SubmitButton
        pending={pending}
        label="Update reporting line"
      />
    </form>
  );
}

function FormInput({
  label,
  value,
  onChange,
  required = false,
  type = "text",
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
  type?: string;
}) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm font-semibold">
        {label}
      </span>
      <input
        type={type}
        value={value}
        required={required}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
      />
    </label>
  );
}

function FormTextarea({
  label,
  value,
  onChange,
  rows = 3,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  rows?: number;
}) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm font-semibold">
        {label}
      </span>
      <textarea
        value={value}
        rows={rows}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 font-mono text-sm dark:border-slate-700 dark:bg-slate-950"
      />
    </label>
  );
}

function FormCheckbox({
  label,
  checked,
  onChange,
}: {
  label: string;
  checked: boolean;
  onChange: (value: boolean) => void;
}) {
  return (
    <label className="flex items-center gap-3 text-sm font-medium">
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) =>
          onChange(
            event.target.checked,
          )
        }
        className="size-4"
      />
      {label}
    </label>
  );
}

function SubmitButton({
  pending,
  label,
}: {
  pending: boolean;
  label: string;
}) {
  return (
    <button
      type="submit"
      disabled={pending}
      className="inline-flex w-full items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50"
    >
      {pending && (
        <LoaderCircle
          size={16}
          className="animate-spin"
        />
      )}
      {label}
    </button>
  );
}
