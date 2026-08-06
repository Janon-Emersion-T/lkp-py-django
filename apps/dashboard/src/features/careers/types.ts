export const jobListingStatuses = [
  "draft",
  "review",
  "scheduled",
  "published",
  "closed",
  "archived",
] as const;

export type JobListingStatus = (typeof jobListingStatuses)[number];

export const applicationStatuses = [
  "new",
  "screening",
  "shortlisted",
  "interview",
  "assessment",
  "offered",
  "hired",
  "rejected",
  "withdrawn",
  "archived",
] as const;

export type ApplicationStatus = (typeof applicationStatuses)[number];

export const applicationSources = [
  "careers_page",
  "linkedin",
  "facebook",
  "referral",
  "email",
  "manual",
  "other",
] as const;

export type ApplicationSource = (typeof applicationSources)[number];

export const interviewStatuses = [
  "scheduled",
  "confirmed",
  "completed",
  "cancelled",
  "no_show",
  "rescheduled",
] as const;

export type InterviewStatus = (typeof interviewStatuses)[number];

export const interviewTypes = [
  "phone",
  "video",
  "onsite",
  "technical",
  "hr",
  "final",
] as const;

export type InterviewType = (typeof interviewTypes)[number];

export interface CareersDashboard {
  open_listings: number;
  featured_listings: number;
  total_applications: number;
  new_applications: number;
  screening_applications: number;
  shortlisted_applications: number;
  interview_applications: number;
  offered_applications: number;
  hired_applications: number;
  rejected_applications: number;
  upcoming_interviews: number;
  completed_interviews: number;
  applications_by_status: Record<string, number>;
  applications_by_source: Record<string, number>;
}

export interface JobDepartment {
  id: string;
  name: string;
  slug: string;
  description: string;
  is_active: boolean;
  sort_order: number;
}

export interface EmploymentType {
  id: string;
  name: string;
  code: string;
  description: string;
  is_active: boolean;
  sort_order: number;
}

export interface JobPosition {
  id: string;
  department_id: string;
  department_name: string;
  employment_type_id: string;
  employment_type_name: string;
  title: string;
  slug: string;
  summary: string;
  description: Record<string, unknown>;
  responsibilities: unknown[];
  requirements: unknown[];
  preferred_qualifications: unknown[];
  benefits: unknown[];
  location: string;
  remote_policy: string;
  experience_level: string;
  salary_min: string | null;
  salary_max: string | null;
  salary_currency: string;
  salary_visible: boolean;
  is_active: boolean;
  sort_order: number;
}

export interface JobListing {
  id: string;
  position_id: string;
  position_title: string;
  department_name: string;
  employment_type_name: string;
  reference_code: string;
  status: JobListingStatus;
  number_of_openings: number;
  application_deadline: string | null;
  published_at: string | null;
  scheduled_for: string | null;
  is_featured: boolean;
  is_active: boolean;
  is_publicly_available: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export interface ApplicationAnswer {
  id: string;
  question_id: string;
  question: string;
  answer: unknown;
}

export interface ApplicationNote {
  id: string;
  author_id: string | null;
  author_name: string | null;
  note: string;
  is_private: boolean;
  created_at: string;
}

export interface JobApplication {
  id: string;
  listing_id: string;
  listing_reference_code: string;
  position_title: string;
  applicant_name: string;
  email: string;
  phone: string;
  country: string;
  city: string;
  linkedin_url: string;
  portfolio_url: string;
  current_company: string;
  current_position: string;
  years_of_experience: string | null;
  expected_salary: string | null;
  expected_salary_currency: string;
  availability_date: string | null;
  cover_letter: string;
  resume_asset_id: string | null;
  status: ApplicationStatus;
  source: ApplicationSource;
  assigned_to_id: string | null;
  assigned_to_name: string | null;
  submitted_at: string;
  reviewed_at: string | null;
  rating: number | null;
  internal_summary: string;
  rejection_reason: string;
  consent_to_process: boolean;
  consent_to_retain: boolean;
  answers: ApplicationAnswer[];
  notes: ApplicationNote[];
  created_at: string;
  updated_at: string;
}

export interface InterviewParticipant {
  id: string;
  user_id: string;
  user_name: string;
  is_lead: boolean;
  attendance_confirmed: boolean;
}

export interface Interview {
  id: string;
  application_id: string;
  applicant_name: string;
  position_title: string;
  title: string;
  interview_type: InterviewType;
  status: InterviewStatus;
  scheduled_start: string;
  scheduled_end: string;
  timezone_name: string;
  location: string;
  meeting_url: string;
  instructions: string;
  organizer_id: string | null;
  organizer_name: string | null;
  completed_at: string | null;
  cancellation_reason: string;
  participants: InterviewParticipant[];
  created_at: string;
  updated_at: string;
}

export interface ListingFilters {
  search: string;
  status: JobListingStatus | "";
  departmentId: string;
  employmentTypeId: string;
  featuredState: "all" | "featured" | "standard";
  activeState: "all" | "active" | "inactive";
  ordering: string;
}

export interface ApplicationFilters {
  search: string;
  listingId: string;
  status: ApplicationStatus | "";
  source: ApplicationSource | "";
  assignedToId: string;
  ordering: string;
}

export interface InterviewFilters {
  applicationId: string;
  status: InterviewStatus | "";
  interviewType: InterviewType | "";
  organizerId: string;
  ordering: string;
}

export interface ApplicationReviewPayload {
  assigned_to_id: string | null;
  rating: number | null;
  internal_summary: string;
}

export interface ApplicationStatusPayload {
  status: ApplicationStatus;
  rejection_reason: string;
}

export interface ApplicationNotePayload {
  note: string;
  is_private: boolean;
}

export interface ListingSchedulePayload {
  scheduled_for: string;
}
