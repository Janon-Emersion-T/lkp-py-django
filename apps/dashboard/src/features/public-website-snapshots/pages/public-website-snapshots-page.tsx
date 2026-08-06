import {
  ArchiveX,
  CheckCircle2,
  Clipboard,
  DatabaseZap,
  Eye,
  FileJson2,
  FilterX,
  Globe2,
  LoaderCircle,
  RefreshCcw,
  RotateCw,
  Sparkles,
  X,
} from "lucide-react";
import {
  useMemo,
  useState,
} from "react";

import {
  getRawPreviewUrl,
} from "../api";
import {
  formatDateTime,
  formatJson,
  formatPayloadSize,
  getSnapshotState,
  isPreviewable,
  shortenChecksum,
  snapshotTypeLabels,
} from "../formatters";
import {
  useGenerateSnapshot,
  useInvalidateSnapshots,
  useRefreshAllSnapshots,
  useSnapshotPreview,
  useSnapshots,
} from "../hooks";
import {
  snapshotTypes,
  type PreviewableSnapshotType,
  type PublicWebsiteSnapshot,
  type SnapshotFilters,
  type SnapshotType,
} from "../types";

const defaultFilters:
SnapshotFilters = {
  snapshotType: "",
  environment: "",
  activeState: "all",
};

const defaultTtlMinutes = 30;

type Operation =
  | "generate"
  | "refresh"
  | "invalidate"
  | null;

export function PublicWebsiteSnapshotsPage() {
  const [
    filters,
    setFilters,
  ] = useState(defaultFilters);

  const [
    selected,
    setSelected,
  ] = useState<
    PublicWebsiteSnapshot | null
  >(null);

  const [
    preview,
    setPreview,
  ] = useState<{
    type: PreviewableSnapshotType;
    environment: string;
  } | null>(null);

  const [
    operation,
    setOperation,
  ] = useState<Operation>(null);

  const [
    notice,
    setNotice,
  ] = useState("");

  const snapshotsQuery =
    useSnapshots(filters);

  const snapshots = useMemo(
    () => snapshotsQuery.data ?? [],
    [snapshotsQuery.data],
  );

  const summary = useMemo(() => {
    const validDates =
      snapshots
        .map((snapshot) =>
          new Date(
            snapshot.generated_at,
          ).getTime(),
        )
        .filter(Number.isFinite)
        .sort(
          (left, right) =>
            right - left,
        );

    return {
      total: snapshots.length,
      active:
        snapshots.filter(
          (snapshot) =>
            snapshot.is_active,
        ).length,
      expired:
        snapshots.filter(
          (snapshot) =>
            snapshot.is_expired,
        ).length,
      inactive:
        snapshots.filter(
          (snapshot) =>
            !snapshot.is_active,
        ).length,
      environments:
        new Set(
          snapshots.map(
            (snapshot) =>
              snapshot.environment,
          ),
        ).size,
      latest:
        validDates[0]
          ? new Date(
            validDates[0],
          ).toISOString()
          : null,
    };
  }, [snapshots]);

  const isFiltered =
    filters.snapshotType !== ""
    || filters.environment.trim() !== ""
    || filters.activeState !== "all";

  return (
    <div className="space-y-6 pb-10">
      <header className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Astro public delivery layer
          </p>

          <h1 className="mt-2 text-2xl font-bold tracking-tight text-slate-950 dark:text-white">
            Website Snapshots
          </h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500 dark:text-slate-400">
            Administer versioned Django API payloads consumed
            by the Astro public website without turning the
            SEO-critical site into a React SPA.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => {
              void snapshotsQuery.refetch();
            }}
            disabled={snapshotsQuery.isFetching}
            className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-3.5 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50 disabled:opacity-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            <RefreshCcw
              size={16}
              className={
                snapshotsQuery.isFetching
                  ? "animate-spin"
                  : ""
              }
            />
            Reload records
          </button>

          <button
            type="button"
            onClick={() =>
              setOperation("invalidate")
            }
            className="inline-flex items-center gap-2 rounded-lg border border-red-200 px-3.5 py-2.5 text-sm font-semibold text-red-700 hover:bg-red-50 dark:border-red-900 dark:text-red-300"
          >
            <ArchiveX size={16} />
            Invalidate
          </button>

          <button
            type="button"
            onClick={() =>
              setOperation("refresh")
            }
            className="inline-flex items-center gap-2 rounded-lg bg-slate-900 px-3.5 py-2.5 text-sm font-semibold text-white hover:bg-slate-800 dark:bg-white dark:text-slate-950"
          >
            <RotateCw size={16} />
            Refresh all snapshots
          </button>

          <button
            type="button"
            onClick={() =>
              setOperation("generate")
            }
            className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
          >
            <Sparkles size={16} />
            Generate snapshot
          </button>
        </div>
      </header>

      {notice && (
        <div className="flex items-start justify-between rounded-xl border border-emerald-200 bg-emerald-50 p-4 dark:border-emerald-900 dark:bg-emerald-950/30">
          <div className="flex gap-3">
            <CheckCircle2
              size={19}
              className="mt-0.5 text-emerald-600"
            />

            <p className="text-sm font-medium text-emerald-800 dark:text-emerald-300">
              {notice}
            </p>
          </div>

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

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-6">
        <Summary
          label="Total"
          value={summary.total}
          icon={DatabaseZap}
        />
        <Summary
          label="Active"
          value={summary.active}
          icon={CheckCircle2}
        />
        <Summary
          label="Expired"
          value={summary.expired}
          icon={RefreshCcw}
        />
        <Summary
          label="Inactive"
          value={summary.inactive}
          icon={ArchiveX}
        />
        <Summary
          label="Environments"
          value={summary.environments}
          icon={Globe2}
        />
        <Summary
          label="Latest"
          value={
            summary.latest
              ? formatDateTime(
                summary.latest,
              )
              : "—"
          }
          icon={FileJson2}
          compact
        />
      </section>

      <section className="rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
        <div className="grid gap-4 border-b border-slate-200 p-4 md:grid-cols-[1fr_1fr_1fr_auto] dark:border-slate-800">
          <select
            value={filters.snapshotType}
            onChange={(event) =>
              setFilters(
                (current) => ({
                  ...current,
                  snapshotType:
                    event.target.value as (
                      SnapshotType | ""
                    ),
                }),
              )
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
            aria-label="Filter by snapshot type"
          >
            <option value="">
              All snapshot types
            </option>

            {snapshotTypes.map(
              (type) => (
                <option
                  key={type}
                  value={type}
                >
                  {snapshotTypeLabels[type]}
                </option>
              ),
            )}
          </select>

          <input
            value={filters.environment}
            onChange={(event) =>
              setFilters(
                (current) => ({
                  ...current,
                  environment:
                    event.target.value,
                }),
              )
            }
            placeholder="All environments"
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
            aria-label="Filter by environment"
          />

          <select
            value={filters.activeState}
            onChange={(event) =>
              setFilters(
                (current) => ({
                  ...current,
                  activeState:
                    event.target.value as
                      SnapshotFilters["activeState"],
                }),
              )
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
            aria-label="Filter by active state"
          >
            <option value="all">
              All states
            </option>
            <option value="active">
              Active
            </option>
            <option value="inactive">
              Inactive
            </option>
          </select>

          <button
            type="button"
            onClick={() =>
              setFilters(defaultFilters)
            }
            disabled={!isFiltered}
            className="inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 text-sm font-semibold disabled:opacity-40 dark:border-slate-700"
          >
            <FilterX size={16} />
            Clear
          </button>
        </div>

        {snapshotsQuery.isLoading && (
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
        )}

        {snapshotsQuery.isError && (
          <div className="m-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            {snapshotsQuery.error.message}
          </div>
        )}

        {!snapshotsQuery.isLoading
        && !snapshotsQuery.isError
        && snapshots.length === 0 && (
          <div className="px-5 py-16 text-center">
            <FileJson2
              size={34}
              className="mx-auto text-slate-300"
            />

            <h2 className="mt-4 font-semibold text-slate-950 dark:text-white">
              {isFiltered
                ? "No snapshots match the filters"
                : "No snapshots have been generated"}
            </h2>
          </div>
        )}

        {snapshots.length > 0 && (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 dark:divide-slate-800">
              <thead className="bg-slate-50 dark:bg-slate-950/40">
                <tr className="text-left text-xs font-semibold uppercase tracking-wider text-slate-400">
                  <th className="px-4 py-3">
                    Snapshot
                  </th>
                  <th className="px-4 py-3">
                    Version
                  </th>
                  <th className="px-4 py-3">
                    State
                  </th>
                  <th className="px-4 py-3">
                    Generated
                  </th>
                  <th className="px-4 py-3">
                    Expires
                  </th>
                  <th className="px-4 py-3">
                    Checksum
                  </th>
                  <th className="px-4 py-3 text-right">
                    Actions
                  </th>
                </tr>
              </thead>

              <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
                {snapshots.map(
                  (snapshot) => {
                    const state =
                      getSnapshotState(
                        snapshot,
                      );

                    return (
                      <tr
                        key={snapshot.id}
                        className="text-sm"
                      >
                        <td className="px-4 py-4">
                          <p className="font-semibold text-slate-950 dark:text-white">
                            {snapshotTypeLabels[
                              snapshot.snapshot_type
                            ]}
                          </p>
                          <p className="mt-1 text-xs text-slate-500">
                            {snapshot.environment}
                          </p>
                        </td>

                        <td className="px-4 py-4 font-mono text-xs">
                          v{snapshot.version}
                        </td>

                        <td className="px-4 py-4">
                          <span
                            className={`rounded-full border px-2.5 py-1 text-xs font-semibold ${state.className}`}
                          >
                            {state.label}
                          </span>
                        </td>

                        <td className="whitespace-nowrap px-4 py-4 text-xs">
                          {formatDateTime(
                            snapshot.generated_at,
                          )}
                        </td>

                        <td className="whitespace-nowrap px-4 py-4 text-xs">
                          {formatDateTime(
                            snapshot.expires_at,
                          )}
                        </td>

                        <td className="px-4 py-4 font-mono text-xs">
                          {shortenChecksum(
                            snapshot.checksum,
                          )}
                        </td>

                        <td className="px-4 py-4">
                          <div className="flex justify-end gap-2">
                            {isPreviewable(
                              snapshot.snapshot_type,
                            ) ? (
                              <button
                                type="button"
                                onClick={() =>
                                  setPreview({
                                    type:
                                      snapshot.snapshot_type,
                                    environment:
                                      snapshot.environment,
                                  })
                                }
                                className="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
                              >
                                <Eye size={14} />
                                Preview
                              </button>
                            ) : (
                              <span className="rounded-lg border border-slate-200 px-2.5 py-2 text-xs text-slate-400 dark:border-slate-700">
                                Preview unavailable
                              </span>
                            )}

                            <button
                              type="button"
                              onClick={() =>
                                setSelected(
                                  snapshot,
                                )
                              }
                              className="rounded-lg border border-slate-200 px-2.5 py-2 text-xs font-semibold dark:border-slate-700"
                            >
                              Inspect
                            </button>
                          </div>
                        </td>
                      </tr>
                    );
                  },
                )}
              </tbody>
            </table>
          </div>
        )}
      </section>

      <DetailPanel
        snapshot={selected}
        onClose={() =>
          setSelected(null)
        }
      />

      <PreviewPanel
        preview={preview}
        onClose={() =>
          setPreview(null)
        }
      />

      <OperationDialog
        operation={operation}
        onClose={() =>
          setOperation(null)
        }
        onNotice={setNotice}
      />
    </div>
  );
}

function Summary({
  label,
  value,
  icon: Icon,
  compact = false,
}: {
  label: string;
  value: string | number;
  icon: typeof DatabaseZap;
  compact?: boolean;
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

      <p
        className={
          compact
            ? "mt-3 text-sm font-semibold"
            : "mt-3 text-2xl font-bold"
        }
      >
        {value}
      </p>
    </article>
  );
}

function DetailPanel({
  snapshot,
  onClose,
}: {
  snapshot: PublicWebsiteSnapshot | null;
  onClose: () => void;
}) {
  const [
    copied,
    setCopied,
  ] = useState("");

  if (!snapshot) {
    return null;
  }

  async function copy(
    type: string,
    value: string,
  ) {
    try {
      await navigator.clipboard.writeText(
        value,
      );
      setCopied(type);
      window.setTimeout(
        () => setCopied(""),
        1500,
      );
    } catch {
      setCopied("");
    }
  }

  return (
    <PanelShell
      title={`${snapshotTypeLabels[
        snapshot.snapshot_type
      ]} · ${snapshot.environment} · v${snapshot.version}`}
      onClose={onClose}
    >
      <div className="grid gap-3 sm:grid-cols-2">
        <Metadata
          label="Generated"
          value={formatDateTime(
            snapshot.generated_at,
          )}
        />
        <Metadata
          label="Expires"
          value={formatDateTime(
            snapshot.expires_at,
          )}
        />
        <Metadata
          label="Payload size"
          value={formatPayloadSize(
            snapshot.payload,
          )}
        />
        <Metadata
          label="Active"
          value={
            snapshot.is_active
              ? "Yes"
              : "No"
          }
        />
      </div>

      <section className="mt-5 rounded-xl border border-slate-200 p-4 dark:border-slate-800">
        <div className="flex items-center justify-between gap-4">
          <p className="break-all font-mono text-xs">
            {snapshot.checksum}
          </p>

          <button
            type="button"
            onClick={() => {
              void copy(
                "checksum",
                snapshot.checksum,
              );
            }}
            aria-label="Copy checksum"
          >
            {copied === "checksum"
              ? <CheckCircle2 size={17} />
              : <Clipboard size={17} />}
          </button>
        </div>
      </section>

      <div className="mt-5 flex justify-end">
        <button
          type="button"
          onClick={() => {
            void copy(
              "payload",
              formatJson(
                snapshot.payload,
              ),
            );
          }}
          className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-3 py-2 text-sm dark:border-slate-700"
        >
          <Clipboard size={16} />
          {copied === "payload"
            ? "Copied"
            : "Copy payload"}
        </button>
      </div>

      <pre className="mt-3 max-h-[60vh] overflow-auto rounded-xl bg-slate-950 p-5 text-xs leading-6 text-slate-200">
        {formatJson(
          snapshot.payload,
        )}
      </pre>
    </PanelShell>
  );
}

function PreviewPanel({
  preview,
  onClose,
}: {
  preview: {
    type: PreviewableSnapshotType;
    environment: string;
  } | null;
  onClose: () => void;
}) {
  const query =
    useSnapshotPreview(
      preview?.type ?? "bootstrap",
      preview?.environment
      ?? "production",
      preview !== null,
    );

  if (!preview) {
    return null;
  }

  const hasMetadata =
    query.data
    && typeof query.data.snapshot
      === "object"
    && query.data.snapshot !== null;

  return (
    <PanelShell
      title={`${snapshotTypeLabels[
        preview.type
      ]} public preview · ${preview.environment}`}
      onClose={onClose}
    >
      <div className="flex flex-wrap items-center justify-between gap-3">
        <p className="text-sm text-slate-500">
          {hasMetadata
            ? "Served from a stored snapshot."
            : "No snapshot metadata detected; this may be live-built data."}
        </p>

        <button
          type="button"
          onClick={() =>
            window.open(
              getRawPreviewUrl(
                preview.type,
                preview.environment,
              ),
              "_blank",
              "noopener,noreferrer",
            )
          }
          className="rounded-lg border border-slate-200 px-3 py-2 text-sm dark:border-slate-700"
        >
          Open raw API
        </button>
      </div>

      {query.isLoading && (
        <div className="mt-4 h-96 animate-pulse rounded-xl bg-slate-200 dark:bg-slate-800" />
      )}

      {query.isError && (
        <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
          {query.error.message}
        </div>
      )}

      {query.data && (
        <pre className="mt-4 max-h-[70vh] overflow-auto rounded-xl bg-slate-950 p-5 text-xs leading-6 text-slate-200">
          {formatJson(query.data)}
        </pre>
      )}
    </PanelShell>
  );
}

function OperationDialog({
  operation,
  onClose,
  onNotice,
}: {
  operation: Operation;
  onClose: () => void;
  onNotice: (notice: string) => void;
}) {
  const [
    type,
    setType,
  ] = useState<
    SnapshotType | ""
  >("bootstrap");

  const [
    environment,
    setEnvironment,
  ] = useState("production");

  const [
    ttlMinutes,
    setTtlMinutes,
  ] = useState(
    defaultTtlMinutes,
  );

  const [
    error,
    setError,
  ] = useState("");

  const generateMutation =
    useGenerateSnapshot();

  const refreshMutation =
    useRefreshAllSnapshots();

  const invalidateMutation =
    useInvalidateSnapshots();

  const pending =
    generateMutation.isPending
    || refreshMutation.isPending
    || invalidateMutation.isPending;

  if (!operation) {
    return null;
  }

  async function submit() {
    setError("");

    try {
      if (operation === "generate") {
        if (!type) {
          throw new Error(
            "Snapshot type is required.",
          );
        }

        if (!environment.trim()) {
          throw new Error(
            "Environment is required.",
          );
        }

        if (ttlMinutes < 1) {
          throw new Error(
            "TTL must be at least one minute.",
          );
        }

        const snapshot =
          await generateMutation.mutateAsync({
            snapshot_type: type,
            environment:
              environment.trim(),
            ttl_minutes:
              ttlMinutes,
          });

        onNotice(
          `${snapshotTypeLabels[
            snapshot.snapshot_type
          ]} ${snapshot.environment} version ${snapshot.version} was generated.`,
        );
      }

      if (operation === "refresh") {
        if (!environment.trim()) {
          throw new Error(
            "Environment is required.",
          );
        }

        if (ttlMinutes < 1) {
          throw new Error(
            "TTL must be at least one minute.",
          );
        }

        const result =
          await refreshMutation.mutateAsync({
            environment:
              environment.trim(),
            ttl_minutes:
              ttlMinutes,
          });

        const versions =
          result.snapshots
            .map(
              (snapshot) =>
                `${snapshotTypeLabels[
                  snapshot.snapshot_type
                ]} v${snapshot.version}`,
            )
            .join(", ");

        onNotice(
          `${result.snapshot_count} snapshots refreshed for ${result.environment}: ${versions}.`,
        );
      }

      if (operation === "invalidate") {
        const result =
          await invalidateMutation.mutateAsync({
            snapshot_type:
              type || null,
            environment:
              environment.trim()
                || null,
          });

        onNotice(
          `${result.invalidated_count} active snapshot record${result.invalidated_count === 1 ? "" : "s"} invalidated.`,
        );
      }

      onClose();
    } catch (caught) {
      setError(
        caught instanceof Error
          ? caught.message
          : "Operation failed.",
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
        aria-label="Close snapshot operation"
        className="fixed inset-0 z-[60] bg-slate-950/60"
      />

      <div
        role="dialog"
        aria-modal="true"
        className="fixed left-1/2 top-1/2 z-[70] w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl dark:border-slate-800 dark:bg-slate-900"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold capitalize">
            {operation === "refresh"
              ? "Refresh all snapshots"
              : `${operation} snapshots`}
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

        <div className="mt-5 space-y-4">
          {operation !== "refresh" && (
            <select
              value={type}
              onChange={(event) =>
                setType(
                  (event.target.value as SnapshotType | ""),
                )
              }
              className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
              aria-label="Snapshot type"
            >
              {operation === "invalidate" && (
                <option value="">
                  All snapshot types
                </option>
              )}

              {snapshotTypes.map(
                (snapshotType) => (
                  <option
                    key={snapshotType}
                    value={snapshotType}
                  >
                    {snapshotTypeLabels[
                      snapshotType
                    ]}
                  </option>
                ),
              )}
            </select>
          )}

          <input
            value={environment}
            onChange={(event) =>
              setEnvironment(
                event.target.value,
              )
            }
            placeholder={
              operation === "invalidate"
                ? "Empty means all environments"
                : "production"
            }
            className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
            aria-label="Environment"
          />

          {operation !== "invalidate" && (
            <input
              type="number"
              min={1}
              step={1}
              value={ttlMinutes}
              onChange={(event) =>
                setTtlMinutes(
                  Number(
                    event.target.value,
                  ),
                )
              }
              className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
              aria-label="TTL minutes"
            />
          )}

          {operation === "refresh" && (
            <p className="rounded-xl border border-amber-200 bg-amber-50 p-4 text-sm leading-6 text-amber-800 dark:border-amber-900 dark:bg-amber-950/30 dark:text-amber-300">
              This generates new versions of bootstrap,
              homepage, catalog, and content snapshots and
              replaces the currently active versions.
            </p>
          )}

          {operation === "invalidate" && (
            <p className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm leading-6 text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              Empty type and environment fields invalidate
              every active public website snapshot globally.
            </p>
          )}

          {error && (
            <p className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
              {error}
            </p>
          )}
        </div>

        <div className="mt-6 flex justify-end gap-2">
          <button
            type="button"
            onClick={onClose}
            disabled={pending}
            className="rounded-lg border border-slate-200 px-4 py-2.5 text-sm font-semibold dark:border-slate-700"
          >
            Cancel
          </button>

          <button
            type="button"
            onClick={() => {
              void submit();
            }}
            disabled={pending}
            className={`inline-flex items-center gap-2 rounded-lg px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50 ${
              operation === "invalidate"
                ? "bg-red-600"
                : "bg-blue-600"
            }`}
          >
            {pending && (
              <LoaderCircle
                size={16}
                className="animate-spin"
              />
            )}
            Confirm
          </button>
        </div>
      </div>
    </>
  );
}

function PanelShell({
  title,
  onClose,
  children,
}: {
  title: string;
  onClose: () => void;
  children: React.ReactNode;
}) {
  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close panel"
        className="fixed inset-0 z-40 bg-slate-950/50"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-4xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-950">
        <header className="flex items-center justify-between border-b border-slate-200 px-5 py-4 dark:border-slate-800">
          <h2 className="font-semibold">
            {title}
          </h2>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close panel"
          >
            <X size={19} />
          </button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {children}
        </div>
      </aside>
    </>
  );
}

function Metadata({
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
