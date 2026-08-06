import {
  CalendarClock,
  CheckCircle2,
  CircleX,
  Eye,
  FilterX,
  FolderKanban,
  LoaderCircle,
  Mail,
  MailCheck,
  MailPlus,
  MousePointerClick,
  Search,
  Send,
  Tags,
  UserCheck,
  UserPlus,
  Users,
  X,
} from "lucide-react";
import { useMemo, useState, type ReactNode } from "react";

import {
  campaignStatusLabels,
  formatDateTime,
  formatRate,
  statusClasses,
  subscriberSourceLabels,
  subscriberStatusLabels,
} from "../formatters";
import {
  useCampaign,
  useCampaignRecipients,
  useCampaigns,
  useConfirmSubscriber,
  useCreateCampaign,
  useCreateNewsletterList,
  useCreateNewsletterTag,
  useCreateSubscriber,
  useMarkCampaignSent,
  useNewsletterDashboard,
  useNewsletterLists,
  useNewsletterTags,
  usePrepareCampaign,
  useResubscribeSubscriber,
  useScheduleCampaign,
  useSubscriber,
  useSubscribers,
  useUnsubscribeSubscriber,
} from "../hooks";
import {
  campaignStatuses,
  subscriberSources,
  subscriberStatuses,
  type CampaignFilters,
  type CampaignPayload,
  type CampaignRecipient,
  type NewsletterCampaign,
  type NewsletterListPayload,
  type NewsletterTagPayload,
  type Subscriber,
  type SubscriberFilters,
  type SubscriberPayload,
} from "../types";

type NewsletterTab = "overview" | "subscribers" | "segments" | "campaigns";

type Dialog = "subscriber" | "list" | "tag" | "campaign" | "schedule" | null;

const defaultSubscriberFilters: SubscriberFilters = {
  search: "",
  status: "",
  source: "",
  country: "",
  language: "",
  listId: "",
  tagId: "",
  ordering: "-subscribed_at",
};

const defaultCampaignFilters: CampaignFilters = {
  search: "",
  status: "",
  ordering: "-created_at",
};

const emptySubscriber: SubscriberPayload = {
  email: "",
  first_name: "",
  last_name: "",
  company_name: "",
  phone: "",
  country: "",
  language: "en",
  status: "pending",
  source: "manual",
  source_reference: "",
  consent_given: false,
  consent_ip_address: null,
  consent_user_agent: "",
  metadata: {},
  list_ids: [],
  tag_ids: [],
};

const emptyList: NewsletterListPayload = {
  name: "",
  slug: "",
  description: "",
  is_default: false,
  is_public: false,
  is_active: true,
  sort_order: 0,
};

const emptyTag: NewsletterTagPayload = {
  name: "",
  slug: "",
  description: "",
  color: "",
  is_active: true,
};

const emptyCampaign: CampaignPayload = {
  name: "",
  subject: "",
  preview_text: "",
  from_name: "LKProfessionals",
  from_email: "",
  reply_to_email: "",
  html_content: "",
  text_content: "",
  status: "draft",
  metadata: {},
  list_ids: [],
  tag_ids: [],
};

function errorMessage(error: unknown): string {
  return error instanceof Error
    ? error.message
    : "The operation could not be completed.";
}

export function NewsletterPage() {
  const [tab, setTab] = useState<NewsletterTab>("overview");
  const [subscriberFilters, setSubscriberFilters] = useState(
    defaultSubscriberFilters,
  );
  const [campaignFilters, setCampaignFilters] = useState(
    defaultCampaignFilters,
  );
  const [selectedSubscriberId, setSelectedSubscriberId] = useState("");
  const [selectedCampaignId, setSelectedCampaignId] = useState("");
  const [dialog, setDialog] = useState<Dialog>(null);
  const [notice, setNotice] = useState("");
  const [operationError, setOperationError] = useState("");
  const [subscriberForm, setSubscriberForm] = useState(emptySubscriber);
  const [listForm, setListForm] = useState(emptyList);
  const [tagForm, setTagForm] = useState(emptyTag);
  const [campaignForm, setCampaignForm] = useState(emptyCampaign);
  const [scheduleValue, setScheduleValue] = useState("");

  const dashboardQuery = useNewsletterDashboard();
  const listsQuery = useNewsletterLists();
  const tagsQuery = useNewsletterTags();
  const subscribersQuery = useSubscribers(subscriberFilters);
  const campaignsQuery = useCampaigns(campaignFilters);
  const subscriberQuery = useSubscriber(
    selectedSubscriberId,
    selectedSubscriberId !== "",
  );
  const campaignQuery = useCampaign(
    selectedCampaignId,
    selectedCampaignId !== "",
  );
  const recipientsQuery = useCampaignRecipients(
    selectedCampaignId,
    selectedCampaignId !== "",
  );

  const createSubscriberMutation = useCreateSubscriber();
  const createListMutation = useCreateNewsletterList();
  const createTagMutation = useCreateNewsletterTag();
  const createCampaignMutation = useCreateCampaign();
  const confirmMutation = useConfirmSubscriber();
  const unsubscribeMutation = useUnsubscribeSubscriber();
  const resubscribeMutation = useResubscribeSubscriber();
  const prepareMutation = usePrepareCampaign();
  const markSentMutation = useMarkCampaignSent();
  const scheduleMutation = useScheduleCampaign();

  const isMutating = [
    createSubscriberMutation,
    createListMutation,
    createTagMutation,
    createCampaignMutation,
    confirmMutation,
    unsubscribeMutation,
    resubscribeMutation,
    prepareMutation,
    markSentMutation,
    scheduleMutation,
  ].some((mutation) => mutation.isPending);

  const dashboard = dashboardQuery.data;
  const lists = listsQuery.data ?? [];
  const tags = tagsQuery.data ?? [];
  const subscribers = subscribersQuery.data ?? [];
  const campaigns = campaignsQuery.data ?? [];
  const selectedSubscriber = subscriberQuery.data;
  const selectedCampaign = campaignQuery.data;
  const recipients = recipientsQuery.data ?? [];

  const metrics = useMemo(
    () => [
      {
        label: "Total subscribers",
        value: dashboard?.total_subscribers ?? 0,
        icon: Users,
      },
      {
        label: "Active subscribers",
        value: dashboard?.active_subscribers ?? 0,
        icon: UserCheck,
      },
      {
        label: "Pending confirmation",
        value: dashboard?.pending_subscribers ?? 0,
        icon: Mail,
      },
      {
        label: "Unsubscribed",
        value: dashboard?.unsubscribed_subscribers ?? 0,
        icon: CircleX,
      },
      {
        label: "Campaigns",
        value: dashboard?.total_campaigns ?? 0,
        icon: FolderKanban,
      },
      {
        label: "Emails sent",
        value: dashboard?.total_emails_sent ?? 0,
        icon: Send,
      },
      {
        label: "Delivered",
        value: dashboard?.total_delivered ?? 0,
        icon: MailCheck,
      },
      {
        label: "Clicked",
        value: dashboard?.total_clicked ?? 0,
        icon: MousePointerClick,
      },
    ],
    [dashboard],
  );

  function resetFeedback() {
    setNotice("");
    setOperationError("");
  }

  async function submitSubscriber() {
    if (!subscriberForm.email.trim()) return;

    resetFeedback();

    try {
      await createSubscriberMutation.mutateAsync({
        ...subscriberForm,
        email: subscriberForm.email.trim(),
      });
      setSubscriberForm(emptySubscriber);
      setDialog(null);
      setNotice("Newsletter subscriber created.");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitList() {
    if (!listForm.name.trim() || !listForm.slug.trim()) return;

    resetFeedback();

    try {
      await createListMutation.mutateAsync(listForm);
      setListForm(emptyList);
      setDialog(null);
      setNotice("Newsletter list created.");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitTag() {
    if (!tagForm.name.trim() || !tagForm.slug.trim()) return;

    resetFeedback();

    try {
      await createTagMutation.mutateAsync(tagForm);
      setTagForm(emptyTag);
      setDialog(null);
      setNotice("Newsletter tag created.");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitCampaign() {
    if (
      !campaignForm.name.trim() ||
      !campaignForm.subject.trim() ||
      !campaignForm.from_email.trim()
    ) {
      return;
    }

    resetFeedback();

    try {
      await createCampaignMutation.mutateAsync(campaignForm);
      setCampaignForm(emptyCampaign);
      setDialog(null);
      setNotice("Newsletter campaign created.");
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function performSubscriberAction(
    subscriber: Subscriber,
    action: "confirm" | "unsubscribe" | "resubscribe",
  ) {
    resetFeedback();

    try {
      if (action === "confirm") {
        await confirmMutation.mutateAsync(subscriber.id);
      } else if (action === "unsubscribe") {
        await unsubscribeMutation.mutateAsync(subscriber.id);
      } else {
        await resubscribeMutation.mutateAsync(subscriber.id);
      }

      setNotice(`${subscriber.email} was ${action}d.`);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function performCampaignAction(
    campaign: NewsletterCampaign,
    action: "prepare" | "mark-sent",
  ) {
    resetFeedback();

    try {
      if (action === "prepare") {
        await prepareMutation.mutateAsync(campaign.id);
        setNotice(`${campaign.name} recipients were prepared.`);
      } else {
        await markSentMutation.mutateAsync(campaign.id);
        setNotice(`${campaign.name} was marked as sent.`);
      }
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  async function submitSchedule() {
    if (!selectedCampaign || !scheduleValue) return;

    resetFeedback();

    try {
      await scheduleMutation.mutateAsync({
        campaignId: selectedCampaign.id,
        payload: {
          scheduled_for: new Date(scheduleValue).toISOString(),
        },
      });
      setDialog(null);
      setScheduleValue("");
      setNotice(`${selectedCampaign.name} was scheduled.`);
    } catch (error) {
      setOperationError(errorMessage(error));
    }
  }

  return (
    <div className="space-y-6 pb-10">
      <header className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Audience and campaign operations
          </p>
          <h1 className="mt-2 text-2xl font-bold">Newsletter</h1>
          <p className="mt-2 max-w-4xl text-sm leading-6 text-slate-500">
            Manage subscribers, consent, mailing lists, audience tags,
            campaigns, recipient preparation, schedules, delivery statistics,
            opens and clicks from one operational workspace.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setDialog("subscriber")}
            className="button-secondary"
          >
            <UserPlus size={16} />
            Add subscriber
          </button>
          <button
            type="button"
            onClick={() => setDialog("campaign")}
            className="button-primary"
          >
            <MailPlus size={16} />
            Create campaign
          </button>
        </div>
      </header>

      {(notice || operationError) && (
        <div
          className={
            operationError
              ? "flex items-center justify-between rounded-xl border border-rose-200 bg-rose-50 p-4 text-sm text-rose-700"
              : "flex items-center justify-between rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700"
          }
        >
          <span>{operationError || notice}</span>
          <button
            type="button"
            onClick={() => {
              setNotice("");
              setOperationError("");
            }}
            aria-label="Dismiss"
          >
            <X size={17} />
          </button>
        </div>
      )}

      <nav className="flex flex-wrap gap-2">
        {[
          ["overview", "Overview"],
          ["subscribers", "Subscribers"],
          ["segments", "Lists & Tags"],
          ["campaigns", "Campaigns"],
        ].map(([value, label]) => (
          <button
            key={value}
            type="button"
            onClick={() => setTab(value as NewsletterTab)}
            className={
              tab === value
                ? "rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white"
                : "rounded-lg border border-slate-300 px-4 py-2 text-sm font-semibold hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-900"
            }
          >
            {label}
          </button>
        ))}
      </nav>

      {tab === "overview" && (
        <>
          <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
            {dashboardQuery.isLoading ? (
              <LoaderBlock />
            ) : (
              metrics.map((metric) => <Metric key={metric.label} {...metric} />)
            )}
          </section>

          <section className="grid gap-4 lg:grid-cols-2">
            <BreakdownCard
              title="Subscriber lifecycle"
              values={[
                ["Active", dashboard?.active_subscribers ?? 0],
                ["Pending", dashboard?.pending_subscribers ?? 0],
                ["Unsubscribed", dashboard?.unsubscribed_subscribers ?? 0],
                ["Bounced", dashboard?.bounced_subscribers ?? 0],
              ]}
            />
            <BreakdownCard
              title="Campaign lifecycle"
              values={[
                ["Draft", dashboard?.draft_campaigns ?? 0],
                ["Scheduled", dashboard?.scheduled_campaigns ?? 0],
                ["Sent", dashboard?.sent_campaigns ?? 0],
                ["Opened", dashboard?.total_opened ?? 0],
              ]}
            />
          </section>
        </>
      )}

      {tab === "subscribers" && (
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
          <div className="grid gap-3 border-b border-slate-200 p-5 dark:border-slate-800 md:grid-cols-2 xl:grid-cols-6">
            <SearchInput
              value={subscriberFilters.search}
              placeholder="Search subscribers"
              onChange={(search) =>
                setSubscriberFilters((current) => ({ ...current, search }))
              }
            />

            <select
              value={subscriberFilters.status}
              onChange={(event) =>
                setSubscriberFilters((current) => ({
                  ...current,
                  status: event.target.value as SubscriberFilters["status"],
                }))
              }
              className="field"
            >
              <option value="">All statuses</option>
              {subscriberStatuses.map((status) => (
                <option key={status} value={status}>
                  {subscriberStatusLabels[status]}
                </option>
              ))}
            </select>

            <select
              value={subscriberFilters.source}
              onChange={(event) =>
                setSubscriberFilters((current) => ({
                  ...current,
                  source: event.target.value as SubscriberFilters["source"],
                }))
              }
              className="field"
            >
              <option value="">All sources</option>
              {subscriberSources.map((source) => (
                <option key={source} value={source}>
                  {subscriberSourceLabels[source]}
                </option>
              ))}
            </select>

            <select
              value={subscriberFilters.listId}
              onChange={(event) =>
                setSubscriberFilters((current) => ({
                  ...current,
                  listId: event.target.value,
                }))
              }
              className="field"
            >
              <option value="">All lists</option>
              {lists.map((list) => (
                <option key={list.id} value={list.id}>
                  {list.name}
                </option>
              ))}
            </select>

            <select
              value={subscriberFilters.tagId}
              onChange={(event) =>
                setSubscriberFilters((current) => ({
                  ...current,
                  tagId: event.target.value,
                }))
              }
              className="field"
            >
              <option value="">All tags</option>
              {tags.map((tag) => (
                <option key={tag.id} value={tag.id}>
                  {tag.name}
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={() => setSubscriberFilters(defaultSubscriberFilters)}
              className="button-secondary"
            >
              <FilterX size={16} />
              Reset
            </button>
          </div>

          {subscribersQuery.isLoading ? (
            <LoaderBlock />
          ) : subscribersQuery.isError ? (
            <ErrorBlock error={subscribersQuery.error} />
          ) : subscribers.length === 0 ? (
            <EmptyBlock text="No subscribers match the current filters." />
          ) : (
            <div className="divide-y divide-slate-200 dark:divide-slate-800">
              {subscribers.map((subscriber) => (
                <article
                  key={subscriber.id}
                  className="grid gap-4 p-5 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
                >
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="font-semibold">
                        {subscriber.full_name || subscriber.email}
                      </h2>
                      <StatusBadge
                        status={subscriber.status}
                        label={subscriberStatusLabels[subscriber.status]}
                      />
                      {subscriber.can_receive_email && (
                        <span className="rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-700">
                          Receivable
                        </span>
                      )}
                    </div>
                    <p className="mt-1 text-sm text-slate-500">
                      {subscriber.email} ·{" "}
                      {subscriber.company_name || "No company"}
                    </p>
                    <p className="mt-3 text-xs text-slate-500">
                      {subscriberSourceLabels[subscriber.source]} · Subscribed{" "}
                      {formatDateTime(subscriber.subscribed_at)}
                    </p>
                  </div>

                  <div className="space-y-2 text-sm text-slate-500">
                    <p>{subscriber.country || "No country"}</p>
                    <p>{subscriber.language || "No language"}</p>
                    <p>
                      {subscriber.lists.length} list(s) ·{" "}
                      {subscriber.tags.length} tag(s)
                    </p>
                  </div>

                  <button
                    type="button"
                    onClick={() => setSelectedSubscriberId(subscriber.id)}
                    className="button-secondary self-start"
                  >
                    <Eye size={16} />
                    Inspect
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>
      )}

      {tab === "segments" && (
        <section className="grid gap-6 xl:grid-cols-2">
          <SegmentCard
            title="Newsletter Lists"
            icon={FolderKanban}
            actionLabel="Create list"
            onAction={() => setDialog("list")}
          >
            {lists.map((list) => (
              <div
                key={list.id}
                className="rounded-xl border border-slate-200 p-4 dark:border-slate-800"
              >
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="font-semibold">{list.name}</p>
                    <p className="mt-1 text-xs text-slate-500">{list.slug}</p>
                  </div>
                  <span className="text-2xl font-bold">
                    {list.subscriber_count}
                  </span>
                </div>
                <p className="mt-3 text-sm text-slate-500">
                  {list.description || "No description."}
                </p>
                <div className="mt-3 flex flex-wrap gap-2 text-xs">
                  {list.is_default && <Chip text="Default" />}
                  {list.is_public && <Chip text="Public" />}
                  <Chip text={list.is_active ? "Active" : "Inactive"} />
                </div>
              </div>
            ))}
          </SegmentCard>

          <SegmentCard
            title="Newsletter Tags"
            icon={Tags}
            actionLabel="Create tag"
            onAction={() => setDialog("tag")}
          >
            {tags.map((tag) => (
              <div
                key={tag.id}
                className="rounded-xl border border-slate-200 p-4 dark:border-slate-800"
              >
                <div className="flex items-center justify-between gap-3">
                  <div>
                    <p className="font-semibold">{tag.name}</p>
                    <p className="mt-1 text-xs text-slate-500">{tag.slug}</p>
                  </div>
                  <span className="text-2xl font-bold">
                    {tag.subscriber_count}
                  </span>
                </div>
                <p className="mt-3 text-sm text-slate-500">
                  {tag.description || "No description."}
                </p>
                <div className="mt-3 flex flex-wrap gap-2 text-xs">
                  {tag.color && <Chip text={tag.color} />}
                  <Chip text={tag.is_active ? "Active" : "Inactive"} />
                </div>
              </div>
            ))}
          </SegmentCard>
        </section>
      )}

      {tab === "campaigns" && (
        <section className="overflow-hidden rounded-2xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
          <div className="grid gap-3 border-b border-slate-200 p-5 dark:border-slate-800 md:grid-cols-3">
            <SearchInput
              value={campaignFilters.search}
              placeholder="Search campaigns"
              onChange={(search) =>
                setCampaignFilters((current) => ({ ...current, search }))
              }
            />

            <select
              value={campaignFilters.status}
              onChange={(event) =>
                setCampaignFilters((current) => ({
                  ...current,
                  status: event.target.value as CampaignFilters["status"],
                }))
              }
              className="field"
            >
              <option value="">All statuses</option>
              {campaignStatuses.map((status) => (
                <option key={status} value={status}>
                  {campaignStatusLabels[status]}
                </option>
              ))}
            </select>

            <button
              type="button"
              onClick={() => setCampaignFilters(defaultCampaignFilters)}
              className="button-secondary"
            >
              <FilterX size={16} />
              Reset
            </button>
          </div>

          {campaignsQuery.isLoading ? (
            <LoaderBlock />
          ) : campaignsQuery.isError ? (
            <ErrorBlock error={campaignsQuery.error} />
          ) : campaigns.length === 0 ? (
            <EmptyBlock text="No campaigns match the current filters." />
          ) : (
            <div className="divide-y divide-slate-200 dark:divide-slate-800">
              {campaigns.map((campaign) => (
                <article
                  key={campaign.id}
                  className="grid gap-4 p-5 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)_auto]"
                >
                  <div>
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="font-semibold">{campaign.name}</h2>
                      <StatusBadge
                        status={campaign.status}
                        label={campaignStatusLabels[campaign.status]}
                      />
                    </div>
                    <p className="mt-1 text-sm text-slate-500">
                      {campaign.subject}
                    </p>
                    <p className="mt-3 text-xs text-slate-500">
                      {campaign.recipient_count} recipients ·{" "}
                      {campaign.sent_count} sent · {campaign.delivered_count}{" "}
                      delivered
                    </p>
                  </div>

                  <div className="space-y-2 text-sm text-slate-500">
                    <p>Open rate: {formatRate(campaign.open_rate)}</p>
                    <p>Click rate: {formatRate(campaign.click_rate)}</p>
                    <p>Scheduled: {formatDateTime(campaign.scheduled_for)}</p>
                  </div>

                  <button
                    type="button"
                    onClick={() => setSelectedCampaignId(campaign.id)}
                    className="button-secondary self-start"
                  >
                    <Eye size={16} />
                    Inspect
                  </button>
                </article>
              ))}
            </div>
          )}
        </section>
      )}

      {selectedSubscriberId && (
        <SidePanel
          title="Subscriber details"
          onClose={() => setSelectedSubscriberId("")}
        >
          {subscriberQuery.isLoading ? (
            <LoaderBlock />
          ) : selectedSubscriber ? (
            <SubscriberDetail
              subscriber={selectedSubscriber}
              pending={isMutating}
              onAction={(action) =>
                void performSubscriberAction(selectedSubscriber, action)
              }
            />
          ) : (
            <ErrorBlock error={subscriberQuery.error} />
          )}
        </SidePanel>
      )}

      {selectedCampaignId && (
        <SidePanel
          title="Campaign details"
          onClose={() => setSelectedCampaignId("")}
        >
          {campaignQuery.isLoading ? (
            <LoaderBlock />
          ) : selectedCampaign ? (
            <CampaignDetail
              campaign={selectedCampaign}
              recipients={recipients}
              recipientsLoading={recipientsQuery.isLoading}
              pending={isMutating}
              onPrepare={() =>
                void performCampaignAction(selectedCampaign, "prepare")
              }
              onMarkSent={() =>
                void performCampaignAction(selectedCampaign, "mark-sent")
              }
              onSchedule={() => setDialog("schedule")}
            />
          ) : (
            <ErrorBlock error={campaignQuery.error} />
          )}
        </SidePanel>
      )}

      {dialog === "subscriber" && (
        <Modal title="Create subscriber" onClose={() => setDialog(null)}>
          <SubscriberForm
            value={subscriberForm}
            lists={lists}
            tags={tags}
            onChange={setSubscriberForm}
          />
          <DialogActions
            pending={isMutating}
            disabled={!subscriberForm.email.trim()}
            submitLabel="Create subscriber"
            onCancel={() => setDialog(null)}
            onSubmit={() => void submitSubscriber()}
          />
        </Modal>
      )}

      {dialog === "list" && (
        <Modal title="Create newsletter list" onClose={() => setDialog(null)}>
          <TextField
            label="Name"
            value={listForm.name}
            onChange={(name) =>
              setListForm((current) => ({
                ...current,
                name,
                slug: current.slug || slugify(name),
              }))
            }
          />
          <TextField
            label="Slug"
            value={listForm.slug}
            onChange={(slug) =>
              setListForm((current) => ({ ...current, slug }))
            }
          />
          <TextArea
            label="Description"
            value={listForm.description}
            onChange={(description) =>
              setListForm((current) => ({ ...current, description }))
            }
          />
          <Checkbox
            label="Public list"
            checked={listForm.is_public}
            onChange={(is_public) =>
              setListForm((current) => ({ ...current, is_public }))
            }
          />
          <Checkbox
            label="Default list"
            checked={listForm.is_default}
            onChange={(is_default) =>
              setListForm((current) => ({ ...current, is_default }))
            }
          />
          <DialogActions
            pending={isMutating}
            disabled={!listForm.name.trim() || !listForm.slug.trim()}
            submitLabel="Create list"
            onCancel={() => setDialog(null)}
            onSubmit={() => void submitList()}
          />
        </Modal>
      )}

      {dialog === "tag" && (
        <Modal title="Create newsletter tag" onClose={() => setDialog(null)}>
          <TextField
            label="Name"
            value={tagForm.name}
            onChange={(name) =>
              setTagForm((current) => ({
                ...current,
                name,
                slug: current.slug || slugify(name),
              }))
            }
          />
          <TextField
            label="Slug"
            value={tagForm.slug}
            onChange={(slug) => setTagForm((current) => ({ ...current, slug }))}
          />
          <TextField
            label="Colour"
            value={tagForm.color}
            placeholder="#2563eb"
            onChange={(color) =>
              setTagForm((current) => ({ ...current, color }))
            }
          />
          <TextArea
            label="Description"
            value={tagForm.description}
            onChange={(description) =>
              setTagForm((current) => ({ ...current, description }))
            }
          />
          <DialogActions
            pending={isMutating}
            disabled={!tagForm.name.trim() || !tagForm.slug.trim()}
            submitLabel="Create tag"
            onCancel={() => setDialog(null)}
            onSubmit={() => void submitTag()}
          />
        </Modal>
      )}

      {dialog === "campaign" && (
        <Modal
          title="Create newsletter campaign"
          onClose={() => setDialog(null)}
        >
          <TextField
            label="Campaign name"
            value={campaignForm.name}
            onChange={(name) =>
              setCampaignForm((current) => ({ ...current, name }))
            }
          />
          <TextField
            label="Subject"
            value={campaignForm.subject}
            onChange={(subject) =>
              setCampaignForm((current) => ({ ...current, subject }))
            }
          />
          <TextField
            label="Preview text"
            value={campaignForm.preview_text}
            onChange={(preview_text) =>
              setCampaignForm((current) => ({ ...current, preview_text }))
            }
          />
          <div className="grid gap-4 sm:grid-cols-2">
            <TextField
              label="From name"
              value={campaignForm.from_name}
              onChange={(from_name) =>
                setCampaignForm((current) => ({ ...current, from_name }))
              }
            />
            <TextField
              label="From email"
              value={campaignForm.from_email}
              type="email"
              onChange={(from_email) =>
                setCampaignForm((current) => ({ ...current, from_email }))
              }
            />
          </div>
          <TextField
            label="Reply-to email"
            value={campaignForm.reply_to_email}
            type="email"
            onChange={(reply_to_email) =>
              setCampaignForm((current) => ({ ...current, reply_to_email }))
            }
          />
          <TextArea
            label="HTML content"
            value={campaignForm.html_content}
            rows={7}
            onChange={(html_content) =>
              setCampaignForm((current) => ({ ...current, html_content }))
            }
          />
          <TextArea
            label="Plain-text content"
            value={campaignForm.text_content}
            rows={5}
            onChange={(text_content) =>
              setCampaignForm((current) => ({ ...current, text_content }))
            }
          />
          <MultiSelect
            label="Newsletter lists"
            options={lists.map((item) => ({
              value: item.id,
              label: item.name,
            }))}
            selected={campaignForm.list_ids}
            onChange={(list_ids) =>
              setCampaignForm((current) => ({ ...current, list_ids }))
            }
          />
          <MultiSelect
            label="Newsletter tags"
            options={tags.map((item) => ({
              value: item.id,
              label: item.name,
            }))}
            selected={campaignForm.tag_ids}
            onChange={(tag_ids) =>
              setCampaignForm((current) => ({ ...current, tag_ids }))
            }
          />
          <DialogActions
            pending={isMutating}
            disabled={
              !campaignForm.name.trim() ||
              !campaignForm.subject.trim() ||
              !campaignForm.from_email.trim()
            }
            submitLabel="Create campaign"
            onCancel={() => setDialog(null)}
            onSubmit={() => void submitCampaign()}
          />
        </Modal>
      )}

      {dialog === "schedule" && selectedCampaign && (
        <Modal title="Schedule campaign" onClose={() => setDialog(null)}>
          <TextField
            label="Scheduled date and time"
            value={scheduleValue}
            type="datetime-local"
            onChange={setScheduleValue}
          />
          <DialogActions
            pending={isMutating}
            disabled={!scheduleValue}
            submitLabel="Schedule campaign"
            onCancel={() => setDialog(null)}
            onSubmit={() => void submitSchedule()}
          />
        </Modal>
      )}
    </div>
  );
}

function SubscriberDetail({
  subscriber,
  pending,
  onAction,
}: {
  subscriber: Subscriber;
  pending: boolean;
  onAction: (action: "confirm" | "unsubscribe" | "resubscribe") => void;
}) {
  return (
    <div className="space-y-6 p-6">
      <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
        <Detail label="Name" value={subscriber.full_name || "Not supplied"} />
        <Detail label="Email" value={subscriber.email} />
        <Detail
          label="Company"
          value={subscriber.company_name || "Not supplied"}
        />
        <Detail label="Phone" value={subscriber.phone || "Not supplied"} />
        <Detail label="Country" value={subscriber.country || "Not supplied"} />
        <Detail label="Language" value={subscriber.language} />
        <Detail
          label="Status"
          value={subscriberStatusLabels[subscriber.status]}
        />
        <Detail
          label="Source"
          value={subscriberSourceLabels[subscriber.source]}
        />
        <Detail
          label="Subscribed"
          value={formatDateTime(subscriber.subscribed_at)}
        />
        <Detail
          label="Confirmed"
          value={formatDateTime(subscriber.confirmed_at)}
        />
        <Detail
          label="Unsubscribed"
          value={formatDateTime(subscriber.unsubscribed_at)}
        />
        <Detail
          label="Can receive email"
          value={subscriber.can_receive_email ? "Yes" : "No"}
        />
      </section>

      <section>
        <h3 className="font-semibold">Lists</h3>
        <div className="mt-3 flex flex-wrap gap-2">
          {subscriber.lists.length ? (
            subscriber.lists.map((list) => (
              <Chip key={list.id} text={list.name} />
            ))
          ) : (
            <EmptyBlock text="No newsletter lists assigned." />
          )}
        </div>
      </section>

      <section>
        <h3 className="font-semibold">Tags</h3>
        <div className="mt-3 flex flex-wrap gap-2">
          {subscriber.tags.length ? (
            subscriber.tags.map((tag) => <Chip key={tag.id} text={tag.name} />)
          ) : (
            <EmptyBlock text="No newsletter tags assigned." />
          )}
        </div>
      </section>

      <section className="flex flex-wrap gap-2 border-t border-slate-200 pt-6 dark:border-slate-800">
        {subscriber.status === "pending" && (
          <button
            type="button"
            disabled={pending}
            onClick={() => onAction("confirm")}
            className="button-primary"
          >
            <CheckCircle2 size={16} />
            Confirm
          </button>
        )}

        {subscriber.status === "unsubscribed" ? (
          <button
            type="button"
            disabled={pending}
            onClick={() => onAction("resubscribe")}
            className="button-primary"
          >
            <MailCheck size={16} />
            Resubscribe
          </button>
        ) : (
          <button
            type="button"
            disabled={pending}
            onClick={() => onAction("unsubscribe")}
            className="button-danger"
          >
            <CircleX size={16} />
            Unsubscribe
          </button>
        )}
      </section>
    </div>
  );
}

function CampaignDetail({
  campaign,
  recipients,
  recipientsLoading,
  pending,
  onPrepare,
  onMarkSent,
  onSchedule,
}: {
  campaign: NewsletterCampaign;
  recipients: CampaignRecipient[];
  recipientsLoading: boolean;
  pending: boolean;
  onPrepare: () => void;
  onMarkSent: () => void;
  onSchedule: () => void;
}) {
  return (
    <div className="space-y-6 p-6">
      <section className="grid gap-4 rounded-2xl border border-slate-200 p-5 dark:border-slate-800 sm:grid-cols-2">
        <Detail label="Campaign" value={campaign.name} />
        <Detail label="Status" value={campaignStatusLabels[campaign.status]} />
        <Detail label="Subject" value={campaign.subject} />
        <Detail
          label="From"
          value={`${campaign.from_name} <${campaign.from_email}>`}
        />
        <Detail
          label="Scheduled"
          value={formatDateTime(campaign.scheduled_for)}
        />
        <Detail label="Sent" value={formatDateTime(campaign.sent_at)} />
        <Detail label="Open rate" value={formatRate(campaign.open_rate)} />
        <Detail label="Click rate" value={formatRate(campaign.click_rate)} />
      </section>

      <section className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <SmallMetric label="Recipients" value={campaign.recipient_count} />
        <SmallMetric label="Queued" value={campaign.queued_count} />
        <SmallMetric label="Sent" value={campaign.sent_count} />
        <SmallMetric label="Delivered" value={campaign.delivered_count} />
        <SmallMetric label="Opened" value={campaign.opened_count} />
        <SmallMetric label="Clicked" value={campaign.clicked_count} />
        <SmallMetric label="Bounced" value={campaign.bounced_count} />
        <SmallMetric label="Failed" value={campaign.failed_count} />
      </section>

      <section>
        <h3 className="font-semibold">Target lists</h3>
        <div className="mt-3 flex flex-wrap gap-2">
          {campaign.lists.map((list) => (
            <Chip key={list.id} text={list.name} />
          ))}
        </div>
      </section>

      <section>
        <h3 className="font-semibold">Target tags</h3>
        <div className="mt-3 flex flex-wrap gap-2">
          {campaign.tags.map((tag) => (
            <Chip key={tag.id} text={tag.name} />
          ))}
        </div>
      </section>

      <section>
        <h3 className="font-semibold">Recipient delivery status</h3>
        {recipientsLoading ? (
          <LoaderBlock />
        ) : recipients.length === 0 ? (
          <EmptyBlock text="Recipients have not been prepared." />
        ) : (
          <div className="mt-3 max-h-96 divide-y divide-slate-200 overflow-auto rounded-xl border border-slate-200 dark:divide-slate-800 dark:border-slate-800">
            {recipients.map((recipient) => (
              <div
                key={recipient.id}
                className="grid gap-2 p-3 sm:grid-cols-[minmax(0,1fr)_auto]"
              >
                <div>
                  <p className="text-sm font-semibold">{recipient.email}</p>
                  <p className="mt-1 text-xs text-slate-500">
                    {recipient.first_name} {recipient.last_name}
                  </p>
                </div>
                <StatusBadge
                  status={recipient.status}
                  label={recipient.status}
                />
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="flex flex-wrap gap-2 border-t border-slate-200 pt-6 dark:border-slate-800">
        <button
          type="button"
          disabled={pending}
          onClick={onPrepare}
          className="button-secondary"
        >
          <Users size={16} />
          Prepare recipients
        </button>
        <button
          type="button"
          disabled={pending}
          onClick={onSchedule}
          className="button-secondary"
        >
          <CalendarClock size={16} />
          Schedule
        </button>
        <button
          type="button"
          disabled={pending}
          onClick={onMarkSent}
          className="button-primary"
        >
          <Send size={16} />
          Mark sent
        </button>
      </section>
    </div>
  );
}

function SubscriberForm({
  value,
  lists,
  tags,
  onChange,
}: {
  value: SubscriberPayload;
  lists: { id: string; name: string }[];
  tags: { id: string; name: string }[];
  onChange: (value: SubscriberPayload) => void;
}) {
  return (
    <>
      <TextField
        label="Email"
        value={value.email}
        type="email"
        onChange={(email) => onChange({ ...value, email })}
      />
      <div className="grid gap-4 sm:grid-cols-2">
        <TextField
          label="First name"
          value={value.first_name}
          onChange={(first_name) => onChange({ ...value, first_name })}
        />
        <TextField
          label="Last name"
          value={value.last_name}
          onChange={(last_name) => onChange({ ...value, last_name })}
        />
      </div>
      <TextField
        label="Company"
        value={value.company_name}
        onChange={(company_name) => onChange({ ...value, company_name })}
      />
      <div className="grid gap-4 sm:grid-cols-2">
        <TextField
          label="Country"
          value={value.country}
          onChange={(country) => onChange({ ...value, country })}
        />
        <TextField
          label="Language"
          value={value.language}
          onChange={(language) => onChange({ ...value, language })}
        />
      </div>
      <MultiSelect
        label="Newsletter lists"
        options={lists.map((item) => ({ value: item.id, label: item.name }))}
        selected={value.list_ids}
        onChange={(list_ids) => onChange({ ...value, list_ids })}
      />
      <MultiSelect
        label="Newsletter tags"
        options={tags.map((item) => ({ value: item.id, label: item.name }))}
        selected={value.tag_ids}
        onChange={(tag_ids) => onChange({ ...value, tag_ids })}
      />
      <Checkbox
        label="Consent received"
        checked={value.consent_given}
        onChange={(consent_given) => onChange({ ...value, consent_given })}
      />
    </>
  );
}

function Metric({
  label,
  value,
  icon: Icon,
}: {
  label: string;
  value: number;
  icon: typeof Users;
}) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center justify-between">
        <p className="text-sm font-medium text-slate-500">{label}</p>
        <Icon className="h-5 w-5 text-blue-500" />
      </div>
      <p className="mt-3 text-3xl font-bold">{value}</p>
    </article>
  );
}

function BreakdownCard({
  title,
  values,
}: {
  title: string;
  values: [string, number][];
}) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
      <h2 className="font-semibold">{title}</h2>
      <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
        {values.map(([label, value]) => (
          <SmallMetric key={label} label={label} value={value} />
        ))}
      </div>
    </article>
  );
}

function SmallMetric({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-xl bg-slate-50 p-3 dark:bg-slate-900">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 text-xl font-bold">{value}</p>
    </div>
  );
}

function SegmentCard({
  title,
  icon: Icon,
  actionLabel,
  onAction,
  children,
}: {
  title: string;
  icon: typeof Tags;
  actionLabel: string;
  onAction: () => void;
  children: ReactNode;
}) {
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
      <div className="flex items-center justify-between gap-3">
        <h2 className="flex items-center gap-2 font-semibold">
          <Icon size={18} />
          {title}
        </h2>
        <button type="button" onClick={onAction} className="button-secondary">
          {actionLabel}
        </button>
      </div>
      <div className="mt-5 space-y-3">{children}</div>
    </article>
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
        className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
      />
      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="field pl-9"
      />
    </label>
  );
}

function StatusBadge({ status, label }: { status: string; label: string }) {
  return (
    <span
      className={`inline-flex w-fit rounded-full border px-2 py-0.5 text-xs font-semibold ${statusClasses(status)}`}
    >
      {label}
    </span>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wide text-slate-400">
        {label}
      </p>
      <p className="mt-1 break-words text-sm font-semibold">{value}</p>
    </div>
  );
}

function Chip({ text }: { text: string }) {
  return (
    <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-300">
      {text}
    </span>
  );
}

function SidePanel({
  title,
  onClose,
  children,
}: {
  title: string;
  onClose: () => void;
  children: ReactNode;
}) {
  return (
    <div className="fixed inset-0 z-40 flex justify-end bg-slate-950/50">
      <div className="h-full w-full max-w-3xl overflow-y-auto bg-white shadow-2xl dark:bg-slate-950">
        <header className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-950">
          <h2 className="font-semibold">{title}</h2>
          <button type="button" onClick={onClose} aria-label="Close panel">
            <X size={20} />
          </button>
        </header>
        {children}
      </div>
    </div>
  );
}

function Modal({
  title,
  onClose,
  children,
}: {
  title: string;
  onClose: () => void;
  children: ReactNode;
}) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 p-4">
      <div className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white p-6 shadow-2xl dark:bg-slate-950">
        <header className="mb-5 flex items-center justify-between">
          <h2 className="text-lg font-semibold">{title}</h2>
          <button type="button" onClick={onClose} aria-label="Close dialog">
            <X size={20} />
          </button>
        </header>
        <div className="space-y-4">{children}</div>
      </div>
    </div>
  );
}

function TextField({
  label,
  value,
  type = "text",
  placeholder,
  onChange,
}: {
  label: string;
  value: string;
  type?: string;
  placeholder?: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-semibold">{label}</span>
      <input
        type={type}
        value={value}
        placeholder={placeholder}
        onChange={(event) => onChange(event.target.value)}
        className="field"
      />
    </label>
  );
}

function TextArea({
  label,
  value,
  rows = 4,
  onChange,
}: {
  label: string;
  value: string;
  rows?: number;
  onChange: (value: string) => void;
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-semibold">{label}</span>
      <textarea
        rows={rows}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        className="field min-h-24"
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
  onChange: (checked: boolean) => void;
}) {
  return (
    <label className="flex items-center gap-3 rounded-xl border border-slate-200 p-3 text-sm font-medium dark:border-slate-800">
      <input
        type="checkbox"
        checked={checked}
        onChange={(event) => onChange(event.target.checked)}
      />
      {label}
    </label>
  );
}

function MultiSelect({
  label,
  options,
  selected,
  onChange,
}: {
  label: string;
  options: { value: string; label: string }[];
  selected: string[];
  onChange: (value: string[]) => void;
}) {
  return (
    <fieldset>
      <legend className="mb-2 text-sm font-semibold">{label}</legend>
      <div className="grid gap-2 sm:grid-cols-2">
        {options.map((option) => (
          <label
            key={option.value}
            className="flex items-center gap-2 rounded-lg border border-slate-200 p-2.5 text-sm dark:border-slate-800"
          >
            <input
              type="checkbox"
              checked={selected.includes(option.value)}
              onChange={(event) =>
                onChange(
                  event.target.checked
                    ? [...selected, option.value]
                    : selected.filter((value) => value !== option.value),
                )
              }
            />
            {option.label}
          </label>
        ))}
      </div>
    </fieldset>
  );
}

function DialogActions({
  pending,
  disabled,
  submitLabel,
  onCancel,
  onSubmit,
}: {
  pending: boolean;
  disabled: boolean;
  submitLabel: string;
  onCancel: () => void;
  onSubmit: () => void;
}) {
  return (
    <div className="flex justify-end gap-3 pt-3">
      <button type="button" onClick={onCancel} className="button-secondary">
        Cancel
      </button>
      <button
        type="button"
        disabled={pending || disabled}
        onClick={onSubmit}
        className="button-primary disabled:opacity-50"
      >
        {pending && <LoaderCircle size={16} className="animate-spin" />}
        {submitLabel}
      </button>
    </div>
  );
}

function LoaderBlock() {
  return (
    <div className="flex min-h-48 items-center justify-center gap-2 p-8 text-sm text-slate-500">
      <LoaderCircle className="h-5 w-5 animate-spin" />
      Loading…
    </div>
  );
}

function ErrorBlock({ error }: { error: unknown }) {
  return (
    <div className="p-8 text-center text-sm text-rose-600">
      {errorMessage(error)}
    </div>
  );
}

function EmptyBlock({ text }: { text: string }) {
  return (
    <p className="rounded-xl border border-dashed border-slate-300 p-5 text-center text-sm text-slate-500 dark:border-slate-700">
      {text}
    </p>
  );
}

function slugify(value: string): string {
  return value
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}
