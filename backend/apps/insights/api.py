from django.contrib.auth import get_user_model
from django.utils.text import slugify
from ninja import Router

from apps.api.auth import jwt_auth
from apps.api.common_schemas import (
    ErrorSchema,
    MessageSchema,
)
from apps.api.exceptions import ApiHttpError
from apps.api.pagination_schemas import (
    PaginatedResponseSchema,
)
from apps.api.responses import paginated_response
from apps.common.pagination import paginate_queryset
from apps.media_library.models import MediaAsset
from apps.rbac.services import require_permissions

from .models import (
    InsightArticle,
    InsightArticleSeo,
    InsightCategory,
    InsightTag,
)
from .repositories import InsightArticleRepository
from .schemas import (
    CategoryCreateSchema,
    CategorySchema,
    InsightArticleCreateSchema,
    InsightArticleSchema,
    InsightArticleUpdateSchema,
    InsightScheduleSchema,
    TagCreateSchema,
    TagSchema,
)
from .services import InsightService


User = get_user_model()

router = Router(
    tags=["Insights"],
    auth=jwt_auth,
)


def resolve_category(category_id):
    if category_id is None:
        return None

    category = InsightCategory.objects.filter(
        pk=category_id,
    ).first()

    if category is None:
        raise ApiHttpError(
            400,
            "Insight category not found.",
            code="invalid_insight_category",
        )

    return category


def resolve_tags(tag_ids):
    tags = list(
        InsightTag.objects.filter(pk__in=tag_ids)
    )

    if len(tags) != len(set(tag_ids)):
        raise ApiHttpError(
            400,
            "One or more insight tags were not found.",
            code="invalid_insight_tags",
        )

    return tags


def resolve_user(user_id):
    if user_id is None:
        return None

    user = User.objects.filter(pk=user_id).first()

    if user is None:
        raise ApiHttpError(
            400,
            "Article author not found.",
            code="invalid_article_author",
        )

    return user


def resolve_media(asset_id):
    if asset_id is None:
        return None

    asset = MediaAsset.objects.filter(pk=asset_id).first()

    if asset is None:
        raise ApiHttpError(
            400,
            "Media asset not found.",
            code="invalid_media_asset",
        )

    return asset


def resolve_related_articles(
    article_ids,
    *,
    exclude_article=None,
):
    queryset = InsightArticle.objects.filter(
        pk__in=article_ids,
    )

    if exclude_article is not None:
        queryset = queryset.exclude(
            pk=exclude_article.pk,
        )

    articles = list(queryset)

    expected = set(article_ids)

    if exclude_article is not None:
        expected.discard(exclude_article.pk)

    if len(articles) != len(expected):
        raise ApiHttpError(
            400,
            "One or more related articles were not found.",
            code="invalid_related_articles",
        )

    return articles


def resolve_internal_links(
    links,
    *,
    source_article=None,
):
    resolved = []

    for item in links:
        values = item.dict()
        target_id = values.pop("target_article_id")

        target = InsightArticle.objects.filter(
            pk=target_id,
        ).first()

        if target is None:
            raise ApiHttpError(
                400,
                "Internal-link article not found.",
                code="invalid_internal_link",
            )

        if (
            source_article is not None
            and target.pk == source_article.pk
        ):
            raise ApiHttpError(
                400,
                "An article cannot link to itself.",
                code="self_internal_link",
            )

        values["target_article"] = target
        resolved.append(values)

    return resolved


def get_article(article_id):
    article = InsightArticleRepository.find_by_id(
        article_id
    )

    if article is None:
        raise ApiHttpError(
            404,
            "Insight article not found.",
            code="insight_article_not_found",
        )

    return article


def refresh_article(article):
    refreshed = (
        InsightArticleRepository.queryset()
        .filter(pk=article.pk)
        .first()
    )

    if refreshed is None:
        raise ApiHttpError(
            404,
            "Insight article not found.",
            code="insight_article_not_found",
        )

    return refreshed


def serialize_category(category):
    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "parent_id": category.parent_id,
        "is_active": category.is_active,
        "sort_order": category.sort_order,
        "created_at": category.created_at,
        "updated_at": category.updated_at,
    }


def serialize_tag(tag):
    return {
        "id": tag.id,
        "name": tag.name,
        "slug": tag.slug,
        "description": tag.description,
        "is_active": tag.is_active,
        "created_at": tag.created_at,
        "updated_at": tag.updated_at,
    }


def serialize_article(article):
    try:
        seo = article.seo
    except InsightArticleSeo.DoesNotExist:
        seo = None

    return {
        "id": article.id,
        "title": article.title,
        "slug": article.slug,
        "excerpt": article.excerpt,
        "content": article.content,
        "category_id": article.category_id,
        "category_name": (
            article.category.name
            if article.category
            else None
        ),
        "author_id": article.author_id,
        "author_email": (
            article.author.email
            if article.author
            else None
        ),
        "featured_image_id": (
            article.featured_image_id
        ),
        "status": article.status,
        "published_at": article.published_at,
        "scheduled_for": article.scheduled_for,
        "reading_time_minutes": (
            article.reading_time_minutes
        ),
        "word_count": article.word_count,
        "view_count": article.view_count,
        "is_featured": article.is_featured,
        "is_active": article.is_active,
        "allow_comments": article.allow_comments,
        "is_publicly_available": (
            article.is_publicly_available
        ),
        "current_revision_number": (
            article.current_revision_number
        ),
        "tags": [
            {
                "id": item.tag.id,
                "name": item.tag.name,
                "slug": item.tag.slug,
            }
            for item in article.article_tags.all()
        ],
        "related_articles": [
            {
                "id": related.id,
                "title": related.title,
                "slug": related.slug,
            }
            for related in article.related_articles.all()
        ],
        "internal_links": [
            {
                "id": link.id,
                "target_article_id": (
                    link.target_article_id
                ),
                "target_article_title": (
                    link.target_article.title
                ),
                "anchor_text": link.anchor_text,
                "context": link.context,
                "is_active": link.is_active,
            }
            for link in (
                article.outgoing_internal_links.all()
            )
        ],
        "seo": (
            {
                "id": seo.id,
                "meta_title": seo.meta_title,
                "meta_description": (
                    seo.meta_description
                ),
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
                    seo.open_graph_image_id
                ),
                "twitter_title": seo.twitter_title,
                "twitter_description": (
                    seo.twitter_description
                ),
                "article_schema": seo.article_schema,
                "faq_schema": seo.faq_schema,
            }
            if seo
            else None
        ),
        "revisions": [
            {
                "id": revision.id,
                "revision_number": (
                    revision.revision_number
                ),
                "snapshot": revision.snapshot,
                "change_summary": (
                    revision.change_summary
                ),
                "created_at": revision.created_at,
            }
            for revision in article.revisions.all()
        ],
        "publishing_events": [
            {
                "id": event.id,
                "event_type": event.event_type,
                "description": event.description,
                "metadata": event.metadata,
                "created_at": event.created_at,
            }
            for event in article.publishing_events.all()
        ],
        "created_at": article.created_at,
        "updated_at": article.updated_at,
    }


def payload_parts(payload, *, article=None):
    raw = payload.dict()

    tags = resolve_tags(payload.tag_ids)

    related_articles = resolve_related_articles(
        payload.related_article_ids,
        exclude_article=article,
    )

    internal_links = resolve_internal_links(
        payload.internal_links,
        source_article=article,
    )

    seo = payload.seo.dict()
    og_image_id = seo.pop("open_graph_image_id")
    seo["open_graph_image"] = resolve_media(
        og_image_id
    )

    values = {
        key: value
        for key, value in raw.items()
        if key not in (
            "tag_ids",
            "related_article_ids",
            "internal_links",
            "seo",
            "change_summary",
            "category_id",
            "author_id",
            "featured_image_id",
        )
    }

    values["slug"] = slugify(payload.slug)
    values["category"] = resolve_category(
        payload.category_id
    )
    values["author"] = resolve_user(
        payload.author_id
    )
    values["featured_image"] = resolve_media(
        payload.featured_image_id
    )

    return (
        values,
        tags,
        related_articles,
        internal_links,
        seo,
    )


@router.get(
    "/categories",
    response={
        200: list[CategorySchema],
        403: ErrorSchema,
    },
)
@require_permissions("insights.view_insightcategory")
def list_categories(request):
    return [
        serialize_category(category)
        for category in InsightCategory.objects.all()
    ]


@router.post(
    "/categories",
    response={
        201: CategorySchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("insights.add_insightcategory")
def create_category(
    request,
    payload: CategoryCreateSchema,
):
    normalized_slug = slugify(payload.slug)

    if InsightCategory.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Category slug already exists.",
            code="duplicate_insight_category",
        )

    parent = resolve_category(payload.parent_id)

    category = InsightCategory.objects.create(
        name=payload.name,
        slug=normalized_slug,
        description=payload.description,
        parent=parent,
        is_active=payload.is_active,
        sort_order=payload.sort_order,
        created_by=request.auth,
        updated_by=request.auth,
    )

    return 201, serialize_category(category)


@router.get(
    "/tags",
    response={
        200: list[TagSchema],
        403: ErrorSchema,
    },
)
@require_permissions("insights.view_insighttag")
def list_tags(request):
    return [
        serialize_tag(tag)
        for tag in InsightTag.objects.all()
    ]


@router.post(
    "/tags",
    response={
        201: TagSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("insights.add_insighttag")
def create_tag(request, payload: TagCreateSchema):
    normalized_slug = slugify(payload.slug)

    if InsightTag.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Tag slug already exists.",
            code="duplicate_insight_tag",
        )

    tag = InsightTag.objects.create(
        name=payload.name,
        slug=normalized_slug,
        description=payload.description,
        is_active=payload.is_active,
        created_by=request.auth,
        updated_by=request.auth,
    )

    return 201, serialize_tag(tag)


@router.get(
    "",
    response={
        200: PaginatedResponseSchema[
            InsightArticleSchema
        ],
        403: ErrorSchema,
    },
)
@require_permissions("insights.view_insightarticle")
def list_articles(
    request,
    page: int = 1,
    page_size: int = 25,
    search: str | None = None,
    status: str | None = None,
    category_id: str | None = None,
    author_id: int | None = None,
    tag_id: str | None = None,
    is_featured: bool | None = None,
    is_active: bool | None = None,
    ordering: str | None = None,
):
    result = paginate_queryset(
        InsightArticleRepository.search(
            search=search,
            status=status,
            category_id=category_id,
            author_id=author_id,
            tag_id=tag_id,
            is_featured=is_featured,
            is_active=is_active,
            ordering=ordering,
        ),
        page=page,
        page_size=page_size,
    )

    return paginated_response(
        result,
        serializer=serialize_article,
    )


@router.post(
    "",
    response={
        201: InsightArticleSchema,
        400: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("insights.add_insightarticle")
def create_article(
    request,
    payload: InsightArticleCreateSchema,
):
    normalized_slug = slugify(payload.slug)

    if InsightArticle.all_objects.filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Article slug already exists.",
            code="duplicate_insight_slug",
        )

    (
        values,
        tags,
        related_articles,
        internal_links,
        seo,
    ) = payload_parts(payload)

    if values["author"] is None:
        values["author"] = request.auth

    article = InsightService.create_article(
        request=request,
        values=values,
        tags=tags,
        related_articles=related_articles,
        internal_links=internal_links,
        seo_values=seo,
    )

    return 201, serialize_article(
        refresh_article(article)
    )


@router.get(
    "/{article_id}",
    response={
        200: InsightArticleSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("insights.view_insightarticle")
def article_detail(request, article_id: str):
    return serialize_article(
        get_article(article_id)
    )


@router.put(
    "/{article_id}",
    response={
        200: InsightArticleSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("insights.change_insightarticle")
def update_article(
    request,
    article_id: str,
    payload: InsightArticleUpdateSchema,
):
    article = get_article(article_id)
    normalized_slug = slugify(payload.slug)

    if InsightArticle.all_objects.exclude(
        pk=article.pk
    ).filter(
        slug=normalized_slug,
    ).exists():
        raise ApiHttpError(
            400,
            "Article slug already exists.",
            code="duplicate_insight_slug",
        )

    (
        values,
        tags,
        related_articles,
        internal_links,
        seo,
    ) = payload_parts(
        payload,
        article=article,
    )

    article = InsightService.update_article(
        request=request,
        article=article,
        values=values,
        tags=tags,
        related_articles=related_articles,
        internal_links=internal_links,
        seo_values=seo,
        change_summary=payload.change_summary,
    )

    return serialize_article(
        refresh_article(article)
    )


@router.delete(
    "/{article_id}",
    response={
        200: MessageSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("insights.delete_insightarticle")
def delete_article(request, article_id: str):
    InsightService.soft_delete(
        request=request,
        article=get_article(article_id),
    )

    return {
        "status": "ok",
        "message": "Insight article deleted successfully.",
    }


@router.post(
    "/{article_id}/publish",
    response={
        200: InsightArticleSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("insights.change_insightarticle")
def publish_article(request, article_id: str):
    article = InsightService.publish_article(
        request=request,
        article=get_article(article_id),
    )

    return serialize_article(
        refresh_article(article)
    )


@router.post(
    "/{article_id}/schedule",
    response={
        200: InsightArticleSchema,
        400: ErrorSchema,
        404: ErrorSchema,
        403: ErrorSchema,
    },
)
@require_permissions("insights.change_insightarticle")
def schedule_article(
    request,
    article_id: str,
    payload: InsightScheduleSchema,
):
    try:
        article = InsightService.schedule_article(
            request=request,
            article=get_article(article_id),
            scheduled_for=payload.scheduled_for,
        )
    except ValueError as exc:
        raise ApiHttpError(
            400,
            str(exc),
            code="invalid_publish_schedule",
        ) from exc

    return serialize_article(
        refresh_article(article)
    )
