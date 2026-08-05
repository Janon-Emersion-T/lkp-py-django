import hashlib
import mimetypes
from pathlib import Path
from typing import Any

from django.db import transaction
from django.utils.text import slugify

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    MediaAsset,
    MediaFolder,
    MediaType,
    MediaUsage,
)


class MediaLibraryService:
    @staticmethod
    def detect_media_type(
        *,
        filename: str,
        mime_type: str,
    ) -> str:
        extension = Path(filename).suffix.lower()

        if mime_type.startswith("image/"):
            if "logo" in filename.lower():
                return MediaType.LOGO

            if extension in (
                ".ico",
                ".svg",
            ):
                return MediaType.ICON

            return MediaType.IMAGE

        if mime_type.startswith("video/"):
            return MediaType.VIDEO

        if mime_type == "application/pdf":
            return MediaType.PDF

        if mime_type.startswith(
            "application/"
        ) or mime_type.startswith("text/"):
            return MediaType.DOCUMENT

        return MediaType.OTHER

    @staticmethod
    def calculate_checksum(uploaded_file) -> str:
        digest = hashlib.sha256()

        for chunk in uploaded_file.chunks():
            digest.update(chunk)

        uploaded_file.seek(0)

        return digest.hexdigest()

    @staticmethod
    @transaction.atomic
    def create_folder(
        *,
        request,
        name: str,
        parent=None,
        description: str = "",
    ) -> MediaFolder:
        slug = slugify(name)

        if MediaFolder.all_objects.filter(
            parent=parent,
            slug=slug,
            is_deleted=False,
        ).exists():
            raise ValueError(
                "A folder with this name already exists here."
            )

        folder = MediaFolder.objects.create(
            name=name.strip(),
            slug=slug,
            parent=parent,
            description=description,
            created_by=request.auth,
            updated_by=request.auth,
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="media_library",
            message="Media folder created.",
            target_type="media_library.MediaFolder",
            target_id=str(folder.pk),
            after={
                "name": folder.name,
                "slug": folder.slug,
                "parent_id": (
                    str(folder.parent_id)
                    if folder.parent_id
                    else None
                ),
            },
        )

        return folder

    @staticmethod
    @transaction.atomic
    def upload_asset(
        *,
        request,
        uploaded_file,
        title: str = "",
        folder=None,
        media_type: str | None = None,
        alt_text: str = "",
        caption: str = "",
        description: str = "",
        tags: list[str] | None = None,
        is_public: bool = True,
    ) -> MediaAsset:
        original_name = uploaded_file.name
        guessed_mime, _ = mimetypes.guess_type(
            original_name
        )

        mime_type = (
            getattr(uploaded_file, "content_type", "")
            or guessed_mime
            or "application/octet-stream"
        )

        resolved_media_type = (
            media_type
            or MediaLibraryService.detect_media_type(
                filename=original_name,
                mime_type=mime_type,
            )
        )

        checksum = (
            MediaLibraryService.calculate_checksum(
                uploaded_file
            )
        )

        duplicate = MediaAsset.objects.filter(
            checksum=checksum,
        ).first()

        if duplicate is not None:
            raise ValueError(
                "This file already exists in the media library."
            )

        asset = MediaAsset.objects.create(
            folder=folder,
            title=title.strip() or Path(
                original_name
            ).stem,
            file=uploaded_file,
            original_name=original_name,
            media_type=resolved_media_type,
            mime_type=mime_type,
            extension=Path(
                original_name
            ).suffix.lower().lstrip("."),
            size=getattr(uploaded_file, "size", 0),
            alt_text=alt_text,
            caption=caption,
            description=description,
            tags=tags or [],
            checksum=checksum,
            is_public=is_public,
            uploaded_by=request.auth,
            created_by=request.auth,
            updated_by=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="media_asset_uploaded",
            module="media_library",
            description="Media asset uploaded.",
            entity_type="media_library.MediaAsset",
            entity_id=str(asset.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="media_library",
            message="Media asset uploaded.",
            target_type="media_library.MediaAsset",
            target_id=str(asset.pk),
            after={
                "title": asset.title,
                "original_name": asset.original_name,
                "media_type": asset.media_type,
                "mime_type": asset.mime_type,
                "size": asset.size,
                "checksum": asset.checksum,
            },
        )

        return asset

    @staticmethod
    @transaction.atomic
    def update_asset(
        *,
        request,
        asset: MediaAsset,
        values: dict[str, Any],
    ) -> MediaAsset:
        before = {
            "title": asset.title,
            "folder_id": (
                str(asset.folder_id)
                if asset.folder_id
                else None
            ),
            "alt_text": asset.alt_text,
            "is_public": asset.is_public,
            "tags": asset.tags,
        }

        for field, value in values.items():
            setattr(asset, field, value)

        asset.updated_by = request.auth
        asset.save()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_UPDATED,
            module="media_library",
            message="Media asset updated.",
            target_type="media_library.MediaAsset",
            target_id=str(asset.pk),
            before=before,
            after={
                "title": asset.title,
                "folder_id": (
                    str(asset.folder_id)
                    if asset.folder_id
                    else None
                ),
                "alt_text": asset.alt_text,
                "is_public": asset.is_public,
                "tags": asset.tags,
            },
        )

        return asset

    @staticmethod
    @transaction.atomic
    def register_usage(
        *,
        request,
        asset: MediaAsset,
        application: str,
        model_name: str,
        object_id: str,
        field_name: str = "",
        usage_context: str = "",
    ) -> MediaUsage:
        usage = MediaUsage.all_objects.filter(
            asset=asset,
            application=application,
            model_name=model_name,
            object_id=object_id,
            field_name=field_name,
        ).first()

        if usage is None:
            usage = MediaUsage.objects.create(
                asset=asset,
                application=application,
                model_name=model_name,
                object_id=object_id,
                field_name=field_name,
                usage_context=usage_context,
                created_by=request.auth,
                updated_by=request.auth,
            )
        else:
            usage.usage_context = usage_context
            usage.is_deleted = False
            usage.deleted_at = None
            usage.updated_by = request.auth
            usage.save()

        return usage

    @staticmethod
    @transaction.atomic
    def soft_delete_asset(
        *,
        request,
        asset: MediaAsset,
    ) -> None:
        if asset.usages.exists():
            raise ValueError(
                "This media asset is currently in use."
            )

        asset_id = str(asset.pk)
        asset.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="media_library",
            message="Media asset soft deleted.",
            target_type="media_library.MediaAsset",
            target_id=asset_id,
            after={
                "is_deleted": True,
            },
        )
