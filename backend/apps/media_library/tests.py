from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from ninja.testing import TestClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.api.api import api

from .models import (
    MediaAsset,
    MediaFolder,
    MediaType,
    MediaUsage,
)
from .services import MediaLibraryService


User = get_user_model()


class MediaLibraryServiceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="media-admin",
            email="media-admin@example.com",
            password="StrongPassword123!",
        )

        self.request = type(
            "Request",
            (),
            {
                "auth": self.admin,
                "META": {},
            },
        )()

    def test_folder_can_be_created(self):
        folder = MediaLibraryService.create_folder(
            request=self.request,
            name="Website Images",
        )

        self.assertEqual(folder.slug, "website-images")

    def test_duplicate_folder_is_rejected(self):
        MediaLibraryService.create_folder(
            request=self.request,
            name="Website Images",
        )

        with self.assertRaises(ValueError):
            MediaLibraryService.create_folder(
                request=self.request,
                name="Website Images",
            )

    def test_asset_upload_detects_image(self):
        uploaded = SimpleUploadedFile(
            "hero.jpg",
            b"fake-image-content",
            content_type="image/jpeg",
        )

        asset = MediaLibraryService.upload_asset(
            request=self.request,
            uploaded_file=uploaded,
            title="Homepage Hero",
        )

        self.assertEqual(
            asset.media_type,
            MediaType.IMAGE,
        )
        self.assertEqual(asset.extension, "jpg")
        self.assertTrue(asset.checksum)

    def test_duplicate_upload_is_rejected(self):
        first = SimpleUploadedFile(
            "hero.jpg",
            b"same-content",
            content_type="image/jpeg",
        )

        second = SimpleUploadedFile(
            "hero-copy.jpg",
            b"same-content",
            content_type="image/jpeg",
        )

        MediaLibraryService.upload_asset(
            request=self.request,
            uploaded_file=first,
        )

        with self.assertRaises(ValueError):
            MediaLibraryService.upload_asset(
                request=self.request,
                uploaded_file=second,
            )

    def test_used_asset_cannot_be_deleted(self):
        uploaded = SimpleUploadedFile(
            "document.pdf",
            b"pdf-content",
            content_type="application/pdf",
        )

        asset = MediaLibraryService.upload_asset(
            request=self.request,
            uploaded_file=uploaded,
        )

        MediaLibraryService.register_usage(
            request=self.request,
            asset=asset,
            application="cms",
            model_name="Page",
            object_id="page-1",
            field_name="featured_image",
        )

        with self.assertRaises(ValueError):
            MediaLibraryService.soft_delete_asset(
                request=self.request,
                asset=asset,
            )


class MediaLibraryApiTests(TestCase):
    def setUp(self):
        self.client = TestClient(api)

        self.admin = User.objects.create_superuser(
            username="media-api-admin",
            email="media-api@example.com",
            password="StrongPassword123!",
        )

        token = RefreshToken.for_user(
            self.admin
        ).access_token

        self.headers = {
            "Authorization": f"Bearer {token}",
        }

    def test_superuser_can_create_folder(self):
        response = self.client.post(
            "/media/folders",
            json={
                "name": "Case Studies",
                "description": "Case-study media.",
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["slug"],
            "case-studies",
        )

    def test_superuser_can_list_folders(self):
        MediaFolder.objects.create(
            name="Logos",
            slug="logos",
            created_by=self.admin,
            updated_by=self.admin,
        )

        response = self.client.get(
            "/media/folders",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

    def test_superuser_can_upload_asset(self):
        uploaded = SimpleUploadedFile(
            "logo.svg",
            b"<svg></svg>",
            content_type="image/svg+xml",
        )

        response = self.client.post(
            "/media/assets/upload",
            data={
                "title": "LKP Logo",
                "is_public": "true",
            },
            FILES={
                "file": uploaded,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["title"],
            "LKP Logo",
        )
        self.assertEqual(
            response.json()["media_type"],
            MediaType.LOGO,
        )

    def test_superuser_can_update_asset(self):
        uploaded = SimpleUploadedFile(
            "photo.jpg",
            b"photo-content",
            content_type="image/jpeg",
        )

        asset = MediaLibraryService.upload_asset(
            request=type(
                "Request",
                (),
                {
                    "auth": self.admin,
                    "META": {},
                },
            )(),
            uploaded_file=uploaded,
        )

        response = self.client.put(
            f"/media/assets/{asset.pk}",
            json={
                "folder_id": None,
                "title": "Updated Photo",
                "media_type": "image",
                "alt_text": "Updated alternative text",
                "caption": "",
                "description": "",
                "tags": ["website"],
                "is_public": True,
            },
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["title"],
            "Updated Photo",
        )

    def test_usage_registration_blocks_delete(self):
        uploaded = SimpleUploadedFile(
            "brochure.pdf",
            b"brochure-content",
            content_type="application/pdf",
        )

        asset = MediaLibraryService.upload_asset(
            request=type(
                "Request",
                (),
                {
                    "auth": self.admin,
                    "META": {},
                },
            )(),
            uploaded_file=uploaded,
        )

        usage_response = self.client.post(
            f"/media/assets/{asset.pk}/usages",
            json={
                "application": "cms",
                "model_name": "Page",
                "object_id": "page-1",
                "field_name": "document",
                "usage_context": "About page brochure",
            },
            headers=self.headers,
        )

        self.assertEqual(
            usage_response.status_code,
            201,
        )

        delete_response = self.client.delete(
            f"/media/assets/{asset.pk}",
            headers=self.headers,
        )

        self.assertEqual(
            delete_response.status_code,
            400,
        )
        self.assertEqual(
            delete_response.json()["code"],
            "media_asset_in_use",
        )

        self.assertTrue(
            MediaUsage.objects.filter(
                asset=asset,
            ).exists()
        )

    def test_unused_asset_can_be_soft_deleted(self):
        uploaded = SimpleUploadedFile(
            "unused.txt",
            b"unused-content",
            content_type="text/plain",
        )

        asset = MediaLibraryService.upload_asset(
            request=type(
                "Request",
                (),
                {
                    "auth": self.admin,
                    "META": {},
                },
            )(),
            uploaded_file=uploaded,
        )

        response = self.client.delete(
            f"/media/assets/{asset.pk}",
            headers=self.headers,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            MediaAsset.objects.filter(
                pk=asset.pk,
            ).exists()
        )
        self.assertTrue(
            MediaAsset.all_objects.filter(
                pk=asset.pk,
            ).exists()
        )

    def test_unauthenticated_request_is_rejected(self):
        response = self.client.get("/media/assets")

        self.assertEqual(response.status_code, 401)
