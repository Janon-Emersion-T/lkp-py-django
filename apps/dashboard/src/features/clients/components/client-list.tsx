import {
  Building2,
  ChevronRight,
  Globe2,
  Inbox,
  Mail,
  MapPin,
  UsersRound,
} from "lucide-react";

import {
  formatCount,
} from "../formatters";
import type {
  Client,
} from "../types";
import {
  ClientStatusBadge,
  ClientTypeBadge,
} from "./client-badges";

interface ClientListProps {
  clients: Client[];
  onSelect: (
    clientId: string,
  ) => void;
}

export function ClientList({
  clients,
  onSelect,
}: ClientListProps) {
  if (clients.length === 0) {
    return (
      <section className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-14 text-center dark:border-slate-700 dark:bg-slate-900">
        <Inbox
          size={30}
          className="mx-auto text-slate-300 dark:text-slate-600"
        />

        <h2 className="mt-4 font-semibold text-slate-950 dark:text-white">
          No clients found
        </h2>

        <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">
          No client records match the current search and filters.
        </p>
      </section>
    );
  }

  return (
    <>
      <section className="hidden overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm lg:block dark:border-slate-800 dark:bg-slate-900">
        <div className="overflow-x-auto">
          <table className="w-full min-w-[1050px] border-collapse">
            <thead className="bg-slate-50 dark:bg-slate-800/70">
              <tr className="text-left text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                <th className="px-5 py-3">
                  Client
                </th>
                <th className="px-5 py-3">
                  Status
                </th>
                <th className="px-5 py-3">
                  Industry
                </th>
                <th className="px-5 py-3">
                  Country
                </th>
                <th className="px-5 py-3">
                  Contacts
                </th>
                <th className="px-5 py-3">
                  Websites
                </th>
                <th className="px-5 py-3">
                  Payment terms
                </th>
                <th className="w-12 px-3 py-3">
                  <span className="sr-only">
                    View
                  </span>
                </th>
              </tr>
            </thead>

            <tbody>
              {clients.map(
                (client) => (
                  <tr
                    key={client.id}
                    className="border-t border-slate-200 transition hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/50"
                  >
                    <td className="px-5 py-4">
                      <button
                        type="button"
                        onClick={() => {
                          onSelect(
                            client.id,
                          );
                        }}
                        className="text-left"
                      >
                        <p className="font-medium text-slate-950 hover:text-blue-700 dark:text-white dark:hover:text-blue-400">
                          {
                            client.company_name
                          }
                        </p>

                        <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                          {
                            client.client_code
                          }
                        </p>

                        <div className="mt-1">
                          <ClientTypeBadge
                            clientType={
                              client.client_type
                            }
                          />
                        </div>
                      </button>
                    </td>

                    <td className="px-5 py-4">
                      <ClientStatusBadge
                        status={
                          client.status
                        }
                      />
                    </td>

                    <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                      {client.industry
                        || "Not specified"}
                    </td>

                    <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                      {client.country
                        || "Not specified"}
                    </td>

                    <td className="px-5 py-4">
                      <span className="inline-flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                        <UsersRound
                          size={15}
                          className="text-slate-400"
                        />
                        {formatCount(
                          client.contacts
                            .length,
                        )}
                      </span>
                    </td>

                    <td className="px-5 py-4">
                      <span className="inline-flex items-center gap-2 text-sm text-slate-600 dark:text-slate-300">
                        <Globe2
                          size={15}
                          className="text-slate-400"
                        />
                        {formatCount(
                          client.websites
                            .length,
                        )}
                      </span>
                    </td>

                    <td className="px-5 py-4 text-sm text-slate-600 dark:text-slate-300">
                      {
                        client.payment_terms_days
                      }{" "}
                      days
                    </td>

                    <td className="px-3 py-4">
                      <button
                        type="button"
                        onClick={() => {
                          onSelect(
                            client.id,
                          );
                        }}
                        aria-label={`View ${client.company_name}`}
                        className="grid h-8 w-8 place-items-center rounded-md text-slate-400 transition hover:bg-slate-100 hover:text-slate-950 dark:hover:bg-slate-700 dark:hover:text-white"
                      >
                        <ChevronRight
                          size={17}
                        />
                      </button>
                    </td>
                  </tr>
                ),
              )}
            </tbody>
          </table>
        </div>
      </section>

      <section className="grid gap-3 lg:hidden">
        {clients.map((client) => (
          <button
            key={client.id}
            type="button"
            onClick={() => {
              onSelect(client.id);
            }}
            className="rounded-xl border border-slate-200 bg-white p-4 text-left shadow-sm transition hover:border-blue-300 dark:border-slate-800 dark:bg-slate-900 dark:hover:border-blue-800"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="min-w-0">
                <p className="truncate font-semibold text-slate-950 dark:text-white">
                  {client.company_name}
                </p>

                <p className="mt-1 text-xs text-slate-500 dark:text-slate-400">
                  {client.client_code}
                </p>
              </div>

              <ChevronRight
                size={18}
                className="shrink-0 text-slate-400"
              />
            </div>

            <div className="mt-4 flex flex-wrap items-center gap-2">
              <ClientStatusBadge
                status={client.status}
              />

              <ClientTypeBadge
                clientType={
                  client.client_type
                }
              />
            </div>

            <div className="mt-4 grid gap-2 border-t border-slate-100 pt-3 text-xs text-slate-500 dark:border-slate-800 dark:text-slate-400">
              {client.industry && (
                <span className="flex items-center gap-2">
                  <Building2 size={13} />
                  {client.industry}
                </span>
              )}

              {client.country && (
                <span className="flex items-center gap-2">
                  <MapPin size={13} />
                  {client.country}
                </span>
              )}

              {client.email && (
                <span className="flex items-center gap-2 truncate">
                  <Mail size={13} />
                  {client.email}
                </span>
              )}
            </div>
          </button>
        ))}
      </section>
    </>
  );
}
