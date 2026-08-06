import {
  BadgeCheck,
  Building2,
  CalendarDays,
  ExternalLink,
  Globe2,
  Mail,
  MapPin,
  MessageCircle,
  Phone,
  ReceiptText,
  UserRound,
  X,
} from "lucide-react";

import {
  Button,
} from "../../../components/ui/button";
import {
  formatContactName,
  formatDateTime,
  normalizeExternalUrl,
  whatsappUrl,
} from "../formatters";
import {
  useClient,
} from "../hooks";
import {
  ClientStatusBadge,
  ClientTypeBadge,
} from "./client-badges";

interface ClientDetailPanelProps {
  clientId: string | null;
  onClose: () => void;
}

export function ClientDetailPanel({
  clientId,
  onClose,
}: ClientDetailPanelProps) {
  const clientQuery =
    useClient(clientId);

  const client = clientQuery.data;

  if (!clientId) {
    return null;
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close client details"
        className="fixed inset-0 z-40 bg-slate-950/50 backdrop-blur-sm"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-2xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-900">
        <header className="flex h-16 shrink-0 items-center justify-between border-b border-slate-200 px-5 dark:border-slate-800">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
              Client record
            </p>

            <h2 className="mt-0.5 font-semibold text-slate-950 dark:text-white">
              {client?.company_name
                ?? "Loading client"}
            </h2>
          </div>

          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            aria-label="Close client details"
            className="dark:text-slate-300"
          >
            <X size={19} />
          </Button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {clientQuery.isLoading && (
            <div className="space-y-4">
              {Array.from({
                length: 7,
              }).map((_, index) => (
                <div
                  key={index}
                  className="h-16 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800"
                />
              ))}
            </div>
          )}

          {clientQuery.isError && (
            <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {clientQuery.error
                instanceof Error
                ? clientQuery.error.message
                : "Client details could not be loaded."}
            </div>
          )}

          {client && (
            <div className="space-y-6">
              <section>
                <div className="flex flex-wrap items-center gap-2">
                  <ClientStatusBadge
                    status={client.status}
                  />

                  <ClientTypeBadge
                    clientType={
                      client.client_type
                    }
                  />

                  {client.source_lead_id && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold text-violet-700 dark:bg-violet-950/60 dark:text-violet-300">
                      <BadgeCheck
                        size={13}
                      />
                      Converted lead
                    </span>
                  )}
                </div>

                <h3 className="mt-4 text-2xl font-bold text-slate-950 dark:text-white">
                  {client.company_name}
                </h3>

                <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">
                  {client.client_code}
                </p>

                {client.legal_name && (
                  <p className="mt-2 flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                    <Building2 size={15} />
                    {client.legal_name}
                  </p>
                )}
              </section>

              <section className="grid gap-3 sm:grid-cols-2">
                {client.email && (
                  <a
                    href={`mailto:${client.email}`}
                    className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    <Mail
                      size={17}
                      className="text-slate-400"
                    />
                    <span className="truncate">
                      {client.email}
                    </span>
                  </a>
                )}

                {client.phone && (
                  <a
                    href={`tel:${client.phone}`}
                    className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    <Phone
                      size={17}
                      className="text-slate-400"
                    />
                    <span>
                      {client.phone}
                    </span>
                  </a>
                )}

                {client.whatsapp && (
                  <a
                    href={whatsappUrl(
                      client.whatsapp,
                    )}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    <MessageCircle
                      size={17}
                      className="text-emerald-600"
                    />
                    <span>
                      {client.whatsapp}
                    </span>
                  </a>
                )}

                {client.website && (
                  <a
                    href={normalizeExternalUrl(
                      client.website,
                    )}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-3 rounded-lg border border-slate-200 p-3 text-sm text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
                  >
                    <Globe2
                      size={17}
                      className="text-slate-400"
                    />
                    <span className="truncate">
                      Main website
                    </span>
                    <ExternalLink
                      size={14}
                      className="ml-auto"
                    />
                  </a>
                )}
              </section>

              <section className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
                <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                  Commercial profile
                </h4>

                <dl className="mt-4 space-y-4">
                  <div className="flex items-start justify-between gap-4">
                    <dt className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                      <Building2 size={15} />
                      Industry
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {client.industry
                        || "Not specified"}
                    </dd>
                  </div>

                  <div className="flex items-start justify-between gap-4">
                    <dt className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                      <MapPin size={15} />
                      Country
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {client.country
                        || "Not specified"}
                    </dd>
                  </div>

                  <div className="flex items-start justify-between gap-4">
                    <dt className="flex items-center gap-2 text-sm text-slate-500 dark:text-slate-400">
                      <ReceiptText size={15} />
                      Payment terms
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {
                        client.payment_terms_days
                      }{" "}
                      days
                    </dd>
                  </div>

                  <div className="flex items-start justify-between gap-4">
                    <dt className="text-sm text-slate-500 dark:text-slate-400">
                      Default currency
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {
                        client.default_currency
                      }
                    </dd>
                  </div>

                  <div className="flex items-start justify-between gap-4">
                    <dt className="text-sm text-slate-500 dark:text-slate-400">
                      Timezone
                    </dt>

                    <dd className="text-right text-sm font-medium text-slate-900 dark:text-white">
                      {client.timezone}
                    </dd>
                  </div>
                </dl>
              </section>

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Contacts
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {client.contacts.length}
                  </span>
                </div>

                {client.contacts.length ===
                0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No contacts recorded
                  </p>
                ) : (
                  <div className="mt-3 space-y-3">
                    {client.contacts.map(
                      (contact) => (
                        <article
                          key={contact.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div className="min-w-0">
                              <p className="flex items-center gap-2 font-medium text-slate-950 dark:text-white">
                                <UserRound
                                  size={15}
                                  className="text-slate-400"
                                />

                                {formatContactName(
                                  contact,
                                )}
                              </p>

                              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                                {[
                                  contact.position,
                                  contact.department,
                                ]
                                  .filter(Boolean)
                                  .join(" · ")
                                  || "No role specified"}
                              </p>
                            </div>

                            {contact.is_primary && (
                              <span className="rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-950/60 dark:text-blue-300">
                                Primary
                              </span>
                            )}
                          </div>

                          <div className="mt-3 flex flex-wrap gap-3 text-xs text-slate-500 dark:text-slate-400">
                            {contact.email && (
                              <a
                                href={`mailto:${contact.email}`}
                                className="hover:text-blue-700 dark:hover:text-blue-400"
                              >
                                {contact.email}
                              </a>
                            )}

                            {contact.phone && (
                              <a
                                href={`tel:${contact.phone}`}
                                className="hover:text-blue-700 dark:hover:text-blue-400"
                              >
                                {contact.phone}
                              </a>
                            )}
                          </div>
                        </article>
                      ),
                    )}
                  </div>
                )}
              </section>

              <section>
                <div className="flex items-center justify-between gap-4">
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Managed websites
                  </h4>

                  <span className="text-xs text-slate-500 dark:text-slate-400">
                    {client.websites.length}
                  </span>
                </div>

                {client.websites.length ===
                0 ? (
                  <p className="mt-3 rounded-lg border border-dashed border-slate-200 px-4 py-6 text-center text-sm text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    No websites recorded
                  </p>
                ) : (
                  <div className="mt-3 space-y-3">
                    {client.websites.map(
                      (website) => (
                        <article
                          key={website.id}
                          className="rounded-xl border border-slate-200 p-4 dark:border-slate-700"
                        >
                          <div className="flex items-start justify-between gap-3">
                            <div className="min-w-0">
                              <p className="font-medium text-slate-950 dark:text-white">
                                {website.name}
                              </p>

                              <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                                {website.platform
                                  || "Platform not specified"}
                              </p>
                            </div>

                            <div className="flex gap-2">
                              {website.is_primary && (
                                <span className="rounded-full bg-blue-50 px-2 py-1 text-xs font-semibold text-blue-700 dark:bg-blue-950/60 dark:text-blue-300">
                                  Primary
                                </span>
                              )}

                              <span
                                className={
                                  website.is_active
                                    ? "rounded-full bg-emerald-50 px-2 py-1 text-xs font-semibold text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300"
                                    : "rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600 dark:bg-slate-800 dark:text-slate-400"
                                }
                              >
                                {website.is_active
                                  ? "Active"
                                  : "Inactive"}
                              </span>
                            </div>
                          </div>

                          <a
                            href={normalizeExternalUrl(
                              website.url,
                            )}
                            target="_blank"
                            rel="noreferrer"
                            className="mt-3 flex items-center gap-2 text-sm text-blue-700 hover:underline dark:text-blue-400"
                          >
                            <Globe2 size={15} />
                            <span className="truncate">
                              {website.url}
                            </span>
                            <ExternalLink
                              size={13}
                            />
                          </a>
                        </article>
                      ),
                    )}
                  </div>
                )}
              </section>

              {client.tags.length > 0 && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Tags
                  </h4>

                  <div className="mt-3 flex flex-wrap gap-2">
                    {client.tags.map(
                      (tag) => (
                        <span
                          key={tag}
                          className="rounded-full bg-slate-100 px-3 py-1 text-xs font-medium text-slate-600 dark:bg-slate-800 dark:text-slate-300"
                        >
                          {tag}
                        </span>
                      ),
                    )}
                  </div>
                </section>
              )}

              {client.notes && (
                <section>
                  <h4 className="text-sm font-semibold text-slate-950 dark:text-white">
                    Notes
                  </h4>

                  <p className="mt-3 whitespace-pre-wrap rounded-xl bg-slate-50 p-4 text-sm leading-6 text-slate-600 dark:bg-slate-800/70 dark:text-slate-300">
                    {client.notes}
                  </p>
                </section>
              )}

              <section className="border-t border-slate-200 pt-4 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
                <p className="flex items-center gap-2">
                  <CalendarDays
                    size={13}
                  />
                  Created{" "}
                  {formatDateTime(
                    client.created_at,
                  )}
                </p>

                <p className="mt-1">
                  Updated{" "}
                  {formatDateTime(
                    client.updated_at,
                  )}
                </p>
              </section>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}
