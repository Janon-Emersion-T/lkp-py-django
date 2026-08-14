from django.apps import apps
from django.db.models import Q
from django.utils import timezone

from apps.navigation.repositories import (
    PublicNavigationRepository,
)
from apps.team_management.repositories import (
    PublicTeamRepository,
)
from apps.website_settings.models import (
    SettingEnvironment,
)
from apps.website_settings.repositories import (
    PublicWebsiteSettingRepository,
)

from .models import PublicWebsiteSnapshot


MODEL_CANDIDATES = {
    "services": [
        ("services_catalog", "Service"),
    ],
    "packages": [
        ("packages_catalog", "Package"),
    ],
    "industries": [
        ("industries", "Industry"),
    ],
    "insights": [
        ("insights", "InsightPost"),
        ("insights", "InsightArticle"),
        ("insights", "Article"),
        ("insights", "Post"),
    ],
    "case_studies": [
        ("case_studies", "CaseStudy"),
    ],
    "testimonials": [
        ("testimonials", "Testimonial"),
    ],
    "career_listings": [
        ("careers", "JobListing"),
    ],
}


class PublicModelResolver:
    @staticmethod
    def resolve(resource_name):
        candidates = MODEL_CANDIDATES.get(
            resource_name,
            [],
        )

        for app_label, model_name in candidates:
            try:
                return apps.get_model(
                    app_label,
                    model_name,
                )
            except LookupError:
                continue

        return None


class PublicResourceRepository:
    @staticmethod
    def model_fields(model):
        return {
            field.name
            for field in model._meta.get_fields()
        }

    @classmethod
    def public_queryset(cls, resource_name):
        model = PublicModelResolver.resolve(
            resource_name
        )

        if model is None:
            return None

        fields = cls.model_fields(model)
        queryset = model.objects.all()

        if "is_active" in fields:
            queryset = queryset.filter(
                is_active=True,
            )

        if "is_public" in fields:
            queryset = queryset.filter(
                is_public=True,
            )

        if "is_published" in fields:
            queryset = queryset.filter(
                is_published=True,
            )

        if "status" in fields:
            status_values = {
                value
                for value, _ in (
                    model._meta.get_field(
                        "status"
                    ).choices
                    or []
                )
            }

            preferred_statuses = [
                status
                for status in (
                    "published",
                    "active",
                    "open",
                )
                if status in status_values
            ]

            if preferred_statuses:
                queryset = queryset.filter(
                    status__in=preferred_statuses,
                )

        if "published_at" in fields:
            queryset = queryset.filter(
                Q(published_at__isnull=True)
                | Q(published_at__lte=timezone.now())
            )

        if "scheduled_for" in fields:
            queryset = queryset.filter(
                Q(scheduled_for__isnull=True)
                | Q(scheduled_for__lte=timezone.now())
            )

        if "application_deadline" in fields:
            queryset = queryset.filter(
                Q(application_deadline__isnull=True)
                | Q(
                    application_deadline__gte=(
                        timezone.now()
                    )
                )
            )

        return queryset

    @classmethod
    def list_resources(
        cls,
        resource_name,
        *,
        limit=None,
        featured_only=False,
    ):
        queryset = cls.public_queryset(
            resource_name
        )

        if queryset is None:
            return []

        if resource_name == "services":
            queryset = queryset.select_related(
                "seo",
            ).prefetch_related(
                "features",
                "process_steps",
                "technologies",
                "faqs",
            )

        if resource_name == "insights":
            queryset = queryset.select_related(
                "category",
                "author",
                "featured_image",
                "seo",
            ).prefetch_related(
                "article_tags__tag",
            )

        fields = cls.model_fields(
            queryset.model
        )

        if (
            featured_only
            and "is_featured" in fields
        ):
            queryset = queryset.filter(
                is_featured=True,
            )

        ordering = []

        if "sort_order" in fields:
            ordering.append("sort_order")

        if "published_at" in fields:
            ordering.append("-published_at")
        elif "created_at" in fields:
            ordering.append("-created_at")

        if ordering:
            queryset = queryset.order_by(
                *ordering
            )

        if limit is not None:
            queryset = queryset[:limit]

        return list(queryset)


class PublicWebsiteRepository:
    @staticmethod
    def settings(environment):
        return (
            PublicWebsiteSettingRepository
            .values_for_environment(environment)
        )

    @staticmethod
    def navigation():
        locations = (
            "header_primary",
            "header_secondary",
            "footer_primary",
            "footer_secondary",
            "footer_legal",
            "mobile",
        )

        return {
            location: list(
                PublicNavigationRepository
                .menus_by_location(location)
            )
            for location in locations
        }

    @staticmethod
    def public_teams():
        return list(PublicTeamRepository.teams())

    @staticmethod
    def team_members(team_id):
        return list(
            PublicTeamRepository.members_for_team(
                team_id
            )
        )


class PublicSnapshotRepository:
    @staticmethod
    def queryset():
        return PublicWebsiteSnapshot.objects.all()

    @classmethod
    def latest(
        cls,
        snapshot_type,
        environment,
    ):
        return cls.queryset().filter(
            snapshot_type=snapshot_type,
            environment=environment,
            is_active=True,
        ).filter(
            Q(expires_at__isnull=True)
            | Q(expires_at__gt=timezone.now())
        ).order_by(
            "-version",
            "-generated_at",
        ).first()

    @classmethod
    def next_version(
        cls,
        snapshot_type,
        environment,
    ):
        latest = cls.queryset().filter(
            snapshot_type=snapshot_type,
            environment=environment,
        ).order_by(
            "-version",
        ).first()

        return (
            latest.version + 1
            if latest
            else 1
        )


def normalize_environment(environment):
    valid = {
        choice
        for choice, _ in (
            SettingEnvironment.choices
        )
    }

    if environment not in valid:
        raise ValueError(
            "Invalid public website environment."
        )

    return environment
