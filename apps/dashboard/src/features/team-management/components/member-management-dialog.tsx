import {
  ChevronDown,
  ChevronUp,
  Image,
  LoaderCircle,
  Plus,
  Trash2,
  UserRound,
  X,
} from "lucide-react";
import {
  useMemo,
  useState,
} from "react";

import {
  resolveMediaUrl,
} from "../../media-library/formatters";
import {
  employmentStatusLabels,
  engagementTypeLabels,
  formatMetadata,
  parseMetadata,
  workLocationTypeLabels,
} from "../formatters";
import {
  useCreateTeamMember,
  useUpdateTeamMember,
} from "../hooks";
import {
  engagementTypes,
  employmentStatuses,
  expertiseLevels,
  workLocationTypes,
  type EmploymentStatus,
  type EngagementType,
  type ExpertiseLevel,
  type ProfileImageSelectorItem,
  type ServiceSelectorItem,
  type Team,
  type TeamMember,
  type TeamMemberPayload,
  type TeamMemberServiceInput,
  type TeamMembershipInput,
  type WorkLocationType,
} from "../types";

interface MemberManagementDialogProps {
  open: boolean;
  member: TeamMember | null;
  memberLoading: boolean;
  teams: Team[];
  members: TeamMember[];
  services: ServiceSelectorItem[];
  profileImages: ProfileImageSelectorItem[];
  selectorsLoading: boolean;
  onClose: () => void;
  onSaved: (message: string) => void;
}

interface BasicState {
  employeeCode: string;
  firstName: string;
  lastName: string;
  preferredName: string;
  jobTitle: string;
  professionalTitle: string;
  email: string;
  phone: string;
  publicEmail: string;
  publicPhone: string;
  profileImageId: string;
  bio: string;
  shortBio: string;
  qualifications: string;
  yearsOfExperience: string;
  engagementType: EngagementType;
  employmentStatus: EmploymentStatus;
  workLocationType: WorkLocationType;
  officeLocation: string;
  country: string;
  timezoneName: string;
  joinedAt: string;
  employmentEndedAt: string;
  reportsToId: string;
  linkedinUrl: string;
  githubUrl: string;
  portfolioUrl: string;
  websiteUrl: string;
  isLeadership: boolean;
  isPublic: boolean;
  isFeatured: boolean;
  sortOrder: string;
  metadata: string;
}

const emptyMembership = (): TeamMembershipInput => ({
  team_id: "",
  role_title: "",
  is_primary: false,
  is_active: true,
  joined_at: null,
  left_at: null,
  sort_order: 0,
});

const emptyService = (): TeamMemberServiceInput => ({
  service_id: "",
  expertise_level: "proficient",
  years_of_experience: null,
  is_primary: false,
  is_public: true,
  sort_order: 0,
});

function toDateInput(
  value: string | null,
): string {
  if (!value) {
    return "";
  }

  return value.slice(0, 10);
}

function getInitialState(
  member: TeamMember | null,
): BasicState {
  return {
    employeeCode:
      member?.employee_code ?? "",
    firstName:
      member?.first_name ?? "",
    lastName:
      member?.last_name ?? "",
    preferredName:
      member?.preferred_name ?? "",
    jobTitle:
      member?.job_title ?? "",
    professionalTitle:
      member?.professional_title ?? "",
    email:
      member?.email ?? "",
    phone:
      member?.phone ?? "",
    publicEmail:
      member?.public_email ?? "",
    publicPhone:
      member?.public_phone ?? "",
    profileImageId:
      member?.profile_image_id ?? "",
    bio:
      member?.bio ?? "",
    shortBio:
      member?.short_bio ?? "",
    qualifications:
      member?.qualifications ?? "",
    yearsOfExperience:
      member?.years_of_experience === null
        || member?.years_of_experience === undefined
        ? ""
        : String(
            member.years_of_experience,
          ),
    engagementType:
      member?.engagement_type
      ?? "full_time",
    employmentStatus:
      member?.employment_status
      ?? "active",
    workLocationType:
      member?.work_location_type
      ?? "onsite",
    officeLocation:
      member?.office_location ?? "",
    country:
      member?.country ?? "",
    timezoneName:
      member?.timezone_name
      ?? "Asia/Colombo",
    joinedAt:
      toDateInput(
        member?.joined_at ?? null,
      ),
    employmentEndedAt:
      toDateInput(
        member?.employment_ended_at
        ?? null,
      ),
    reportsToId:
      member?.reports_to_id ?? "",
    linkedinUrl:
      member?.linkedin_url ?? "",
    githubUrl:
      member?.github_url ?? "",
    portfolioUrl:
      member?.portfolio_url ?? "",
    websiteUrl:
      member?.website_url ?? "",
    isLeadership:
      member?.is_leadership ?? false,
    isPublic:
      member?.is_public ?? false,
    isFeatured:
      member?.is_featured ?? false,
    sortOrder:
      String(member?.sort_order ?? 0),
    metadata:
      formatMetadata(
        member?.metadata ?? {},
      ),
  };
}

function getInitialMemberships(
  member: TeamMember | null,
): TeamMembershipInput[] {
  if (!member) {
    return [];
  }

  return member.memberships.map(
    (membership) => ({
      team_id: membership.team_id,
      role_title:
        membership.role_title,
      is_primary:
        membership.is_primary,
      is_active:
        membership.is_active,
      joined_at:
        toDateInput(
          membership.joined_at,
        ) || null,
      left_at:
        toDateInput(
          membership.left_at,
        ) || null,
      sort_order:
        membership.sort_order,
    }),
  );
}

function getInitialServices(
  member: TeamMember | null,
): TeamMemberServiceInput[] {
  if (!member) {
    return [];
  }

  return member.services.map(
    (service) => ({
      service_id:
        service.service_id,
      expertise_level:
        service.expertise_level as ExpertiseLevel,
      years_of_experience:
        service.years_of_experience
          === null
          ? null
          : Number(
              service.years_of_experience,
            ),
      is_primary:
        service.is_primary,
      is_public:
        service.is_public,
      sort_order:
        service.sort_order,
    }),
  );
}

function validatePayload(
  payload: TeamMemberPayload,
) {
  if (!payload.employee_code) {
    throw new Error(
      "Employee code is required.",
    );
  }

  if (!payload.first_name) {
    throw new Error(
      "First name is required.",
    );
  }

  if (!payload.job_title) {
    throw new Error(
      "Job title is required.",
    );
  }

  const teamIds =
    payload.memberships.map(
      (item) => item.team_id,
    );

  if (
    teamIds.some(
      (teamId) => !teamId,
    )
  ) {
    throw new Error(
      "Every membership must select a team.",
    );
  }

  if (
    new Set(teamIds).size
    !== teamIds.length
  ) {
    throw new Error(
      "A team cannot be assigned more than once.",
    );
  }

  const primaryMemberships =
    payload.memberships.filter(
      (item) =>
        item.is_primary
        && item.is_active,
    );

  if (
    primaryMemberships.length > 1
  ) {
    throw new Error(
      "Only one active primary team is allowed.",
    );
  }

  const serviceIds =
    payload.services.map(
      (item) => item.service_id,
    );

  if (
    serviceIds.some(
      (serviceId) => !serviceId,
    )
  ) {
    throw new Error(
      "Every expertise assignment must select a service.",
    );
  }

  if (
    new Set(serviceIds).size
    !== serviceIds.length
  ) {
    throw new Error(
      "A service cannot be assigned more than once.",
    );
  }

  if (
    payload.reports_to_id
    && payload.reports_to_id
      === payload.employee_code
  ) {
    throw new Error(
      "A member cannot report to themselves.",
    );
  }
}

export function MemberManagementDialog({
  open,
  member,
  memberLoading,
  teams,
  members,
  services,
  profileImages,
  selectorsLoading,
  onClose,
  onSaved,
}: MemberManagementDialogProps) {
  const [
    form,
    setForm,
  ] = useState<BasicState>(
    () => getInitialState(member),
  );

  const [
    memberships,
    setMemberships,
  ] = useState<TeamMembershipInput[]>(
    () => getInitialMemberships(
      member,
    ),
  );

  const [
    expertise,
    setExpertise,
  ] = useState<TeamMemberServiceInput[]>(
    () => getInitialServices(member),
  );

  const [
    activeSection,
    setActiveSection,
  ] = useState(
    "identity",
  );

  const [
    error,
    setError,
  ] = useState("");

  const createMutation =
    useCreateTeamMember();

  const updateMutation =
    useUpdateTeamMember();

  const pending =
    createMutation.isPending
    || updateMutation.isPending;

  const selectedImage =
    useMemo(
      () =>
        profileImages.find(
          (image) =>
            image.id
            === form.profileImageId,
        ) ?? null,
      [
        form.profileImageId,
        profileImages,
      ],
    );

  if (!open) {
    return null;
  }

  function updateForm<
    Key extends keyof BasicState,
  >(
    key: Key,
    value: BasicState[Key],
  ) {
    setForm(
      (current) => ({
        ...current,
        [key]: value,
      }),
    );
  }

  function updateMembership(
    index: number,
    values: Partial<
      TeamMembershipInput
    >,
  ) {
    setMemberships(
      (current) =>
        current.map(
          (item, itemIndex) =>
            itemIndex === index
              ? {
                  ...item,
                  ...values,
                }
              : item,
        ),
    );
  }

  function setPrimaryMembership(
    index: number,
  ) {
    setMemberships(
      (current) =>
        current.map(
          (item, itemIndex) => ({
            ...item,
            is_primary:
              itemIndex === index,
            is_active:
              itemIndex === index
                ? true
                : item.is_active,
          }),
        ),
    );
  }

  function updateExpertise(
    index: number,
    values: Partial<
      TeamMemberServiceInput
    >,
  ) {
    setExpertise(
      (current) =>
        current.map(
          (item, itemIndex) =>
            itemIndex === index
              ? {
                  ...item,
                  ...values,
                }
              : item,
        ),
    );
  }

  function buildPayload():
  TeamMemberPayload {
    return {
      user_id: null,
      employee_code:
        form.employeeCode.trim(),
      first_name:
        form.firstName.trim(),
      last_name:
        form.lastName.trim(),
      preferred_name:
        form.preferredName.trim(),
      job_title:
        form.jobTitle.trim(),
      professional_title:
        form.professionalTitle.trim(),
      email:
        form.email.trim(),
      phone:
        form.phone.trim(),
      public_email:
        form.publicEmail.trim(),
      public_phone:
        form.publicPhone.trim(),
      profile_image_id:
        form.profileImageId || null,
      bio: form.bio,
      short_bio: form.shortBio,
      qualifications:
        form.qualifications,
      years_of_experience:
        form.yearsOfExperience
          ? Math.max(
              0,
              Number(
                form.yearsOfExperience,
              ),
            )
          : null,
      engagement_type:
        form.engagementType,
      employment_status:
        form.employmentStatus,
      work_location_type:
        form.workLocationType,
      office_location:
        form.officeLocation.trim(),
      country:
        form.country.trim(),
      timezone_name:
        form.timezoneName.trim()
        || "Asia/Colombo",
      joined_at:
        form.joinedAt || null,
      employment_ended_at:
        form.employmentEndedAt
        || null,
      reports_to_id:
        form.reportsToId || null,
      linkedin_url:
        form.linkedinUrl.trim(),
      github_url:
        form.githubUrl.trim(),
      portfolio_url:
        form.portfolioUrl.trim(),
      website_url:
        form.websiteUrl.trim(),
      is_leadership:
        form.isLeadership,
      is_public:
        form.isPublic,
      is_featured:
        form.isFeatured,
      sort_order:
        Math.max(
          0,
          Number(form.sortOrder) || 0,
        ),
      metadata:
        parseMetadata(form.metadata),
      memberships:
        memberships.map(
          (item, index) => ({
            ...item,
            joined_at:
              item.joined_at || null,
            left_at:
              item.left_at || null,
            sort_order: index,
          }),
        ),
      services:
        expertise.map(
          (item, index) => ({
            ...item,
            years_of_experience:
              item.years_of_experience
              === null
                ? null
                : Math.max(
                    0,
                    Number(
                      item.years_of_experience,
                    ),
                  ),
            sort_order: index,
          }),
        ),
    };
  }

  async function submit() {
    setError("");

    try {
      const payload =
        buildPayload();

      validatePayload(payload);

      const saved = member
        ? await updateMutation.mutateAsync({
            memberId: member.id,
            payload,
          })
        : await createMutation.mutateAsync(
            payload,
          );

      onSaved(
        `${saved.display_name} was ${
          member
            ? "updated"
            : "created"
        } successfully.`,
      );

      onClose();
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Member operation failed.",
      );
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={
          pending
            ? undefined
            : onClose
        }
        aria-label="Close member editor"
        className="fixed inset-0 z-[80] bg-slate-950/60"
      />

      <section
        role="dialog"
        aria-modal="true"
        aria-label={
          member
            ? "Edit team member"
            : "Create team member"
        }
        className="fixed inset-y-0 right-0 z-[90] flex w-full max-w-5xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-950"
      >
        <header className="flex flex-col gap-4 border-b border-slate-200 p-5 sm:flex-row sm:items-center sm:justify-between dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Team member profile
            </p>

            <h2 className="mt-1 text-xl font-bold">
              {member
                ? `Edit ${member.display_name}`
                : "Create team member"}
            </h2>
          </div>

          <div className="flex gap-2">
            <button
              type="button"
              disabled={pending}
              onClick={onClose}
              className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-semibold dark:border-slate-700"
            >
              Cancel
            </button>

            <button
              type="button"
              disabled={
                pending
                || memberLoading
                || selectorsLoading
              }
              onClick={() => {
                void submit();
              }}
              className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
            >
              {pending && (
                <LoaderCircle
                  size={16}
                  className="animate-spin"
                />
              )}
              {member
                ? "Save member"
                : "Create member"}
            </button>

            <button
              type="button"
              disabled={pending}
              onClick={onClose}
              aria-label="Close member editor"
              className="rounded-lg border border-slate-200 p-2 dark:border-slate-700"
            >
              <X size={18} />
            </button>
          </div>
        </header>

        <div className="grid min-h-0 flex-1 lg:grid-cols-[220px_1fr]">
          <nav className="border-b border-slate-200 p-4 lg:border-b-0 lg:border-r dark:border-slate-800">
            <div className="grid gap-1 sm:grid-cols-3 lg:grid-cols-1">
              <SectionButton
                active={
                  activeSection
                  === "identity"
                }
                label="Identity"
                onClick={() =>
                  setActiveSection(
                    "identity",
                  )
                }
              />
              <SectionButton
                active={
                  activeSection
                  === "employment"
                }
                label="Employment"
                onClick={() =>
                  setActiveSection(
                    "employment",
                  )
                }
              />
              <SectionButton
                active={
                  activeSection
                  === "public"
                }
                label="Public profile"
                onClick={() =>
                  setActiveSection(
                    "public",
                  )
                }
              />
              <SectionButton
                active={
                  activeSection
                  === "memberships"
                }
                label="Memberships"
                onClick={() =>
                  setActiveSection(
                    "memberships",
                  )
                }
              />
              <SectionButton
                active={
                  activeSection
                  === "services"
                }
                label="Service expertise"
                onClick={() =>
                  setActiveSection(
                    "services",
                  )
                }
              />
              <SectionButton
                active={
                  activeSection
                  === "advanced"
                }
                label="Advanced"
                onClick={() =>
                  setActiveSection(
                    "advanced",
                  )
                }
              />
            </div>
          </nav>

          <main className="overflow-y-auto p-5 lg:p-7">
            {(memberLoading
              || selectorsLoading) && (
              <div className="mb-5 flex items-center gap-2 rounded-xl border border-blue-200 bg-blue-50 p-4 text-sm text-blue-700 dark:border-blue-900 dark:bg-blue-950/30 dark:text-blue-300">
                <LoaderCircle
                  size={16}
                  className="animate-spin"
                />
                Loading member editor data…
              </div>
            )}

            {error && (
              <div className="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
                {error}
              </div>
            )}

            {activeSection
              === "identity" && (
              <IdentitySection
                form={form}
                selectedImage={
                  selectedImage
                }
                profileImages={
                  profileImages
                }
                onUpdate={updateForm}
              />
            )}

            {activeSection
              === "employment" && (
              <EmploymentSection
                form={form}
                members={members}
                currentMemberId={
                  member?.id ?? ""
                }
                onUpdate={updateForm}
              />
            )}

            {activeSection
              === "public" && (
              <PublicProfileSection
                form={form}
                onUpdate={updateForm}
              />
            )}

            {activeSection
              === "memberships" && (
              <MembershipsSection
                memberships={
                  memberships
                }
                teams={teams}
                onAdd={() =>
                  setMemberships(
                    (current) => [
                      ...current,
                      emptyMembership(),
                    ],
                  )
                }
                onRemove={(index) =>
                  setMemberships(
                    (current) =>
                      current.filter(
                        (_, itemIndex) =>
                          itemIndex
                          !== index,
                      ),
                  )
                }
                onMove={(
                  index,
                  direction,
                ) =>
                  setMemberships(
                    (current) =>
                      moveItem(
                        current,
                        index,
                        direction,
                      ),
                  )
                }
                onUpdate={
                  updateMembership
                }
                onPrimary={
                  setPrimaryMembership
                }
              />
            )}

            {activeSection
              === "services" && (
              <ServicesSection
                assignments={
                  expertise
                }
                services={services}
                onAdd={() =>
                  setExpertise(
                    (current) => [
                      ...current,
                      emptyService(),
                    ],
                  )
                }
                onRemove={(index) =>
                  setExpertise(
                    (current) =>
                      current.filter(
                        (_, itemIndex) =>
                          itemIndex
                          !== index,
                      ),
                  )
                }
                onMove={(
                  index,
                  direction,
                ) =>
                  setExpertise(
                    (current) =>
                      moveItem(
                        current,
                        index,
                        direction,
                      ),
                  )
                }
                onUpdate={
                  updateExpertise
                }
              />
            )}

            {activeSection
              === "advanced" && (
              <AdvancedSection
                form={form}
                onUpdate={updateForm}
              />
            )}
          </main>
        </div>
      </section>
    </>
  );
}

function moveItem<Item>(
  items: Item[],
  index: number,
  direction: -1 | 1,
): Item[] {
  const target =
    index + direction;

  if (
    target < 0
    || target >= items.length
  ) {
    return items;
  }

  const output = [...items];
  const current = output[index];
  const replacement =
    output[target];

  if (
    current === undefined
    || replacement === undefined
  ) {
    return items;
  }

  output[index] = replacement;
  output[target] = current;

  return output;
}

function SectionButton({
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
      className={`rounded-lg px-3 py-2 text-left text-sm font-semibold ${
        active
          ? "bg-slate-950 text-white dark:bg-white dark:text-slate-950"
          : "text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-800"
      }`}
    >
      {label}
    </button>
  );
}

function IdentitySection({
  form,
  selectedImage,
  profileImages,
  onUpdate,
}: {
  form: BasicState;
  selectedImage:
    ProfileImageSelectorItem | null;
  profileImages:
    ProfileImageSelectorItem[];
  onUpdate: <
    Key extends keyof BasicState,
  >(
    key: Key,
    value: BasicState[Key],
  ) => void;
}) {
  return (
    <Section
      title="Identity and contact"
      description="Internal identity, contact details, and the Media Library profile image."
    >
      <div className="grid gap-5 xl:grid-cols-[220px_1fr]">
        <div>
          <div className="flex aspect-square items-center justify-center overflow-hidden rounded-2xl border border-slate-200 bg-slate-100 dark:border-slate-800 dark:bg-slate-900">
            {selectedImage ? (
              <img
                src={resolveMediaUrl(
                  selectedImage.file_url,
                )}
                alt={
                  selectedImage.alt_text
                  || selectedImage.title
                }
                className="h-full w-full object-cover"
              />
            ) : (
              <UserRound
                size={50}
                className="text-slate-300"
              />
            )}
          </div>

          <label className="mt-3 block space-y-1.5">
            <span className="text-sm font-semibold">
              Profile image
            </span>

            <select
              value={
                form.profileImageId
              }
              onChange={(event) =>
                onUpdate(
                  "profileImageId",
                  event.target.value,
                )
              }
              className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
            >
              <option value="">
                No profile image
              </option>

              {profileImages.map(
                (image) => (
                  <option
                    key={image.id}
                    value={image.id}
                  >
                    {image.title}
                  </option>
                ),
              )}
            </select>
          </label>

          <p className="mt-2 flex items-start gap-2 text-xs leading-5 text-slate-500">
            <Image
              size={14}
              className="mt-0.5 shrink-0"
            />
            Images are selected from the
            Media Library.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Input
            label="Employee code"
            value={form.employeeCode}
            required
            onChange={(value) =>
              onUpdate(
                "employeeCode",
                value,
              )
            }
          />

          <Input
            label="Preferred name"
            value={
              form.preferredName
            }
            onChange={(value) =>
              onUpdate(
                "preferredName",
                value,
              )
            }
          />

          <Input
            label="First name"
            value={form.firstName}
            required
            onChange={(value) =>
              onUpdate(
                "firstName",
                value,
              )
            }
          />

          <Input
            label="Last name"
            value={form.lastName}
            onChange={(value) =>
              onUpdate(
                "lastName",
                value,
              )
            }
          />

          <Input
            label="Internal email"
            type="email"
            value={form.email}
            onChange={(value) =>
              onUpdate("email", value)
            }
          />

          <Input
            label="Internal phone"
            value={form.phone}
            onChange={(value) =>
              onUpdate("phone", value)
            }
          />
        </div>
      </div>
    </Section>
  );
}

function EmploymentSection({
  form,
  members,
  currentMemberId,
  onUpdate,
}: {
  form: BasicState;
  members: TeamMember[];
  currentMemberId: string;
  onUpdate: <
    Key extends keyof BasicState,
  >(
    key: Key,
    value: BasicState[Key],
  ) => void;
}) {
  return (
    <Section
      title="Employment"
      description="Operational employment, reporting, location, and engagement details."
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <Input
          label="Job title"
          value={form.jobTitle}
          required
          onChange={(value) =>
            onUpdate(
              "jobTitle",
              value,
            )
          }
        />

        <Input
          label="Professional title"
          value={
            form.professionalTitle
          }
          onChange={(value) =>
            onUpdate(
              "professionalTitle",
              value,
            )
          }
        />

        <Select
          label="Engagement type"
          value={form.engagementType}
          options={engagementTypes.map(
            (value) => ({
              value,
              label:
                engagementTypeLabels[
                  value
                ],
            }),
          )}
          onChange={(value) =>
            onUpdate(
              "engagementType",
              value as EngagementType,
            )
          }
        />

        <Select
          label="Employment status"
          value={
            form.employmentStatus
          }
          options={
            employmentStatuses.map(
              (value) => ({
                value,
                label:
                  employmentStatusLabels[
                    value
                  ],
              }),
            )
          }
          onChange={(value) =>
            onUpdate(
              "employmentStatus",
              value as EmploymentStatus,
            )
          }
        />

        <Select
          label="Work location"
          value={
            form.workLocationType
          }
          options={
            workLocationTypes.map(
              (value) => ({
                value,
                label:
                  workLocationTypeLabels[
                    value
                  ],
              }),
            )
          }
          onChange={(value) =>
            onUpdate(
              "workLocationType",
              value as WorkLocationType,
            )
          }
        />

        <Input
          label="Office location"
          value={
            form.officeLocation
          }
          onChange={(value) =>
            onUpdate(
              "officeLocation",
              value,
            )
          }
        />

        <Input
          label="Country"
          value={form.country}
          onChange={(value) =>
            onUpdate(
              "country",
              value,
            )
          }
        />

        <Input
          label="Timezone"
          value={
            form.timezoneName
          }
          onChange={(value) =>
            onUpdate(
              "timezoneName",
              value,
            )
          }
        />

        <Input
          label="Joined date"
          type="date"
          value={form.joinedAt}
          onChange={(value) =>
            onUpdate(
              "joinedAt",
              value,
            )
          }
        />

        <Input
          label="Employment end date"
          type="date"
          value={
            form.employmentEndedAt
          }
          onChange={(value) =>
            onUpdate(
              "employmentEndedAt",
              value,
            )
          }
        />

        <label className="block space-y-1.5 sm:col-span-2">
          <span className="text-sm font-semibold">
            Reports to
          </span>

          <select
            value={form.reportsToId}
            onChange={(event) =>
              onUpdate(
                "reportsToId",
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
                (member) =>
                  member.id
                  !== currentMemberId,
              )
              .map((member) => (
                <option
                  key={member.id}
                  value={member.id}
                >
                  {member.display_name}
                  {" · "}
                  {member.job_title}
                </option>
              ))}
          </select>
        </label>

        <Input
          label="Years of experience"
          type="number"
          min="0"
          value={
            form.yearsOfExperience
          }
          onChange={(value) =>
            onUpdate(
              "yearsOfExperience",
              value,
            )
          }
        />

        <Input
          label="Sort order"
          type="number"
          min="0"
          value={form.sortOrder}
          onChange={(value) =>
            onUpdate(
              "sortOrder",
              value,
            )
          }
        />
      </div>
    </Section>
  );
}

function PublicProfileSection({
  form,
  onUpdate,
}: {
  form: BasicState;
  onUpdate: <
    Key extends keyof BasicState,
  >(
    key: Key,
    value: BasicState[Key],
  ) => void;
}) {
  return (
    <Section
      title="Public profile"
      description="Content and contact data available to the Astro public website."
    >
      <div className="grid gap-4 sm:grid-cols-2">
        <Input
          label="Public email"
          type="email"
          value={form.publicEmail}
          onChange={(value) =>
            onUpdate(
              "publicEmail",
              value,
            )
          }
        />

        <Input
          label="Public phone"
          value={form.publicPhone}
          onChange={(value) =>
            onUpdate(
              "publicPhone",
              value,
            )
          }
        />

        <Input
          label="LinkedIn URL"
          type="url"
          value={form.linkedinUrl}
          onChange={(value) =>
            onUpdate(
              "linkedinUrl",
              value,
            )
          }
        />

        <Input
          label="GitHub URL"
          type="url"
          value={form.githubUrl}
          onChange={(value) =>
            onUpdate(
              "githubUrl",
              value,
            )
          }
        />

        <Input
          label="Portfolio URL"
          type="url"
          value={form.portfolioUrl}
          onChange={(value) =>
            onUpdate(
              "portfolioUrl",
              value,
            )
          }
        />

        <Input
          label="Website URL"
          type="url"
          value={form.websiteUrl}
          onChange={(value) =>
            onUpdate(
              "websiteUrl",
              value,
            )
          }
        />
      </div>

      <div className="mt-5 space-y-4">
        <Textarea
          label="Short biography"
          value={form.shortBio}
          rows={4}
          onChange={(value) =>
            onUpdate(
              "shortBio",
              value,
            )
          }
        />

        <Textarea
          label="Full biography"
          value={form.bio}
          rows={8}
          onChange={(value) =>
            onUpdate("bio", value)
          }
        />

        <Textarea
          label="Qualifications"
          value={
            form.qualifications
          }
          rows={6}
          onChange={(value) =>
            onUpdate(
              "qualifications",
              value,
            )
          }
        />
      </div>

      <div className="mt-5 grid gap-3 sm:grid-cols-3">
        <Checkbox
          label="Leadership member"
          checked={
            form.isLeadership
          }
          onChange={(value) =>
            onUpdate(
              "isLeadership",
              value,
            )
          }
        />

        <Checkbox
          label="Public profile"
          checked={form.isPublic}
          onChange={(value) =>
            onUpdate(
              "isPublic",
              value,
            )
          }
        />

        <Checkbox
          label="Featured member"
          checked={form.isFeatured}
          onChange={(value) =>
            onUpdate(
              "isFeatured",
              value,
            )
          }
        />
      </div>
    </Section>
  );
}

function MembershipsSection({
  memberships,
  teams,
  onAdd,
  onRemove,
  onMove,
  onUpdate,
  onPrimary,
}: {
  memberships:
    TeamMembershipInput[];
  teams: Team[];
  onAdd: () => void;
  onRemove: (index: number) => void;
  onMove: (
    index: number,
    direction: -1 | 1,
  ) => void;
  onUpdate: (
    index: number,
    values: Partial<
      TeamMembershipInput
    >,
  ) => void;
  onPrimary: (index: number) => void;
}) {
  return (
    <Section
      title="Team memberships"
      description="Assign the member to teams. Only one active membership may be primary."
      action={
        <button
          type="button"
          onClick={onAdd}
          className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white"
        >
          <Plus size={16} />
          Add membership
        </button>
      }
    >
      {memberships.length === 0 ? (
        <EmptyEditorState
          title="No team memberships"
          message="Add at least one membership when this person belongs to an operational team."
        />
      ) : (
        <div className="space-y-4">
          {memberships.map(
            (membership, index) => (
              <div
                key={`${membership.team_id}-${index}`}
                className="rounded-xl border border-slate-200 p-4 dark:border-slate-800"
              >
                <div className="grid gap-4 lg:grid-cols-2">
                  <label className="block space-y-1.5">
                    <span className="text-sm font-semibold">
                      Team
                    </span>

                    <select
                      value={
                        membership.team_id
                      }
                      onChange={(event) =>
                        onUpdate(
                          index,
                          {
                            team_id:
                              event.target.value,
                          },
                        )
                      }
                      className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
                    >
                      <option value="">
                        Select team
                      </option>

                      {teams.map(
                        (team) => (
                          <option
                            key={team.id}
                            value={team.id}
                          >
                            {team.name}
                          </option>
                        ),
                      )}
                    </select>
                  </label>

                  <Input
                    label="Role title"
                    value={
                      membership.role_title
                    }
                    onChange={(value) =>
                      onUpdate(
                        index,
                        {
                          role_title:
                            value,
                        },
                      )
                    }
                  />

                  <Input
                    label="Joined date"
                    type="date"
                    value={
                      membership.joined_at
                      ?? ""
                    }
                    onChange={(value) =>
                      onUpdate(
                        index,
                        {
                          joined_at:
                            value || null,
                        },
                      )
                    }
                  />

                  <Input
                    label="Left date"
                    type="date"
                    value={
                      membership.left_at
                      ?? ""
                    }
                    onChange={(value) =>
                      onUpdate(
                        index,
                        {
                          left_at:
                            value || null,
                        },
                      )
                    }
                  />
                </div>

                <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
                  <div className="flex flex-wrap gap-4">
                    <Checkbox
                      label="Active"
                      checked={
                        membership.is_active
                      }
                      onChange={(value) =>
                        onUpdate(
                          index,
                          {
                            is_active:
                              value,
                            is_primary:
                              value
                                ? membership.is_primary
                                : false,
                          },
                        )
                      }
                    />

                    <Checkbox
                      label="Primary team"
                      checked={
                        membership.is_primary
                      }
                      onChange={(value) => {
                        if (value) {
                          onPrimary(index);
                        } else {
                          onUpdate(
                            index,
                            {
                              is_primary:
                                false,
                            },
                          );
                        }
                      }}
                    />
                  </div>

                  <RowActions
                    index={index}
                    total={
                      memberships.length
                    }
                    onMove={onMove}
                    onRemove={onRemove}
                  />
                </div>
              </div>
            ),
          )}
        </div>
      )}
    </Section>
  );
}

function ServicesSection({
  assignments,
  services,
  onAdd,
  onRemove,
  onMove,
  onUpdate,
}: {
  assignments:
    TeamMemberServiceInput[];
  services: ServiceSelectorItem[];
  onAdd: () => void;
  onRemove: (index: number) => void;
  onMove: (
    index: number,
    direction: -1 | 1,
  ) => void;
  onUpdate: (
    index: number,
    values: Partial<
      TeamMemberServiceInput
    >,
  ) => void;
}) {
  return (
    <Section
      title="Service expertise"
      description="Connect the member to services and define their expertise level."
      action={
        <button
          type="button"
          onClick={onAdd}
          className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-3 py-2 text-sm font-semibold text-white"
        >
          <Plus size={16} />
          Add service
        </button>
      }
    >
      {assignments.length === 0 ? (
        <EmptyEditorState
          title="No service expertise"
          message="Add service expertise when this member contributes to a published LKP service."
        />
      ) : (
        <div className="space-y-4">
          {assignments.map(
            (assignment, index) => (
              <div
                key={`${assignment.service_id}-${index}`}
                className="rounded-xl border border-slate-200 p-4 dark:border-slate-800"
              >
                <div className="grid gap-4 lg:grid-cols-3">
                  <label className="block space-y-1.5 lg:col-span-2">
                    <span className="text-sm font-semibold">
                      Service
                    </span>

                    <select
                      value={
                        assignment.service_id
                      }
                      onChange={(event) =>
                        onUpdate(
                          index,
                          {
                            service_id:
                              event.target.value,
                          },
                        )
                      }
                      className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
                    >
                      <option value="">
                        Select service
                      </option>

                      {services.map(
                        (service) => (
                          <option
                            key={service.id}
                            value={service.id}
                          >
                            {service.title}
                          </option>
                        ),
                      )}
                    </select>
                  </label>

                  <Select
                    label="Expertise level"
                    value={
                      assignment.expertise_level
                    }
                    options={
                      expertiseLevels.map(
                        (value) => ({
                          value,
                          label:
                            value
                              .replaceAll(
                                "_",
                                " ",
                              )
                              .replace(
                                /^./,
                                (character) =>
                                  character
                                    .toUpperCase(),
                              ),
                        }),
                      )
                    }
                    onChange={(value) =>
                      onUpdate(
                        index,
                        {
                          expertise_level:
                            value as ExpertiseLevel,
                        },
                      )
                    }
                  />

                  <Input
                    label="Years of experience"
                    type="number"
                    min="0"
                    step="0.5"
                    value={
                      assignment
                        .years_of_experience
                      === null
                        ? ""
                        : String(
                            assignment
                              .years_of_experience,
                          )
                    }
                    onChange={(value) =>
                      onUpdate(
                        index,
                        {
                          years_of_experience:
                            value
                              ? Number(
                                  value,
                                )
                              : null,
                        },
                      )
                    }
                  />
                </div>

                <div className="mt-4 flex flex-wrap items-center justify-between gap-3">
                  <div className="flex flex-wrap gap-4">
                    <Checkbox
                      label="Primary expertise"
                      checked={
                        assignment.is_primary
                      }
                      onChange={(value) =>
                        onUpdate(
                          index,
                          {
                            is_primary:
                              value,
                          },
                        )
                      }
                    />

                    <Checkbox
                      label="Show publicly"
                      checked={
                        assignment.is_public
                      }
                      onChange={(value) =>
                        onUpdate(
                          index,
                          {
                            is_public:
                              value,
                          },
                        )
                      }
                    />
                  </div>

                  <RowActions
                    index={index}
                    total={
                      assignments.length
                    }
                    onMove={onMove}
                    onRemove={onRemove}
                  />
                </div>
              </div>
            ),
          )}
        </div>
      )}
    </Section>
  );
}

function AdvancedSection({
  form,
  onUpdate,
}: {
  form: BasicState;
  onUpdate: <
    Key extends keyof BasicState,
  >(
    key: Key,
    value: BasicState[Key],
  ) => void;
}) {
  return (
    <Section
      title="Advanced"
      description="Metadata and backend-contract information."
    >
      <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm leading-6 text-amber-800 dark:border-amber-900 dark:bg-amber-950/30 dark:text-amber-300">
        Linked dashboard accounts are intentionally disabled.
        The Users API uses integer IDs, while the Team
        Management member contract currently declares a UUID.
        This editor therefore sends <code>user_id: null</code>.
      </div>

      <div className="mt-5">
        <Textarea
          label="Metadata JSON"
          value={form.metadata}
          rows={14}
          monospace
          onChange={(value) =>
            onUpdate(
              "metadata",
              value,
            )
          }
        />
      </div>
    </Section>
  );
}

function Section({
  title,
  description,
  action,
  children,
}: {
  title: string;
  description: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <section>
      <div className="flex flex-col gap-3 border-b border-slate-200 pb-4 sm:flex-row sm:items-start sm:justify-between dark:border-slate-800">
        <div>
          <h3 className="text-lg font-bold">
            {title}
          </h3>
          <p className="mt-1 max-w-3xl text-sm leading-6 text-slate-500">
            {description}
          </p>
        </div>

        {action}
      </div>

      <div className="mt-5">
        {children}
      </div>
    </section>
  );
}

function Input({
  label,
  value,
  onChange,
  type = "text",
  required = false,
  min,
  step,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  type?: string;
  required?: boolean;
  min?: string;
  step?: string;
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
        min={min}
        step={step}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
      />
    </label>
  );
}

function Select({
  label,
  value,
  options,
  onChange,
}: {
  label: string;
  value: string;
  options: {
    value: string;
    label: string;
  }[];
  onChange: (value: string) => void;
}) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm font-semibold">
        {label}
      </span>

      <select
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
      >
        {options.map((option) => (
          <option
            key={option.value}
            value={option.value}
          >
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}

function Textarea({
  label,
  value,
  onChange,
  rows,
  monospace = false,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  rows: number;
  monospace?: boolean;
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
        className={`w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm leading-6 dark:border-slate-700 dark:bg-slate-950 ${
          monospace
            ? "font-mono"
            : ""
        }`}
      />
    </label>
  );
}

function Checkbox({
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

function RowActions({
  index,
  total,
  onMove,
  onRemove,
}: {
  index: number;
  total: number;
  onMove: (
    index: number,
    direction: -1 | 1,
  ) => void;
  onRemove: (index: number) => void;
}) {
  return (
    <div className="flex gap-2">
      <button
        type="button"
        disabled={index === 0}
        onClick={() =>
          onMove(index, -1)
        }
        aria-label="Move up"
        className="rounded-lg border border-slate-200 p-2 disabled:opacity-30 dark:border-slate-700"
      >
        <ChevronUp size={16} />
      </button>

      <button
        type="button"
        disabled={
          index === total - 1
        }
        onClick={() =>
          onMove(index, 1)
        }
        aria-label="Move down"
        className="rounded-lg border border-slate-200 p-2 disabled:opacity-30 dark:border-slate-700"
      >
        <ChevronDown size={16} />
      </button>

      <button
        type="button"
        onClick={() =>
          onRemove(index)
        }
        aria-label="Remove item"
        className="rounded-lg border border-red-200 p-2 text-red-600 dark:border-red-900"
      >
        <Trash2 size={16} />
      </button>
    </div>
  );
}

function EmptyEditorState({
  title,
  message,
}: {
  title: string;
  message: string;
}) {
  return (
    <div className="rounded-xl border border-dashed border-slate-300 px-5 py-12 text-center dark:border-slate-700">
      <h4 className="font-semibold">
        {title}
      </h4>

      <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-slate-500">
        {message}
      </p>
    </div>
  );
}
