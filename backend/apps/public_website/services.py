import hashlib
import json
from datetime import timedelta
from decimal import Decimal
from uuid import UUID

from django.db import transaction
from django.utils import timezone

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    PublicSnapshotType,
    PublicWebsiteSnapshot,
)
from .repositories import (
    PublicResourceRepository,
    PublicSnapshotRepository,
    PublicWebsiteRepository,
)


class PublicSerializationService:
    COMMON_FIELDS = (
        "id",
        "slug",
        "title",
        "name",
        "label",
        "reference_code",
        "short_description",
        "description",
        "excerpt",
        "summary",
        "content",
        "status",
        "is_featured",
        "sort_order",
        "published_at",
        "created_at",
        "updated_at",
    )

    @staticmethod
    def normalize(value):
        if isinstance(value, UUID):
            return str(value)

        if isinstance(value, Decimal):
            return str(value)

        if hasattr(value, "isoformat"):
            return value.isoformat()

        if isinstance(value, dict):
            return {
                str(key): (
                    PublicSerializationService
                    .normalize(item)
                )
                for key, item in value.items()
            }

        if isinstance(value, (list, tuple)):
            return [
                PublicSerializationService
                .normalize(item)
                for item in value
            ]

        return value

    @classmethod
    def serialize_service(cls, service):
        try:
            seo = service.seo
        except service._meta.get_field(
            "seo"
        ).related_model.DoesNotExist:
            seo = None

        return {
            "resource_type": "service",
            "id": str(service.id),
            "title": service.title,
            "slug": service.slug,
            "short_description": (
                service.short_description
            ),
            "description": cls.normalize(
                service.description
            ),
            "hero_title": service.hero_title,
            "hero_description": (
                service.hero_description
            ),
            "hero_image_id": (
                str(service.hero_image_id)
                if service.hero_image_id
                else None
            ),
            "status": service.status,
            "published_at": cls.normalize(
                service.published_at
            ),
            "scheduled_for": cls.normalize(
                service.scheduled_for
            ),
            "icon": service.icon,
            "sort_order": service.sort_order,
            "is_featured": service.is_featured,
            "is_active": service.is_active,
            "is_publicly_available": (
                service.is_publicly_available
            ),
            "cta_title": service.cta_title,
            "cta_text": service.cta_text,
            "cta_label": service.cta_label,
            "cta_url": service.cta_url,
            "features": [
                {
                    "id": str(item.id),
                    "title": item.title,
                    "description": item.description,
                    "icon": item.icon,
                    "sort_order": item.sort_order,
                }
                for item in service.features.all()
            ],
            "process_steps": [
                {
                    "id": str(item.id),
                    "title": item.title,
                    "description": item.description,
                    "step_number": item.step_number,
                    "sort_order": item.sort_order,
                }
                for item in service.process_steps.all()
            ],
            "technologies": [
                {
                    "id": str(item.id),
                    "name": item.name,
                    "description": item.description,
                    "logo_id": (
                        str(item.logo_id)
                        if item.logo_id
                        else None
                    ),
                    "sort_order": item.sort_order,
                }
                for item in service.technologies.all()
            ],
            "faqs": [
                {
                    "id": str(item.id),
                    "question": item.question,
                    "answer": item.answer,
                    "sort_order": item.sort_order,
                }
                for item in service.faqs.all()
            ],
            "seo": (
                {
                    "id": str(seo.id),
                    "meta_title": seo.meta_title,
                    "meta_description": (
                        seo.meta_description
                    ),
                    "canonical_url": (
                        seo.canonical_url
                    ),
                    "robots_index": seo.robots_index,
                    "robots_follow": seo.robots_follow,
                    "open_graph_title": (
                        seo.open_graph_title
                    ),
                    "open_graph_description": (
                        seo.open_graph_description
                    ),
                    "open_graph_image_id": (
                        str(seo.open_graph_image_id)
                        if seo.open_graph_image_id
                        else None
                    ),
                    "twitter_title": (
                        seo.twitter_title
                    ),
                    "twitter_description": (
                        seo.twitter_description
                    ),
                    "structured_data": cls.normalize(
                        seo.structured_data
                    ),
                }
                if seo
                else None
            ),
            "created_at": cls.normalize(
                service.created_at
            ),
            "updated_at": cls.normalize(
                service.updated_at
            ),
        }

    @classmethod
    def serialize_insight(cls, article):
        try:
            seo = article.seo
        except Exception:
            seo = None

        return {
            "resource_type": "insight_article",
            "id": str(article.id),
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "content": cls.normalize(article.content),
            "status": article.status,
            "published_at": cls.normalize(
                article.published_at
            ),
            "created_at": cls.normalize(
                article.created_at
            ),
            "updated_at": cls.normalize(
                article.updated_at
            ),
            "is_featured": article.is_featured,
            "reading_time_minutes": (
                article.reading_time_minutes
            ),
            "word_count": article.word_count,
            "view_count": article.view_count,
            "category_id": (
                str(article.category_id)
                if article.category_id
                else None
            ),
            "category_name": (
                article.category.name
                if article.category
                else None
            ),
            "category_slug": (
                article.category.slug
                if article.category
                else None
            ),
            "author_id": (
                article.author_id
            ),
            "author_email": (
                article.author.email
                if article.author
                else None
            ),
            "featured_image_id": (
                str(article.featured_image_id)
                if article.featured_image_id
                else None
            ),
            "tags": [
                {
                    "id": str(item.tag.id),
                    "name": item.tag.name,
                    "slug": item.tag.slug,
                }
                for item in article.article_tags.all()
            ],
            "seo": (
                {
                    "meta_title": seo.meta_title,
                    "meta_description": (
                        seo.meta_description
                    ),
                    "canonical_url": (
                        seo.canonical_url
                    ),
                    "robots_index": (
                        seo.robots_index
                    ),
                    "robots_follow": (
                        seo.robots_follow
                    ),
                    "open_graph_title": (
                        seo.open_graph_title
                    ),
                    "open_graph_description": (
                        seo.open_graph_description
                    ),
                    "open_graph_image_id": (
                        str(seo.open_graph_image_id)
                        if seo.open_graph_image_id
                        else None
                    ),
                    "twitter_title": (
                        seo.twitter_title
                    ),
                    "twitter_description": (
                        seo.twitter_description
                    ),
                    "article_schema": (
                        cls.normalize(
                            seo.article_schema
                        )
                    ),
                    "faq_schema": (
                        cls.normalize(
                            seo.faq_schema
                        )
                    ),
                }
                if seo
                else None
            ),
        }

    @classmethod
    def serialize_testimonial(cls, testimonial):
        return {
            "resource_type": "testimonial",
            "id": str(testimonial.id),
            "author_name": testimonial.author_name,
            "author_position": testimonial.author_position,
            "company_name": testimonial.company_name,
            "content": testimonial.content,
            "short_content": testimonial.short_content,
            "rating": testimonial.rating,
            "source": testimonial.source,
            "source_url": testimonial.source_url,
            "author_image_id": (
                str(testimonial.author_image_id)
                if testimonial.author_image_id
                else None
            ),
            "company_logo_id": (
                str(testimonial.company_logo_id)
                if testimonial.company_logo_id
                else None
            ),
            "client_id": (
                str(testimonial.client_id)
                if testimonial.client_id
                else None
            ),
            "client_name": (
                str(testimonial.client)
                if testimonial.client
                else None
            ),
            "project_id": (
                str(testimonial.project_id)
                if testimonial.project_id
                else None
            ),
            "project_title": (
                testimonial.project.title
                if testimonial.project
                else None
            ),
            "status": testimonial.status,
            "published_at": cls.normalize(
                testimonial.published_at
            ),
            "is_featured": testimonial.is_featured,
            "is_verified": testimonial.is_verified,
            "sort_order": testimonial.sort_order,
            "created_at": cls.normalize(
                testimonial.created_at
            ),
            "updated_at": cls.normalize(
                testimonial.updated_at
            ),
        }

    @classmethod
    def serialize_model(cls, instance):
        fields = {
            field.name
            for field in (
                instance._meta.concrete_fields
            )
        }

        output = {
            "resource_type": (
                instance._meta.model_name
            ),
        }

        for field_name in cls.COMMON_FIELDS:
            if field_name not in fields:
                continue

            value = getattr(
                instance,
                field_name,
                None,
            )

            output[field_name] = (
                cls.normalize(value)
            )

        for field_name in (
            "project_title",
            "job_title",
            "company_name",
            "author_name",
            "client_name",
            "rating",
            "source",
            "application_deadline",
            "employment_type",
            "location",
        ):
            if field_name in fields:
                output[field_name] = cls.normalize(
                    getattr(
                        instance,
                        field_name,
                        None,
                    )
                )

        return output


class PublicWebsiteService:
    @classmethod
    def serialize_setting(cls, setting):
        value = setting.typed_value

        if setting.value_type == "media":
            return (
                str(setting.media_asset_id)
                if setting.media_asset_id
                else None
            )

        return PublicSerializationService.normalize(
            value
        )

    @classmethod
    def build_settings(cls, environment):
        resolved = PublicWebsiteRepository.settings(
            environment
        )

        return {
            key: cls.serialize_setting(setting)
            for key, setting in resolved.items()
        }

    @classmethod
    def build_navigation(cls):
        output = {}

        for location, menus in (
            PublicWebsiteRepository
            .navigation()
            .items()
        ):
            output[location] = []

            for menu in menus:
                items = list(
                    menu.items.filter(
                        is_active=True,
                        visibility="everyone",
                    )
                )

                children_map = {}

                for item in items:
                    children_map.setdefault(
                        item.parent_id,
                        [],
                    ).append(item)

                def serialize_item(
                    item,
                    ancestry=None,
                ):
                    ancestry = ancestry or set()

                    if item.id in ancestry:
                        return None

                    next_ancestry = {
                        *ancestry,
                        item.id,
                    }

                    children = []

                    for child in children_map.get(
                        item.id,
                        [],
                    ):
                        serialized = serialize_item(
                            child,
                            next_ancestry,
                        )

                        if serialized:
                            children.append(
                                serialized
                            )

                    return {
                        "id": str(item.id),
                        "label": item.label,
                        "url": item.resolved_url,
                        "link_type": (
                            item.link_type
                        ),
                        "icon": item.icon,
                        "target_blank": (
                            item.target_blank
                        ),
                        "rel_attribute": (
                            item.rel_attribute
                        ),
                        "is_featured": (
                            item.is_featured
                        ),
                        "sort_order": (
                            item.sort_order
                        ),
                        "children": children,
                    }

                roots = []

                for item in children_map.get(
                    None,
                    [],
                ):
                    serialized = serialize_item(
                        item
                    )

                    if serialized:
                        roots.append(serialized)

                output[location].append(
                    {
                        "id": str(menu.id),
                        "name": menu.name,
                        "slug": menu.slug,
                        "items": roots,
                    }
                )

        return output

    @classmethod
    def build_teams(cls):
        output = []

        for team in (
            PublicWebsiteRepository.public_teams()
        ):
            members = []

            for member in (
                PublicWebsiteRepository
                .team_members(team.id)
            ):
                members.append(
                    {
                        "id": str(member.id),
                        "display_name": (
                            member.display_name
                        ),
                        "job_title": (
                            member.job_title
                        ),
                        "professional_title": (
                            member.professional_title
                        ),
                        "short_bio": (
                            member.short_bio
                        ),
                        "bio": member.bio,
                        "profile_image_id": (
                            str(
                                member.profile_image_id
                            )
                            if member.profile_image_id
                            else None
                        ),
                        "linkedin_url": (
                            member.linkedin_url
                        ),
                        "github_url": (
                            member.github_url
                        ),
                        "portfolio_url": (
                            member.portfolio_url
                        ),
                        "is_leadership": (
                            member.is_leadership
                        ),
                        "is_featured": (
                            member.is_featured
                        ),
                    }
                )

            output.append(
                {
                    "id": str(team.id),
                    "name": team.name,
                    "slug": team.slug,
                    "team_type": team.team_type,
                    "description": (
                        team.description
                    ),
                    "members": members,
                }
            )

        return output

    @classmethod
    def serialize_resources(
        cls,
        resource_name,
        *,
        limit=None,
        featured_only=False,
    ):
        instances = (
            PublicResourceRepository.list_resources(
                resource_name,
                limit=limit,
                featured_only=featured_only,
            )
        )

        if resource_name == "services":
            serializer = (
                PublicSerializationService.serialize_service
            )
        elif resource_name == "insights":
            serializer = (
                PublicSerializationService.serialize_insight
            )
        elif resource_name == "testimonials":
            serializer = (
                PublicSerializationService.serialize_testimonial
            )
        else:
            serializer = (
                PublicSerializationService.serialize_model
            )

        return [
            serializer(instance)
            for instance in instances
        ]

    @classmethod
    def build_bootstrap(cls, environment):
        return {
            "environment": environment,
            "generated_at": (
                timezone.now().isoformat()
            ),
            "settings": cls.build_settings(
                environment
            ),
            "navigation": cls.build_navigation(),
        }

    @classmethod
    def build_homepage(cls, environment):
        return {
            "environment": environment,
            "generated_at": (
                timezone.now().isoformat()
            ),
            "settings": cls.build_settings(
                environment
            ),
            "navigation": cls.build_navigation(),
            "featured_services": (
                cls.serialize_resources(
                    "services",
                    limit=12,
                    featured_only=True,
                )
            ),
            "featured_packages": (
                cls.serialize_resources(
                    "packages",
                    limit=12,
                    featured_only=True,
                )
            ),
            "featured_industries": (
                cls.serialize_resources(
                    "industries",
                    limit=12,
                    featured_only=True,
                )
            ),
            "latest_insights": (
                cls.serialize_resources(
                    "insights",
                    limit=6,
                )
            ),
            "featured_case_studies": (
                cls.serialize_resources(
                    "case_studies",
                    limit=6,
                    featured_only=True,
                )
            ),
            "featured_testimonials": (
                cls.serialize_resources(
                    "testimonials",
                    limit=12,
                    featured_only=True,
                )
            ),
            "teams": cls.build_teams(),
        }

    @classmethod
    def build_catalog(cls, environment):
        return {
            "environment": environment,
            "generated_at": (
                timezone.now().isoformat()
            ),
            "services": cls.serialize_resources(
                "services"
            ),
            "packages": cls.serialize_resources(
                "packages"
            ),
            "industries": cls.serialize_resources(
                "industries"
            ),
        }

    @classmethod
    def build_content(cls, environment):
        return {
            "environment": environment,
            "generated_at": (
                timezone.now().isoformat()
            ),
            "insights": cls.serialize_resources(
                "insights"
            ),
            "case_studies": (
                cls.serialize_resources(
                    "case_studies"
                )
            ),
            "testimonials": (
                cls.serialize_resources(
                    "testimonials"
                )
            ),
            "career_listings": (
                cls.serialize_resources(
                    "career_listings"
                )
            ),
        }


class PublicSnapshotService:
    BUILDERS = {
        PublicSnapshotType.BOOTSTRAP: (
            PublicWebsiteService.build_bootstrap
        ),
        PublicSnapshotType.HOMEPAGE: (
            PublicWebsiteService.build_homepage
        ),
        PublicSnapshotType.CATALOG: (
            PublicWebsiteService.build_catalog
        ),
        PublicSnapshotType.CONTENT: (
            PublicWebsiteService.build_content
        ),
    }

    @staticmethod
    def checksum(payload):
        encoded = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")

        return hashlib.sha256(encoded).hexdigest()

    @classmethod
    @transaction.atomic
    def generate(
        cls,
        *,
        request,
        snapshot_type,
        environment,
        ttl_minutes=30,
    ):
        builder = cls.BUILDERS.get(
            snapshot_type
        )

        if builder is None:
            raise ValueError(
                "Unsupported public snapshot type."
            )

        payload = builder(environment)

        PublicWebsiteSnapshot.objects.filter(
            snapshot_type=snapshot_type,
            environment=environment,
            is_active=True,
        ).update(
            is_active=False,
        )

        snapshot = PublicWebsiteSnapshot.objects.create(
            snapshot_type=snapshot_type,
            environment=environment,
            version=(
                PublicSnapshotRepository.next_version(
                    snapshot_type,
                    environment,
                )
            ),
            payload=payload,
            generated_at=timezone.now(),
            expires_at=(
                timezone.now()
                + timedelta(
                    minutes=ttl_minutes
                )
            ),
            checksum=cls.checksum(payload),
            is_active=True,
        )

        if request is not None:
            log_audit_event(
                request=request,
                actor=request.auth,
                event_type=(
                    AuditEventType.RECORD_CREATED
                ),
                module="public_website",
                message=(
                    "Public website snapshot generated."
                ),
                target_type=(
                    "public_website."
                    "PublicWebsiteSnapshot"
                ),
                target_id=str(snapshot.pk),
                metadata={
                    "snapshot_type": (
                        snapshot.snapshot_type
                    ),
                    "environment": (
                        snapshot.environment
                    ),
                    "version": snapshot.version,
                },
            )

            log_activity(
                request=request,
                actor=request.auth,
                action=(
                    "generate_public_snapshot"
                ),
                module="public_website",
                description=(
                    f"Generated "
                    f"{snapshot.snapshot_type} "
                    f"snapshot v{snapshot.version}."
                ),
                entity_type=(
                    "public_website."
                    "PublicWebsiteSnapshot"
                ),
                entity_id=str(snapshot.pk),
            )

        return snapshot


    @classmethod
    @transaction.atomic
    def invalidate(
        cls,
        *,
        request,
        snapshot_type=None,
        environment=None,
    ):
        queryset = PublicWebsiteSnapshot.objects.filter(
            is_active=True,
        )

        if snapshot_type:
            queryset = queryset.filter(
                snapshot_type=snapshot_type,
            )

        if environment:
            queryset = queryset.filter(
                environment=environment,
            )

        snapshot_ids = list(
            queryset.values_list(
                "id",
                flat=True,
            )
        )

        invalidated_count = queryset.update(
            is_active=False,
        )

        if request is not None:
            log_audit_event(
                request=request,
                actor=request.auth,
                event_type=(
                    AuditEventType.RECORD_UPDATED
                ),
                module="public_website",
                message=(
                    "Public website snapshots invalidated."
                ),
                target_type=(
                    "public_website."
                    "PublicWebsiteSnapshot"
                ),
                target_id="bulk",
                metadata={
                    "snapshot_type": snapshot_type,
                    "environment": environment,
                    "snapshot_ids": [
                        str(snapshot_id)
                        for snapshot_id in snapshot_ids
                    ],
                    "invalidated_count": (
                        invalidated_count
                    ),
                },
            )

            log_activity(
                request=request,
                actor=request.auth,
                action=(
                    "invalidate_public_snapshots"
                ),
                module="public_website",
                description=(
                    f"Invalidated {invalidated_count} "
                    "public website snapshots."
                ),
                entity_type=(
                    "public_website."
                    "PublicWebsiteSnapshot"
                ),
                entity_id="bulk",
            )

        return invalidated_count

    @classmethod
    @transaction.atomic
    def refresh_all(
        cls,
        *,
        request,
        environment,
        ttl_minutes=30,
    ):
        snapshots = []

        for snapshot_type in (
            PublicSnapshotType.BOOTSTRAP,
            PublicSnapshotType.HOMEPAGE,
            PublicSnapshotType.CATALOG,
            PublicSnapshotType.CONTENT,
        ):
            snapshots.append(
                cls.generate(
                    request=request,
                    snapshot_type=snapshot_type,
                    environment=environment,
                    ttl_minutes=ttl_minutes,
                )
            )

        return snapshots
