from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import User

from .models import (
    Testimonial,
    TestimonialSource,
    TestimonialStatus,
)
from .repositories import TestimonialRepository
from .services import TestimonialService


class RequestStub:
    def __init__(self, user):
        self.auth = user
        self.user = user
        self.META = {}
        self.headers = {}


class TestimonialModelTests(TestCase):
    def test_testimonial_defaults(self):
        testimonial = Testimonial.objects.create(
            author_name="Example Client",
            company_name="Example Company",
            content="Excellent delivery and support.",
        )

        self.assertEqual(testimonial.rating, 5)
        self.assertEqual(
            testimonial.status,
            TestimonialStatus.DRAFT,
        )
        self.assertEqual(
            testimonial.source,
            TestimonialSource.DIRECT,
        )
        self.assertFalse(
            testimonial.is_publicly_available
        )

    def test_published_testimonial_is_public(self):
        testimonial = Testimonial.objects.create(
            author_name="Example Client",
            content="Excellent work.",
            status=TestimonialStatus.PUBLISHED,
            published_at=timezone.now(),
            is_active=True,
        )

        self.assertTrue(
            testimonial.is_publicly_available
        )

    def test_future_published_testimonial_is_not_public(self):
        testimonial = Testimonial.objects.create(
            author_name="Example Client",
            content="Excellent work.",
            status=TestimonialStatus.PUBLISHED,
            published_at=(
                timezone.now() + timedelta(days=1)
            ),
            is_active=True,
        )

        self.assertFalse(
            testimonial.is_publicly_available
        )


class TestimonialRepositoryTests(TestCase):
    def setUp(self):
        Testimonial.objects.create(
            author_name="Alpha Client",
            company_name="Alpha Ltd",
            content="Strong project delivery.",
            rating=5,
            source=TestimonialSource.GOOGLE,
            is_featured=True,
        )

        Testimonial.objects.create(
            author_name="Beta Client",
            company_name="Beta Ltd",
            content="Reliable technical support.",
            rating=4,
            source=TestimonialSource.EMAIL,
            is_featured=False,
        )

    def test_search_by_author_and_company(self):
        queryset = TestimonialRepository.search(
            search="Alpha"
        )

        self.assertEqual(queryset.count(), 1)
        self.assertEqual(
            queryset.first().author_name,
            "Alpha Client",
        )

    def test_filter_by_rating_source_and_featured(self):
        queryset = TestimonialRepository.search(
            rating=5,
            source=TestimonialSource.GOOGLE,
            is_featured=True,
        )

        self.assertEqual(queryset.count(), 1)

    def test_invalid_ordering_is_ignored(self):
        queryset = TestimonialRepository.search(
            ordering="not_a_real_field"
        )

        self.assertEqual(queryset.count(), 2)


class TestimonialServiceTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testimonial_admin",
            email="testimonials@example.com",
            password="StrongPassword123!",
        )
        self.request = RequestStub(self.user)

        self.testimonial = Testimonial.objects.create(
            author_name="Service Client",
            company_name="Service Company",
            content="Professional service.",
        )

    def test_publish_testimonial(self):
        testimonial = (
            TestimonialService.publish_testimonial(
                request=self.request,
                testimonial=self.testimonial,
            )
        )

        self.assertEqual(
            testimonial.status,
            TestimonialStatus.PUBLISHED,
        )
        self.assertIsNotNone(testimonial.published_at)
        self.assertIsNone(testimonial.scheduled_for)

    def test_schedule_testimonial(self):
        scheduled_for = (
            timezone.now() + timedelta(days=2)
        )

        testimonial = (
            TestimonialService.schedule_testimonial(
                request=self.request,
                testimonial=self.testimonial,
                scheduled_for=scheduled_for,
            )
        )

        self.assertEqual(
            testimonial.status,
            TestimonialStatus.SCHEDULED,
        )
        self.assertEqual(
            testimonial.scheduled_for,
            scheduled_for,
        )

    def test_schedule_rejects_past_datetime(self):
        with self.assertRaises(ValueError):
            TestimonialService.schedule_testimonial(
                request=self.request,
                testimonial=self.testimonial,
                scheduled_for=(
                    timezone.now() - timedelta(minutes=1)
                ),
            )

    def test_soft_delete_testimonial(self):
        testimonial_id = self.testimonial.pk

        TestimonialService.soft_delete(
            request=self.request,
            testimonial=self.testimonial,
        )

        self.assertFalse(
            Testimonial.objects.filter(
                pk=testimonial_id
            ).exists()
        )
        self.assertTrue(
            Testimonial.all_objects.filter(
                pk=testimonial_id,
                is_deleted=True,
            ).exists()
        )
