import {
  Check,
  ChevronLeft,
  ChevronRight,
  Clipboard,
  Eye,
  File,
  FileImage,
  FileText,
  FilterX,
  FolderPlus,
  Grid2X2,
  LoaderCircle,
  Lock,
  Pencil,
  Search,
  Trash2,
  Upload,
  X,
} from "lucide-react";
import {
  useMemo,
  useState,
} from "react";

import {
  formatBytes,
  formatDateTime,
  isImageAsset,
  mediaTypeLabels,
  resolveMediaUrl,
} from "../formatters";
import {
  useCreateMediaFolder,
  useDeleteMediaAsset,
  useMediaAsset,
  useMediaAssets,
  useMediaFolders,
  useUpdateMediaAsset,
  useUploadMediaAsset,
} from "../hooks";
import {
  mediaTypes,
  type MediaAsset,
  type MediaFilters,
  type MediaType,
  type UploadMediaAssetPayload,
} from "../types";

const defaultFilters:
MediaFilters = {
  page: 1,
  pageSize: 24,
  search: "",
  mediaType: "",
  folderId: "",
  visibility: "all",
  ordering: "-created_at",
};

type Dialog =
  | "upload"
  | "folder"
  | "edit"
  | "delete"
  | null;

export function MediaLibraryPage() {
  const [
    filters,
    setFilters,
  ] = useState(defaultFilters);

  const [
    selectedId,
    setSelectedId,
  ] = useState("");

  const [
    dialog,
    setDialog,
  ] = useState<Dialog>(null);

  const [
    notice,
    setNotice,
  ] = useState("");

  const foldersQuery =
    useMediaFolders();

  const assetsQuery =
    useMediaAssets(filters);

  const detailQuery =
    useMediaAsset(
      selectedId,
      selectedId !== "",
    );

  const folders =
    foldersQuery.data ?? [];

  const response =
    assetsQuery.data;

  const assets =
    response?.items ?? [];

  const pagination =
    response?.pagination;

  const totals = useMemo(
    () => ({
      visible: assets.length,
      public: assets.filter(
        (asset) => asset.is_public,
      ).length,
      used: assets.filter(
        (asset) =>
          asset.usages.length > 0,
      ).length,
      images: assets.filter(
        (asset) =>
          isImageAsset(
            asset.media_type,
          ),
      ).length,
    }),
    [assets],
  );

  const isFiltered =
    filters.search !== ""
    || filters.mediaType !== ""
    || filters.folderId !== ""
    || filters.visibility !== "all"
    || filters.ordering !==
      "-created_at";

  function updateFilters(
    values: Partial<MediaFilters>,
  ) {
    setFilters(
      (current) => ({
        ...current,
        ...values,
        page:
          values.page
          ?? (
            "page" in values
              ? current.page
              : 1
          ),
      }),
    );
  }

  function openAsset(
    asset: MediaAsset,
  ) {
    setSelectedId(asset.id);
  }

  return (
    <div className="space-y-6 pb-10">
      <header className="flex flex-col gap-4 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.18em] text-slate-400">
            Digital asset management
          </p>

          <h1 className="mt-2 text-2xl font-bold text-slate-950 dark:text-white">
            Media Library
          </h1>

          <p className="mt-2 max-w-3xl text-sm leading-6 text-slate-500 dark:text-slate-400">
            Centralise images, documents, logos, icons,
            metadata, folders, public delivery URLs, and
            asset usage across the Astro website and CMS.
          </p>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() =>
              setDialog("folder")
            }
            className="inline-flex items-center gap-2 rounded-lg border border-slate-200 px-3.5 py-2.5 text-sm font-semibold dark:border-slate-700"
          >
            <FolderPlus size={16} />
            New folder
          </button>

          <button
            type="button"
            onClick={() =>
              setDialog("upload")
            }
            className="inline-flex items-center gap-2 rounded-lg bg-blue-600 px-3.5 py-2.5 text-sm font-semibold text-white hover:bg-blue-700"
          >
            <Upload size={16} />
            Upload asset
          </button>
        </div>
      </header>

      {notice && (
        <div className="flex items-center justify-between rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm font-medium text-emerald-800 dark:border-emerald-900 dark:bg-emerald-950/30 dark:text-emerald-300">
          {notice}

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

      <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Summary
          label="Visible records"
          value={totals.visible}
        />
        <Summary
          label="Public assets"
          value={totals.public}
        />
        <Summary
          label="Used assets"
          value={totals.used}
        />
        <Summary
          label="Images and logos"
          value={totals.images}
        />
      </section>

      <section className="rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
        <div className="grid gap-3 border-b border-slate-200 p-4 lg:grid-cols-[2fr_1fr_1fr_1fr_1fr_auto] dark:border-slate-800">
          <label className="relative">
            <Search
              size={16}
              className="absolute left-3 top-3 text-slate-400"
            />

            <input
              value={filters.search}
              onChange={(event) =>
                updateFilters({
                  search:
                    event.target.value,
                })
              }
              placeholder="Search title, filename, alt text…"
              className="h-10 w-full rounded-lg border border-slate-200 bg-white pl-9 pr-3 text-sm dark:border-slate-700 dark:bg-slate-950"
            />
          </label>

          <select
            value={filters.mediaType}
            onChange={(event) =>
              updateFilters({
                mediaType:
                  event.target.value as (
                    MediaType | ""
                  ),
              })
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
          >
            <option value="">
              All media types
            </option>

            {mediaTypes.map(
              (type) => (
                <option
                  key={type}
                  value={type}
                >
                  {mediaTypeLabels[type]}
                </option>
              ),
            )}
          </select>

          <select
            value={filters.folderId}
            onChange={(event) =>
              updateFilters({
                folderId:
                  event.target.value,
              })
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
          >
            <option value="">
              All folders
            </option>

            {folders.map(
              (folder) => (
                <option
                  key={folder.id}
                  value={folder.id}
                >
                  {folder.name}
                </option>
              ),
            )}
          </select>

          <select
            value={filters.visibility}
            onChange={(event) =>
              updateFilters({
                visibility:
                  event.target.value as
                    MediaFilters["visibility"],
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

          <select
            value={filters.ordering}
            onChange={(event) =>
              updateFilters({
                ordering:
                  event.target.value,
              })
            }
            className="h-10 rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
          >
            <option value="-created_at">
              Newest first
            </option>
            <option value="created_at">
              Oldest first
            </option>
            <option value="title">
              Title A–Z
            </option>
            <option value="-title">
              Title Z–A
            </option>
            <option value="-size">
              Largest first
            </option>
            <option value="size">
              Smallest first
            </option>
          </select>

          <button
            type="button"
            disabled={!isFiltered}
            onClick={() =>
              setFilters(defaultFilters)
            }
            className="inline-flex h-10 items-center justify-center gap-2 rounded-lg border border-slate-200 px-3 text-sm font-semibold disabled:opacity-40 dark:border-slate-700"
          >
            <FilterX size={16} />
            Clear
          </button>
        </div>

        {assetsQuery.isLoading && (
          <div className="grid gap-4 p-5 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
            {Array.from({
              length: 8,
            }).map((_, index) => (
              <div
                key={index}
                className="h-72 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800"
              />
            ))}
          </div>
        )}

        {assetsQuery.isError && (
          <div className="m-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
            {assetsQuery.error.message}
          </div>
        )}

        {!assetsQuery.isLoading
        && !assetsQuery.isError
        && assets.length === 0 && (
          <div className="px-5 py-20 text-center">
            <Grid2X2
              size={36}
              className="mx-auto text-slate-300"
            />

            <h2 className="mt-4 font-semibold">
              {isFiltered
                ? "No assets match these filters"
                : "The media library is empty"}
            </h2>

            <p className="mt-2 text-sm text-slate-500">
              Upload the first reusable media asset.
            </p>
          </div>
        )}

        {assets.length > 0 && (
          <div className="grid gap-4 p-5 sm:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4">
            {assets.map(
              (asset) => (
                <AssetCard
                  key={asset.id}
                  asset={asset}
                  onOpen={() =>
                    openAsset(asset)
                  }
                  onEdit={() => {
                    setSelectedId(
                      asset.id,
                    );
                    setDialog("edit");
                  }}
                  onDelete={() => {
                    setSelectedId(
                      asset.id,
                    );
                    setDialog("delete");
                  }}
                />
              ),
            )}
          </div>
        )}

        {pagination
        && pagination.total_pages > 1 && (
          <footer className="flex flex-col gap-3 border-t border-slate-200 px-5 py-4 sm:flex-row sm:items-center sm:justify-between dark:border-slate-800">
            <p className="text-sm text-slate-500">
              Page {pagination.page} of{" "}
              {pagination.total_pages}
              {" · "}
              {pagination.total_items} assets
            </p>

            <div className="flex gap-2">
              <button
                type="button"
                disabled={
                  pagination.page <= 1
                }
                onClick={() =>
                  updateFilters({
                    page:
                      pagination.page - 1,
                  })
                }
                className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-3 py-2 text-sm disabled:opacity-40 dark:border-slate-700"
              >
                <ChevronLeft size={16} />
                Previous
              </button>

              <button
                type="button"
                disabled={
                  pagination.page
                  >= pagination.total_pages
                }
                onClick={() =>
                  updateFilters({
                    page:
                      pagination.page + 1,
                  })
                }
                className="inline-flex items-center gap-1 rounded-lg border border-slate-200 px-3 py-2 text-sm disabled:opacity-40 dark:border-slate-700"
              >
                Next
                <ChevronRight size={16} />
              </button>
            </div>
          </footer>
        )}
      </section>

      <AssetDetailPanel
        asset={
          detailQuery.data ?? null
        }
        loading={
          detailQuery.isLoading
        }
        onClose={() =>
          setSelectedId("")
        }
      />

      <MediaDialog
        dialog={dialog}
        asset={
          detailQuery.data ?? null
        }
        folders={folders}
        onClose={() =>
          setDialog(null)
        }
        onNotice={setNotice}
      />
    </div>
  );
}

function Summary({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
        {label}
      </p>

      <p className="mt-3 text-2xl font-bold">
        {value}
      </p>
    </article>
  );
}

function AssetCard({
  asset,
  onOpen,
  onEdit,
  onDelete,
}: {
  asset: MediaAsset;
  onOpen: () => void;
  onEdit: () => void;
  onDelete: () => void;
}) {
  const fileUrl =
    resolveMediaUrl(asset.file_url);

  return (
    <article className="overflow-hidden rounded-xl border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950">
      <button
        type="button"
        onClick={onOpen}
        className="block h-44 w-full overflow-hidden bg-slate-100 text-left dark:bg-slate-800"
      >
        {isImageAsset(
          asset.media_type,
        ) && fileUrl ? (
          <img
            src={fileUrl}
            alt={
              asset.alt_text
              || asset.title
            }
            className="h-full w-full object-cover"
          />
        ) : (
          <div className="flex h-full items-center justify-center">
            <AssetIcon
              type={asset.media_type}
            />
          </div>
        )}
      </button>

      <div className="p-4">
        <div className="flex items-start justify-between gap-3">
          <div className="min-w-0">
            <h3 className="truncate font-semibold">
              {asset.title}
            </h3>

            <p className="mt-1 truncate text-xs text-slate-500">
              {asset.original_name}
            </p>
          </div>

          {!asset.is_public && (
            <Lock
              size={15}
              className="shrink-0 text-amber-500"
            />
          )}
        </div>

        <div className="mt-3 flex flex-wrap gap-2 text-xs text-slate-500">
          <span>
            {mediaTypeLabels[
              asset.media_type
            ]}
          </span>
          <span>·</span>
          <span>
            {formatBytes(asset.size)}
          </span>
          <span>·</span>
          <span>
            {asset.usages.length} uses
          </span>
        </div>

        <div className="mt-4 flex gap-2">
          <button
            type="button"
            onClick={onOpen}
            className="inline-flex flex-1 items-center justify-center gap-1 rounded-lg border border-slate-200 px-2 py-2 text-xs font-semibold dark:border-slate-700"
          >
            <Eye size={14} />
            Inspect
          </button>

          <button
            type="button"
            onClick={onEdit}
            aria-label={`Edit ${asset.title}`}
            className="rounded-lg border border-slate-200 p-2 dark:border-slate-700"
          >
            <Pencil size={14} />
          </button>

          <button
            type="button"
            onClick={onDelete}
            aria-label={`Delete ${asset.title}`}
            className="rounded-lg border border-red-200 p-2 text-red-600 dark:border-red-900"
          >
            <Trash2 size={14} />
          </button>
        </div>
      </div>
    </article>
  );
}

function AssetIcon({
  type,
}: {
  type: MediaType;
}) {
  if (
    type === "image"
    || type === "logo"
    || type === "icon"
  ) {
    return (
      <FileImage
        size={40}
        className="text-slate-400"
      />
    );
  }

  if (
    type === "pdf"
    || type === "document"
  ) {
    return (
      <FileText
        size={40}
        className="text-slate-400"
      />
    );
  }

  return (
    <File
      size={40}
      className="text-slate-400"
    />
  );
}

function AssetDetailPanel({
  asset,
  loading,
  onClose,
}: {
  asset: MediaAsset | null;
  loading: boolean;
  onClose: () => void;
}) {
  const [
    copied,
    setCopied,
  ] = useState(false);

  if (!asset && !loading) {
    return null;
  }

  async function copyUrl() {
    if (!asset) {
      return;
    }

    try {
      await navigator.clipboard.writeText(
        resolveMediaUrl(
          asset.file_url,
        ),
      );

      setCopied(true);

      window.setTimeout(
        () => setCopied(false),
        1500,
      );
    } catch {
      setCopied(false);
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={onClose}
        aria-label="Close asset details"
        className="fixed inset-0 z-40 bg-slate-950/50"
      />

      <aside className="fixed inset-y-0 right-0 z-50 flex w-full max-w-3xl flex-col border-l border-slate-200 bg-white shadow-2xl dark:border-slate-800 dark:bg-slate-950">
        <header className="flex items-center justify-between border-b border-slate-200 p-5 dark:border-slate-800">
          <h2 className="font-semibold">
            Asset details
          </h2>

          <button
            type="button"
            onClick={onClose}
            aria-label="Close asset details"
          >
            <X size={19} />
          </button>
        </header>

        <div className="flex-1 overflow-y-auto p-5">
          {loading && (
            <div className="h-96 animate-pulse rounded-xl bg-slate-100 dark:bg-slate-800" />
          )}

          {asset && (
            <>
              {isImageAsset(
                asset.media_type,
              ) && asset.file_url && (
                <img
                  src={resolveMediaUrl(
                    asset.file_url,
                  )}
                  alt={
                    asset.alt_text
                    || asset.title
                  }
                  className="max-h-96 w-full rounded-xl bg-slate-100 object-contain dark:bg-slate-900"
                />
              )}

              <h3 className="mt-5 text-xl font-bold">
                {asset.title}
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                {asset.original_name}
              </p>

              <div className="mt-5 grid gap-3 sm:grid-cols-2">
                <Meta
                  label="Media type"
                  value={
                    mediaTypeLabels[
                      asset.media_type
                    ]
                  }
                />
                <Meta
                  label="File size"
                  value={formatBytes(
                    asset.size,
                  )}
                />
                <Meta
                  label="Dimensions"
                  value={
                    asset.width
                    && asset.height
                      ? `${asset.width} × ${asset.height}`
                      : "Not recorded"
                  }
                />
                <Meta
                  label="Visibility"
                  value={
                    asset.is_public
                      ? "Public"
                      : "Private"
                  }
                />
                <Meta
                  label="Folder"
                  value={
                    asset.folder_name
                    ?? "Unfiled"
                  }
                />
                <Meta
                  label="Created"
                  value={formatDateTime(
                    asset.created_at,
                  )}
                />
              </div>

              <section className="mt-5 rounded-xl border border-slate-200 p-4 dark:border-slate-800">
                <div className="flex items-center justify-between gap-3">
                  <p className="break-all text-xs text-slate-600 dark:text-slate-300">
                    {resolveMediaUrl(
                      asset.file_url,
                    )}
                  </p>

                  <button
                    type="button"
                    onClick={() => {
                      void copyUrl();
                    }}
                    aria-label="Copy asset URL"
                  >
                    {copied
                      ? <Check size={17} />
                      : <Clipboard size={17} />}
                  </button>
                </div>
              </section>

              <section className="mt-5 space-y-3">
                <TextMeta
                  label="Alternative text"
                  value={asset.alt_text}
                />
                <TextMeta
                  label="Caption"
                  value={asset.caption}
                />
                <TextMeta
                  label="Description"
                  value={asset.description}
                />
                <TextMeta
                  label="Tags"
                  value={
                    asset.tags.join(", ")
                  }
                />
              </section>

              <section className="mt-5">
                <h4 className="font-semibold">
                  Usage references
                </h4>

                {asset.usages.length === 0 ? (
                  <p className="mt-2 text-sm text-slate-500">
                    This asset is not currently registered
                    as being used.
                  </p>
                ) : (
                  <div className="mt-3 space-y-2">
                    {asset.usages.map(
                      (usage) => (
                        <div
                          key={usage.id}
                          className="rounded-lg border border-slate-200 p-3 text-sm dark:border-slate-800"
                        >
                          <p className="font-semibold">
                            {usage.application}
                            {" · "}
                            {usage.model_name}
                          </p>

                          <p className="mt-1 text-xs text-slate-500">
                            {usage.object_id}
                            {usage.field_name
                              ? ` · ${usage.field_name}`
                              : ""}
                          </p>

                          {usage.usage_context && (
                            <p className="mt-2 text-xs text-slate-500">
                              {usage.usage_context}
                            </p>
                          )}
                        </div>
                      ),
                    )}
                  </div>
                )}
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

function TextMeta({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div>
      <p className="text-xs font-semibold uppercase tracking-wider text-slate-400">
        {label}
      </p>
      <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">
        {value || "—"}
      </p>
    </div>
  );
}

function MediaDialog({
  dialog,
  asset,
  folders,
  onClose,
  onNotice,
}: {
  dialog: Dialog;
  asset: MediaAsset | null;
  folders: {
    id: string;
    name: string;
  }[];
  onClose: () => void;
  onNotice: (value: string) => void;
}) {
  const createFolderMutation =
    useCreateMediaFolder();

  const uploadMutation =
    useUploadMediaAsset();

  const updateMutation =
    useUpdateMediaAsset();

  const deleteMutation =
    useDeleteMediaAsset();

  const [
    error,
    setError,
  ] = useState("");

  if (!dialog) {
    return null;
  }

  const pending =
    createFolderMutation.isPending
    || uploadMutation.isPending
    || updateMutation.isPending
    || deleteMutation.isPending;

  return (
    <>
      <button
        type="button"
        onClick={
          pending
            ? undefined
            : onClose
        }
        aria-label="Close media dialog"
        className="fixed inset-0 z-[60] bg-slate-950/60"
      />

      <div
        role="dialog"
        aria-modal="true"
        className="fixed left-1/2 top-1/2 z-[70] max-h-[90vh] w-[calc(100%-2rem)] max-w-xl -translate-x-1/2 -translate-y-1/2 overflow-y-auto rounded-2xl border border-slate-200 bg-white p-5 shadow-2xl dark:border-slate-800 dark:bg-slate-900"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold">
            {dialog === "upload"
              ? "Upload media asset"
              : dialog === "folder"
                ? "Create media folder"
                : dialog === "edit"
                  ? "Edit media asset"
                  : "Delete media asset"}
          </h2>

          <button
            type="button"
            disabled={pending}
            onClick={onClose}
            aria-label="Close dialog"
          >
            <X size={18} />
          </button>
        </div>

        {dialog === "folder" && (
          <FolderForm
            folders={folders}
            pending={pending}
            error={error}
            onSubmit={async (
              name,
              parentId,
              description,
            ) => {
              setError("");

              try {
                const folder =
                  await createFolderMutation.mutateAsync({
                    name,
                    parent_id:
                      parentId || null,
                    description,
                  });

                onNotice(
                  `Folder “${folder.name}” was created.`,
                );
                onClose();
              } catch (caught) {
                setError(
                  caught instanceof Error
                    ? caught.message
                    : "Folder creation failed.",
                );
              }
            }}
          />
        )}

        {dialog === "upload" && (
          <UploadForm
            folders={folders}
            pending={pending}
            error={error}
            onSubmit={async (
              payload,
            ) => {
              setError("");

              try {
                const uploaded =
                  await uploadMutation.mutateAsync(
                    payload,
                  );

                onNotice(
                  `“${uploaded.title}” was uploaded successfully.`,
                );
                onClose();
              } catch (caught) {
                setError(
                  caught instanceof Error
                    ? caught.message
                    : "Upload failed.",
                );
              }
            }}
          />
        )}

        {dialog === "edit"
        && asset && (
          <EditForm
            asset={asset}
            folders={folders}
            pending={pending}
            error={error}
            onSubmit={async (
              payload,
            ) => {
              setError("");

              try {
                const updated =
                  await updateMutation.mutateAsync({
                    assetId: asset.id,
                    payload,
                  });

                onNotice(
                  `“${updated.title}” was updated.`,
                );
                onClose();
              } catch (caught) {
                setError(
                  caught instanceof Error
                    ? caught.message
                    : "Update failed.",
                );
              }
            }}
          />
        )}

        {dialog === "delete"
        && asset && (
          <DeleteForm
            asset={asset}
            pending={pending}
            error={error}
            onDelete={async () => {
              setError("");

              try {
                const message =
                  await deleteMutation.mutateAsync(
                    asset.id,
                  );

                onNotice(message);
                onClose();
              } catch (caught) {
                setError(
                  caught instanceof Error
                    ? caught.message
                    : "Deletion failed.",
                );
              }
            }}
          />
        )}
      </div>
    </>
  );
}

function FolderForm({
  folders,
  pending,
  error,
  onSubmit,
}: {
  folders: {
    id: string;
    name: string;
  }[];
  pending: boolean;
  error: string;
  onSubmit: (
    name: string,
    parentId: string,
    description: string,
  ) => Promise<void>;
}) {
  const [
    name,
    setName,
  ] = useState("");

  const [
    parentId,
    setParentId,
  ] = useState("");

  const [
    description,
    setDescription,
  ] = useState("");

  return (
    <form
      className="mt-5 space-y-4"
      onSubmit={(event) => {
        event.preventDefault();

        void onSubmit(
          name.trim(),
          parentId,
          description,
        );
      }}
    >
      <Input
        label="Folder name"
        value={name}
        onChange={setName}
        required
      />

      <SelectFolder
        folders={folders}
        value={parentId}
        onChange={setParentId}
        label="Parent folder"
      />

      <Textarea
        label="Description"
        value={description}
        onChange={setDescription}
      />

      <FormError value={error} />

      <SubmitButton
        pending={pending}
        label="Create folder"
      />
    </form>
  );
}

function UploadForm({
  folders,
  pending,
  error,
  onSubmit,
}: {
  folders: {
    id: string;
    name: string;
  }[];
  pending: boolean;
  error: string;
  onSubmit: (
    payload: UploadMediaAssetPayload,
  ) => Promise<void>;
}) {
  const [
    file,
    setFile,
  ] = useState<File | null>(null);

  const [
    title,
    setTitle,
  ] = useState("");

  const [
    folderId,
    setFolderId,
  ] = useState("");

  const [
    mediaType,
    setMediaType,
  ] = useState<MediaType | "">("");

  const [
    altText,
    setAltText,
  ] = useState("");

  const [
    caption,
    setCaption,
  ] = useState("");

  const [
    description,
    setDescription,
  ] = useState("");

  const [
    isPublic,
    setIsPublic,
  ] = useState(true);

  return (
    <form
      className="mt-5 space-y-4"
      onSubmit={(event) => {
        event.preventDefault();

        if (!file) {
          return;
        }

        void onSubmit({
          file,
          title,
          folderId,
          mediaType,
          altText,
          caption,
          description,
          isPublic,
        });
      }}
    >
      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          File
        </span>

        <input
          type="file"
          required
          onChange={(event) =>
            setFile(
              event.target.files?.[0]
              ?? null,
            )
          }
          className="block w-full rounded-lg border border-slate-200 p-3 text-sm dark:border-slate-700"
        />
      </label>

      <Input
        label="Title"
        value={title}
        onChange={setTitle}
        placeholder="Defaults to filename"
      />

      <SelectFolder
        folders={folders}
        value={folderId}
        onChange={setFolderId}
        label="Folder"
      />

      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          Media type
        </span>

        <select
          value={mediaType}
          onChange={(event) =>
            setMediaType(
              event.target.value as (
                MediaType | ""
              ),
            )
          }
          className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          <option value="">
            Detect automatically
          </option>

          {mediaTypes.map(
            (type) => (
              <option
                key={type}
                value={type}
              >
                {mediaTypeLabels[type]}
              </option>
            ),
          )}
        </select>
      </label>

      <Input
        label="Alternative text"
        value={altText}
        onChange={setAltText}
        maxLength={250}
      />

      <Textarea
        label="Caption"
        value={caption}
        onChange={setCaption}
      />

      <Textarea
        label="Description"
        value={description}
        onChange={setDescription}
      />

      <Checkbox
        label="Publicly accessible asset"
        checked={isPublic}
        onChange={setIsPublic}
      />

      <FormError value={error} />

      <SubmitButton
        pending={pending}
        label="Upload asset"
        disabled={!file}
      />
    </form>
  );
}

function EditForm({
  asset,
  folders,
  pending,
  error,
  onSubmit,
}: {
  asset: MediaAsset;
  folders: {
    id: string;
    name: string;
  }[];
  pending: boolean;
  error: string;
  onSubmit: (
    payload: {
      folder_id: string | null;
      title: string;
      media_type: MediaType;
      alt_text: string;
      caption: string;
      description: string;
      tags: string[];
      is_public: boolean;
    },
  ) => Promise<void>;
}) {
  const [
    title,
    setTitle,
  ] = useState(asset.title);

  const [
    folderId,
    setFolderId,
  ] = useState(
    asset.folder_id ?? "",
  );

  const [
    mediaType,
    setMediaType,
  ] = useState(asset.media_type);

  const [
    altText,
    setAltText,
  ] = useState(asset.alt_text);

  const [
    caption,
    setCaption,
  ] = useState(asset.caption);

  const [
    description,
    setDescription,
  ] = useState(asset.description);

  const [
    tags,
    setTags,
  ] = useState(
    asset.tags.join(", "),
  );

  const [
    isPublic,
    setIsPublic,
  ] = useState(asset.is_public);

  return (
    <form
      className="mt-5 space-y-4"
      onSubmit={(event) => {
        event.preventDefault();

        void onSubmit({
          folder_id:
            folderId || null,
          title: title.trim(),
          media_type: mediaType,
          alt_text: altText,
          caption,
          description,
          tags: tags
            .split(",")
            .map((tag) =>
              tag.trim(),
            )
            .filter(Boolean),
          is_public: isPublic,
        });
      }}
    >
      <Input
        label="Title"
        value={title}
        onChange={setTitle}
        required
        maxLength={250}
      />

      <SelectFolder
        folders={folders}
        value={folderId}
        onChange={setFolderId}
        label="Folder"
      />

      <label className="block space-y-1.5">
        <span className="text-sm font-semibold">
          Media type
        </span>

        <select
          value={mediaType}
          onChange={(event) =>
            setMediaType(
              event.target.value as MediaType,
            )
          }
          className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
        >
          {mediaTypes.map(
            (type) => (
              <option
                key={type}
                value={type}
              >
                {mediaTypeLabels[type]}
              </option>
            ),
          )}
        </select>
      </label>

      <Input
        label="Alternative text"
        value={altText}
        onChange={setAltText}
        maxLength={250}
      />

      <Input
        label="Tags"
        value={tags}
        onChange={setTags}
        placeholder="website, hero, brand"
      />

      <Textarea
        label="Caption"
        value={caption}
        onChange={setCaption}
      />

      <Textarea
        label="Description"
        value={description}
        onChange={setDescription}
      />

      <Checkbox
        label="Publicly accessible asset"
        checked={isPublic}
        onChange={setIsPublic}
      />

      <FormError value={error} />

      <SubmitButton
        pending={pending}
        label="Save changes"
      />
    </form>
  );
}

function DeleteForm({
  asset,
  pending,
  error,
  onDelete,
}: {
  asset: MediaAsset;
  pending: boolean;
  error: string;
  onDelete: () => Promise<void>;
}) {
  return (
    <div className="mt-5">
      <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm leading-6 text-red-800 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
        Delete <strong>{asset.title}</strong>?
        This is a soft deletion. The backend will block
        deletion when registered usage references exist.
      </div>

      {asset.usages.length > 0 && (
        <p className="mt-3 text-sm font-semibold text-amber-700 dark:text-amber-300">
          This asset currently has{" "}
          {asset.usages.length} usage reference
          {asset.usages.length === 1 ? "" : "s"}.
        </p>
      )}

      <FormError value={error} />

      <button
        type="button"
        disabled={pending}
        onClick={() => {
          void onDelete();
        }}
        className="mt-5 inline-flex w-full items-center justify-center gap-2 rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50"
      >
        {pending && (
          <LoaderCircle
            size={16}
            className="animate-spin"
          />
        )}
        Delete asset
      </button>
    </div>
  );
}

function Input({
  label,
  value,
  onChange,
  required = false,
  placeholder,
  maxLength,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
  required?: boolean;
  placeholder?: string;
  maxLength?: number;
}) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm font-semibold">
        {label}
      </span>

      <input
        value={value}
        required={required}
        placeholder={placeholder}
        maxLength={maxLength}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="h-10 w-full rounded-lg border border-slate-200 bg-white px-3 text-sm dark:border-slate-700 dark:bg-slate-950"
      />
    </label>
  );
}

function Textarea({
  label,
  value,
  onChange,
}: {
  label: string;
  value: string;
  onChange: (value: string) => void;
}) {
  return (
    <label className="block space-y-1.5">
      <span className="text-sm font-semibold">
        {label}
      </span>

      <textarea
        value={value}
        rows={3}
        onChange={(event) =>
          onChange(event.target.value)
        }
        className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2 text-sm dark:border-slate-700 dark:bg-slate-950"
      />
    </label>
  );
}

function SelectFolder({
  folders,
  value,
  onChange,
  label,
}: {
  folders: {
    id: string;
    name: string;
  }[];
  value: string;
  onChange: (value: string) => void;
  label: string;
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
        <option value="">
          No folder
        </option>

        {folders.map(
          (folder) => (
            <option
              key={folder.id}
              value={folder.id}
            >
              {folder.name}
            </option>
          ),
        )}
      </select>
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

function FormError({
  value,
}: {
  value: string;
}) {
  if (!value) {
    return null;
  }

  return (
    <p className="mt-4 rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/30 dark:text-red-300">
      {value}
    </p>
  );
}

function SubmitButton({
  pending,
  label,
  disabled = false,
}: {
  pending: boolean;
  label: string;
  disabled?: boolean;
}) {
  return (
    <button
      type="submit"
      disabled={
        pending || disabled
      }
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
