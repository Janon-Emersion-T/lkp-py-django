import { z } from "zod";

import {
  applicationSources,
  applicationStatuses,
  interviewStatuses,
  interviewTypes,
  jobListingStatuses,
} from "./types";

const nullableDecimalSchema = z
  .union([z.string(), z.number()])
  .nullable()
  .transform((value) => (value === null ? null : String(value)));

export const careersDashboardSchema = z.object({
  open_listings: z.number(),
  featured_listings: z.number(),
  total_applications: z.number(),
  new_applications: z.number(),
  screening_applications: z.number(),
  shortlisted_applications: z.number(),
  interview_applications: z.number(),
  offered_applications: z.number(),
  hired_applications: z.number(),
  rejected_applications: z.number(),
  upcoming_interviews: z.number(),
  completed_interviews: z.number(),
  applications_by_status: z.record(z.string(), z.number()),
  applications_by_source: z.record(z.string(), z.number()),
});

export const jobDepartmentSchema = z.object({
  id: z.string(),
  name: z.string(),
  slug: z.string(),
  description: z.string(),
  is_active: z.boolean(),
  sort_order: z.number(),
});

export const employmentTypeSchema = z.object({
  id: z.string(),
  name: z.string(),
  code: z.string(),
  description: z.string(),
  is_active: z.boolean(),
  sort_order: z.number(),
});

export const jobPositionSchema = z.object({
  id: z.string(),
  department_id: z.string(),
  department_name: z.string(),
  employment_type_id: z.string(),
  employment_type_name: z.string(),
  title: z.string(),
  slug: z.string(),
  summary: z.string(),
  description: z.record(z.string(), z.unknown()),
  responsibilities: z.array(z.unknown()),
  requirements: z.array(z.unknown()),
  preferred_qualifications: z.array(z.unknown()),
  benefits: z.array(z.unknown()),
  location: z.string(),
  remote_policy: z.string(),
  experience_level: z.string(),
  salary_min: nullableDecimalSchema,
  salary_max: nullableDecimalSchema,
  salary_currency: z.string(),
  salary_visible: z.boolean(),
  is_active: z.boolean(),
  sort_order: z.number(),
});

export const jobListingSchema = z.object({
  id: z.string(),
  position_id: z.string(),
  position_title: z.string(),
  department_name: z.string(),
  employment_type_name: z.string(),
  reference_code: z.string(),
  status: z.enum(jobListingStatuses),
  number_of_openings: z.number(),
  application_deadline: z.string().nullable(),
  published_at: z.string().nullable(),
  scheduled_for: z.string().nullable(),
  is_featured: z.boolean(),
  is_active: z.boolean(),
  is_publicly_available: z.boolean(),
  sort_order: z.number(),
  created_at: z.string(),
  updated_at: z.string(),
});

const applicationAnswerSchema = z.object({
  id: z.string(),
  question_id: z.string(),
  question: z.string(),
  answer: z.unknown(),
});

export const applicationNoteSchema = z.object({
  id: z.string(),
  author_id: z.string().nullable(),
  author_name: z.string().nullable(),
  note: z.string(),
  is_private: z.boolean(),
  created_at: z.string(),
});

export const jobApplicationSchema = z.object({
  id: z.string(),
  listing_id: z.string(),
  listing_reference_code: z.string(),
  position_title: z.string(),
  applicant_name: z.string(),
  email: z.string(),
  phone: z.string(),
  country: z.string(),
  city: z.string(),
  linkedin_url: z.string(),
  portfolio_url: z.string(),
  current_company: z.string(),
  current_position: z.string(),
  years_of_experience: nullableDecimalSchema,
  expected_salary: nullableDecimalSchema,
  expected_salary_currency: z.string(),
  availability_date: z.string().nullable(),
  cover_letter: z.string(),
  resume_asset_id: z.string().nullable(),
  status: z.enum(applicationStatuses),
  source: z.enum(applicationSources),
  assigned_to_id: z.string().nullable(),
  assigned_to_name: z.string().nullable(),
  submitted_at: z.string(),
  reviewed_at: z.string().nullable(),
  rating: z.number().nullable(),
  internal_summary: z.string(),
  rejection_reason: z.string(),
  consent_to_process: z.boolean(),
  consent_to_retain: z.boolean(),
  answers: z.array(applicationAnswerSchema),
  notes: z.array(applicationNoteSchema),
  created_at: z.string(),
  updated_at: z.string(),
});

const interviewParticipantSchema = z.object({
  id: z.string(),
  user_id: z.string(),
  user_name: z.string(),
  is_lead: z.boolean(),
  attendance_confirmed: z.boolean(),
});

export const interviewSchema = z.object({
  id: z.string(),
  application_id: z.string(),
  applicant_name: z.string(),
  position_title: z.string(),
  title: z.string(),
  interview_type: z.enum(interviewTypes),
  status: z.enum(interviewStatuses),
  scheduled_start: z.string(),
  scheduled_end: z.string(),
  timezone_name: z.string(),
  location: z.string(),
  meeting_url: z.string(),
  instructions: z.string(),
  organizer_id: z.string().nullable(),
  organizer_name: z.string().nullable(),
  completed_at: z.string().nullable(),
  cancellation_reason: z.string(),
  participants: z.array(interviewParticipantSchema),
  created_at: z.string(),
  updated_at: z.string(),
});
