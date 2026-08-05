import math
import re
from typing import Any

from django.db import transaction
from django.utils import timezone
from django.utils.html import strip_tags

from apps.activity.services import log_activity
from apps.audit.models import AuditEventType
from apps.audit.services import log_audit_event

from .models import (
    ArticleStatus,
    InsightArticle,
    InsightArticleSeo,
    InsightArticleTag,
    InsightInternalLink,
    InsightPublishingEvent,
    InsightPublishingEventType,
    InsightRevision,
)


class InsightService:
    @staticmethod
    def plain_text(content: Any) -> str:
        if isinstance(content, str):
            return strip_tags(content)

        if isinstance(content, dict):
            return " ".join(
                InsightService.plain_text(value)
                for value in content.values()
            )

        if isinstance(content, list):
            return " ".join(
                InsightService.plain_text(value)
                for value in content
            )

        return str(content or "")

    @staticmethod
    def calculate_content_metrics(content):
        text = InsightService.plain_text(content)
        words = re.findall(r"\b[\w'-]+\b", text)
        word_count = len(words)

        return {
            "word_count": word_count,
            "reading_time_minutes": max(
                1,
                math.ceil(word_count / 220),
            ),
        }

    @staticmethod
    def create_event(
        *,
        article,
        event_type,
        description,
        actor=None,
        metadata=None,
    ):
        return InsightPublishingEvent.objects.create(
            article=article,
            event_type=event_type,
            description=description,
            metadata=metadata or {},
            created_by=actor,
            updated_by=actor,
        )

    @staticmethod
    def snapshot(article):
        try:
            seo = article.seo
        except InsightArticleSeo.DoesNotExist:
            seo = None

        return {
            "title": article.title,
            "slug": article.slug,
            "excerpt": article.excerpt,
            "content": article.content,
            "category_id": (
                str(article.category_id)
                if article.category_id
                else None
            ),
            "author_id": article.author_id,
            "featured_image_id": (
                str(article.featured_image_id)
                if article.featured_image_id
                else None
            ),
            "status": article.status,
            "is_featured": article.is_featured,
            "is_active": article.is_active,
            "allow_comments": article.allow_comments,
            "tag_ids": [
                str(item.tag_id)
                for item in article.article_tags.all()
            ],
            "related_article_ids": [
                str(item.pk)
                for item in article.related_articles.all()
            ],
            "seo": (
                {
                    "meta_title": seo.meta_title,
                    "meta_description": seo.meta_description,
                    "canonical_url": seo.canonical_url,
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
                    "twitter_title": seo.twitter_title,
                    "twitter_description": (
                        seo.twitter_description
                    ),
                    "article_schema": seo.article_schema,
                    "faq_schema": seo.faq_schema,
                }
                if seo
                else {}
            ),
        }

    @staticmethod
    def create_revision(
        *,
        article,
        actor,
        change_summary="",
    ):
        latest = (
            InsightRevision.all_objects.filter(
                article=article,
            )
            .order_by("-revision_number")
            .values_list("revision_number", flat=True)
            .first()
        )

        revision_number = (latest or 0) + 1

        revision = InsightRevision.objects.create(
            article=article,
            revision_number=revision_number,
            snapshot=InsightService.snapshot(article),
            change_summary=change_summary,
            created_by=actor,
            updated_by=actor,
        )

        article.current_revision_number = (
            revision_number
        )
        article.save(
            update_fields=[
                "current_revision_number",
                "updated_at",
            ],
        )

        return revision

    @staticmethod
    def replace_tags(*, request, article, tags):
        article.article_tags.all().delete()

        for tag in tags:
            InsightArticleTag.objects.create(
                article=article,
                tag=tag,
                created_by=request.auth,
                updated_by=request.auth,
            )

    @staticmethod
    def replace_internal_links(
        *,
        request,
        article,
        internal_links,
    ):
        article.outgoing_internal_links.all().delete()

        for values in internal_links:
            InsightInternalLink.objects.create(
                source_article=article,
                created_by=request.auth,
                updated_by=request.auth,
                **values,
            )

    @staticmethod
    @transaction.atomic
    def create_article(
        *,
        request,
        values,
        tags,
        related_articles,
        internal_links,
        seo_values,
    ):
        metrics = InsightService.calculate_content_metrics(
            values.get("content", {})
        )

        article = InsightArticle.objects.create(
            **values,
            **metrics,
            created_by=request.auth,
            updated_by=request.auth,
        )

        InsightArticleSeo.objects.create(
            article=article,
            created_by=request.auth,
            updated_by=request.auth,
            **seo_values,
        )

        InsightService.replace_tags(
            request=request,
            article=article,
            tags=tags,
        )

        article.related_articles.set(related_articles)

        InsightService.replace_internal_links(
            request=request,
            article=article,
            internal_links=internal_links,
        )

        InsightService.create_revision(
            article=article,
            actor=request.auth,
            change_summary="Initial article revision.",
        )

        InsightService.create_event(
            article=article,
            event_type=InsightPublishingEventType.CREATED,
            description="Insight article created.",
            actor=request.auth,
        )

        log_activity(
            request=request,
            actor=request.auth,
            action="insight_created",
            module="insights",
            description="Insight article created.",
            entity_type="insights.InsightArticle",
            entity_id=str(article.pk),
        )

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_CREATED,
            module="insights",
            message="Insight article created.",
            target_type="insights.InsightArticle",
            target_id=str(article.pk),
            after={
                "title": article.title,
                "slug": article.slug,
                "status": article.status,
            },
        )

        return article

    @staticmethod
    @transaction.atomic
    def update_article(
        *,
        request,
        article,
        values,
        tags,
        related_articles,
        internal_links,
        seo_values,
        change_summary="",
    ):
        for field, value in values.items():
            setattr(article, field, value)

        metrics = InsightService.calculate_content_metrics(
            article.content
        )

        article.word_count = metrics["word_count"]
        article.reading_time_minutes = (
            metrics["reading_time_minutes"]
        )
        article.updated_by = request.auth
        article.save()

        seo, _ = InsightArticleSeo.objects.get_or_create(
            article=article,
            defaults={
                "created_by": request.auth,
                "updated_by": request.auth,
            },
        )

        for field, value in seo_values.items():
            setattr(seo, field, value)

        seo.updated_by = request.auth
        seo.save()

        InsightService.replace_tags(
            request=request,
            article=article,
            tags=tags,
        )

        article.related_articles.set(related_articles)

        InsightService.replace_internal_links(
            request=request,
            article=article,
            internal_links=internal_links,
        )

        InsightService.create_revision(
            article=article,
            actor=request.auth,
            change_summary=change_summary,
        )

        InsightService.create_event(
            article=article,
            event_type=InsightPublishingEventType.UPDATED,
            description="Insight article updated.",
            actor=request.auth,
        )

        return article

    @staticmethod
    @transaction.atomic
    def publish_article(*, request, article):
        article.status = ArticleStatus.PUBLISHED
        article.published_at = timezone.now()
        article.scheduled_for = None
        article.updated_by = request.auth
        article.save()

        InsightService.create_revision(
            article=article,
            actor=request.auth,
            change_summary="Article published.",
        )

        InsightService.create_event(
            article=article,
            event_type=InsightPublishingEventType.PUBLISHED,
            description="Insight article published.",
            actor=request.auth,
        )

        return article

    @staticmethod
    @transaction.atomic
    def schedule_article(
        *,
        request,
        article,
        scheduled_for,
    ):
        if scheduled_for <= timezone.now():
            raise ValueError(
                "Scheduled publication time must be in the future."
            )

        article.status = ArticleStatus.SCHEDULED
        article.scheduled_for = scheduled_for
        article.published_at = None
        article.updated_by = request.auth
        article.save()

        InsightService.create_event(
            article=article,
            event_type=InsightPublishingEventType.SCHEDULED,
            description="Article publication scheduled.",
            actor=request.auth,
            metadata={
                "scheduled_for": scheduled_for.isoformat(),
            },
        )

        return article

    @staticmethod
    @transaction.atomic
    def process_scheduled_articles():
        articles = list(
            InsightArticle.objects.filter(
                is_active=True,
                status=ArticleStatus.SCHEDULED,
                scheduled_for__lte=timezone.now(),
            )
        )

        for article in articles:
            article.status = ArticleStatus.PUBLISHED
            article.published_at = article.scheduled_for
            article.scheduled_for = None
            article.save()

            InsightService.create_event(
                article=article,
                event_type=(
                    InsightPublishingEventType.PUBLISHED
                ),
                description=(
                    "Scheduled article automatically published."
                ),
            )

        return len(articles)

    @staticmethod
    @transaction.atomic
    def soft_delete(*, request, article):
        article_id = str(article.pk)
        article.delete()

        log_audit_event(
            request=request,
            actor=request.auth,
            event_type=AuditEventType.RECORD_DELETED,
            module="insights",
            message="Insight article soft deleted.",
            target_type="insights.InsightArticle",
            target_id=article_id,
            after={"is_deleted": True},
        )
