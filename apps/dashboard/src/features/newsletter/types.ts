export const subscriberStatuses = [
  "pending",
  "active",
  "unsubscribed",
  "bounced",
  "complained",
  "suppressed",
] as const;

export type SubscriberStatus = (typeof subscriberStatuses)[number];

export const subscriberSources = [
  "website",
  "manual",
  "import",
  "contact_form",
  "quote_form",
  "careers",
  "client_portal",
  "other",
] as const;

export type SubscriberSource = (typeof subscriberSources)[number];

export const campaignStatuses = [
  "draft",
  "review",
  "scheduled",
  "queued",
  "sending",
  "sent",
  "paused",
  "cancelled",
  "failed",
  "archived",
] as const;

export type CampaignStatus = (typeof campaignStatuses)[number];

export interface NewsletterList {
  id: string;
  name: string;
  slug: string;
  description: string;
  is_default: boolean;
  is_public: boolean;
  is_active: boolean;
  sort_order: number;
  subscriber_count: number;
}

export interface NewsletterTag {
  id: string;
  name: string;
  slug: string;
  description: string;
  color: string;
  is_active: boolean;
  subscriber_count: number;
}

export interface Subscriber {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  full_name: string;
  company_name: string;
  phone: string;
  country: string;
  language: string;
  status: SubscriberStatus;
  source: SubscriberSource;
  source_reference: string;
  consent_given: boolean;
  subscribed_at: string;
  confirmed_at: string | null;
  unsubscribed_at: string | null;
  confirmation_token: string;
  unsubscribe_token: string;
  bounce_count: number;
  last_bounced_at: string | null;
  last_email_sent_at: string | null;
  metadata: Record<string, unknown>;
  can_receive_email: boolean;
  lists: NewsletterList[];
  tags: NewsletterTag[];
  created_at: string;
  updated_at: string;
}

export interface CampaignRecipient {
  id: string;
  subscriber_id: string | null;
  email: string;
  first_name: string;
  last_name: string;
  status: string;
  queued_at: string | null;
  sent_at: string | null;
  delivered_at: string | null;
  opened_at: string | null;
  clicked_at: string | null;
  bounced_at: string | null;
  complained_at: string | null;
  unsubscribed_at: string | null;
  failed_at: string | null;
  failure_reason: string;
  provider_message_id: string;
  open_count: number;
  click_count: number;
}

export interface NewsletterCampaign {
  id: string;
  name: string;
  subject: string;
  preview_text: string;
  from_name: string;
  from_email: string;
  reply_to_email: string;
  html_content: string;
  text_content: string;
  status: CampaignStatus;
  scheduled_for: string | null;
  queued_at: string | null;
  sending_started_at: string | null;
  sent_at: string | null;
  completed_at: string | null;
  failure_reason: string;
  recipient_count: number;
  queued_count: number;
  sent_count: number;
  delivered_count: number;
  opened_count: number;
  clicked_count: number;
  bounced_count: number;
  complained_count: number;
  unsubscribed_count: number;
  failed_count: number;
  open_rate: number;
  click_rate: number;
  metadata: Record<string, unknown>;
  lists: NewsletterList[];
  tags: NewsletterTag[];
  created_at: string;
  updated_at: string;
}

export interface NewsletterDashboard {
  total_subscribers: number;
  active_subscribers: number;
  pending_subscribers: number;
  unsubscribed_subscribers: number;
  bounced_subscribers: number;
  total_campaigns: number;
  draft_campaigns: number;
  scheduled_campaigns: number;
  sent_campaigns: number;
  total_emails_sent: number;
  total_delivered: number;
  total_opened: number;
  total_clicked: number;
}

export interface SubscriberFilters {
  search: string;
  status: SubscriberStatus | "";
  source: SubscriberSource | "";
  country: string;
  language: string;
  listId: string;
  tagId: string;
  ordering: string;
}

export interface CampaignFilters {
  search: string;
  status: CampaignStatus | "";
  ordering: string;
}

export interface SubscriberPayload {
  email: string;
  first_name: string;
  last_name: string;
  company_name: string;
  phone: string;
  country: string;
  language: string;
  status: SubscriberStatus;
  source: SubscriberSource;
  source_reference: string;
  consent_given: boolean;
  consent_ip_address: string | null;
  consent_user_agent: string;
  metadata: Record<string, unknown>;
  list_ids: string[];
  tag_ids: string[];
}

export interface NewsletterListPayload {
  name: string;
  slug: string;
  description: string;
  is_default: boolean;
  is_public: boolean;
  is_active: boolean;
  sort_order: number;
}

export interface NewsletterTagPayload {
  name: string;
  slug: string;
  description: string;
  color: string;
  is_active: boolean;
}

export interface CampaignPayload {
  name: string;
  subject: string;
  preview_text: string;
  from_name: string;
  from_email: string;
  reply_to_email: string;
  html_content: string;
  text_content: string;
  status: CampaignStatus;
  metadata: Record<string, unknown>;
  list_ids: string[];
  tag_ids: string[];
}

export interface CampaignSchedulePayload {
  scheduled_for: string;
}
