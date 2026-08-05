from ninja import File, Form, Router
from ninja.files import UploadedFile

from apps.api.auth import jwt_auth
from apps.api.common_schemas import ErrorSchema, MessageSchema
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import PaginatedResponseSchema
from apps.api.responses import paginated_response
from apps.common.pagination import paginate_queryset
from apps.rbac.services import require_permissions

from .models import (
    MediaAsset,
    MediaFolder,
)
from .repositories import (
    MediaAssetRepository,
    MediaFolderRepository,
)
from .schemas import (
    MediaAssetSchema,
    MediaAssetUpdateSchema,
    MediaFolderCreateSchema,
    MediaFolderSchema,
    MediaUsageCreateSchema,
    MediaUsageSchema,
)
from .services import MediaLibraryService


router = Router(
    tags=["Media Library"],
    auth=jwt_auth,
)


def file_url(file_field):
    if not file_field:
        return None

    try:
        return file_field.url
    except ValueError:
        return None


def serialize_folder(folder):
    return {
        "id": folder.id,
        "name": folder.name,
        "slug": folder.slug,
        "parent_id": folder.parent_id,
        "description": folder.description,
        "created_at": folder.created_at,
        "updated_at": folder.updated_at,
    }


def serialize_usage(usage):
    return {
        "id": usage.id,
        "application": usage.application,
        "model_name": usage.model_name,
        "object_id": usage.object_id,
        "field_name": usage.field_name,
        "usage_context": usage.usage_context,
        "created_at": usage.created_at,
    }


def serialize_asset(asset):
    return {
        "id": asset.id,
        "folder_id": asset.folder_id,
        "folder_name": (
            asset.folder.name
            if asset.folder
            else None
        ),
        "title": asset.title,
        "file_url": file_url(asset.file) or "",
        "original_name": asset.original_name,
        "media_type": asset.media_type,
        "mime_type": asset.mime_type,
        "extension": asset.extension,
        "size": asset.size,
        "width": asset.width,
        "height": asset.height,
        "duration_seconds": asset.duration_seconds,
        "alt_text": asset.alt_text,
        "caption": asset.caption,
        "description": asset.description,
        "tags": asset.tags,
        "checksum": asset.checksum,
        "is_optimized": asset.is_optimized,
        "optimized_file_url": file_url(
            asset.optimized_file
        ),
        "webp_file_url": file_url(asset.webp_file),
        "is_public": asset.is_public,
        "usages": [
            serialize_usage(usage)
            for usage in asset.usages.all()
        ],
        "created_at": asset.created_at,
        "updated_at": asset.updated_at,
    }


def get_folder(folder_id):
    if folder_id is None:
        return None

    folder = MediaFolderRepository.find_by_id(folder_id)

    if folder is None:
        raise ApiHttpError(
            400,
            "Media folder not found.",
            code="invalid_media_folder",
        )

    return folder


def get_asset(asset_id):
    asset = MediaAssetRepository.find_by_id(asset_id)

    if asset is None:
        raise ApiHttpError(
            404,
            "Media asset not found.",
            code="media_asset_not_found",
        )

    return asset


@router.get(
    "/folders",
    response={
        200: list[MediaFolderSchema],
        403: ErrorSchema,
    },
)
@require_permissions("media_library.view_mediafolder")
def list_folders(request):
    return [
        serialize_folder(folder)
        for folder in MediaFolderRepository.queryset()
    ]


@router.post(
    "/folders",
    response={
        201: MediaFolderSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("media_library.add_mediafolder")
def create_folder(
    request,
    payload: MediaFolderCreateSchema,
):
    try:
        folder = MediaLibraryService.create_folder(
            request=request,
            name=payload.name,
            parent=get_folder(payload.parent_id),
            description=payload.description,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="duplicate_media_folder",
        ) from exc

    return 201, serialize_folder(folder)


@router.get(
    "/assets",
    response={
        200: PaginatedResponseSchema[MediaAssetSchema],
        403: ErrorSchema,
    },
)
@require_permissions("media_library.view_mediaasset")
def list_assets(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    media_type: str | None = None,
    folder_id: str | None = None,
    is_public: bool | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        MediaAssetRepository.search(
            search=search,
            media_type=media_type,
            folder_id=folder_id,
            is_public=is_public,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_asset,
    )


@router.post(
    "/assets/upload",
    response={
        201: MediaAssetSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("media_library.add_mediaasset")
def upload_asset(
    request,
    file: File[UploadedFile],
    title: Form[str] = "",
    folder_id: Form[str] = "",
    media_type: Form[str] = "",
    alt_text: Form[str] = "",
    caption: Form[str] = "",
    description: Form[str] = "",
    is_public: Form[bool] = True,
):
    try:
        asset = MediaLibraryService.upload_asset(
            request=request,
            uploaded_file=file,
            title=title,
            folder=get_folder(folder_id or None),
            media_type=media_type or None,
            alt_text=alt_text,
            caption=caption,
            description=description,
            is_public=is_public,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_media_upload",
        ) from exc

    return 201, serialize_asset(asset)


@router.get(
    "/assets/{asset_id}",
    response={
        200: MediaAssetSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("media_library.view_mediaasset")
def asset_detail(request, asset_id: str):
    return serialize_asset(get_asset(asset_id))


@router.put(
    "/assets/{asset_id}",
    response={
        200: MediaAssetSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("media_library.change_mediaasset")
def update_asset(
    request,
    asset_id: str,
    payload: MediaAssetUpdateSchema,
):
    values = payload.dict()
    folder_id = values.pop("folder_id")

    values["folder"] = get_folder(folder_id)

    asset = MediaLibraryService.update_asset(
        request=request,
        asset=get_asset(asset_id),
        values=values,
    )

    refreshed = MediaAssetRepository.queryset().filter(
        pk=asset.pk,
    ).first()

    return serialize_asset(refreshed)


@router.delete(
    "/assets/{asset_id}",
    response={
        200: MessageSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("media_library.delete_mediaasset")
def delete_asset(request, asset_id: str):
    try:
        MediaLibraryService.soft_delete_asset(
            request=request,
            asset=get_asset(asset_id),
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="media_asset_in_use",
        ) from exc

    return {
        "status": "ok",
        "message": "Media asset deleted successfully.",
    }


@router.post(
    "/assets/{asset_id}/usages",
    response={
        201: MediaUsageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("media_library.add_mediausage")
def register_usage(
    request,
    asset_id: str,
    payload: MediaUsageCreateSchema,
):
    usage = MediaLibraryService.register_usage(
        request=request,
        asset=get_asset(asset_id),
        application=payload.application,
        model_name=payload.model_name,
        object_id=payload.object_id,
        field_name=payload.field_name,
        usage_context=payload.usage_context,
    )

    return 201, serialize_usage(usage)
