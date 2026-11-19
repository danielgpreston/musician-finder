from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Genre, Instrument, Profile

User = get_user_model()

ME_URL = "/api/profiles/me/"
OPTIONS_URL = "/api/options/"
UNAUTHENTICATED = (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN)


def detail_url(user_id):
    return f"/api/profiles/{user_id}/"


class ProfileTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user("tester", "test@example.com", "testpass123")
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
        self.guitar = Instrument.objects.create(name="Guitar")
        self.drums = Instrument.objects.create(name="Drums")
        self.rock = Genre.objects.create(name="Rock")
        self.jazz = Genre.objects.create(name="Jazz")


class MyProfileTests(ProfileTestCase):
    def test_get_creates_default_profile(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], "tester")
        self.assertEqual(res.data["experience_level"], "beginner")
        self.assertEqual(res.data["instruments"], [])
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_requires_login(self):
        self.client.credentials()
        res = self.client.get(ME_URL)
        self.assertIn(res.status_code, UNAUTHENTICATED)

    def test_patch_updates_and_persists_fields(self):
        data = {
            "display_name": "Alex Rivera",
            "bio": "Looking for a drummer",
            "age": 25,
            "city": "Gainesville",
            "state": "FL",
            "experience_level": "advanced",
            "instruments": ["Guitar"],
            "genres": ["Rock", "Jazz"],
            "looking_for": ["Drums"],
        }
        res = self.client.patch(ME_URL, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        again = self.client.get(ME_URL)
        self.assertEqual(again.data["display_name"], "Alex Rivera")
        self.assertEqual(again.data["experience_level"], "advanced")
        self.assertEqual(again.data["instruments"], ["Guitar"])
        self.assertEqual(set(again.data["genres"]), {"Rock", "Jazz"})
        self.assertEqual(again.data["looking_for"], ["Drums"])

    def test_unknown_instrument_is_rejected(self):
        res = self.client.patch(ME_URL, {"instruments": ["Kazoo"]}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_experience_level_is_rejected(self):
        res = self.client.patch(ME_URL, {"experience_level": "wizard"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_age_boundaries(self):
        for age in (13, 120):
            with self.subTest(age=age):
                res = self.client.patch(ME_URL, {"age": age}, format="json")
                self.assertEqual(res.status_code, status.HTTP_200_OK)
        for age in (-1, 12, 121):
            with self.subTest(age=age):
                res = self.client.patch(ME_URL, {"age": age}, format="json")
                self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bio_length_boundary(self):
        ok = self.client.patch(ME_URL, {"bio": "x" * 500}, format="json")
        self.assertEqual(ok.status_code, status.HTTP_200_OK)
        too_long = self.client.patch(ME_URL, {"bio": "x" * 501}, format="json")
        self.assertEqual(too_long.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_url_is_rejected(self):
        res = self.client.patch(ME_URL, {"website": "not a url"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_and_id_cannot_be_changed(self):
        res = self.client.patch(ME_URL, {"username": "hacker", "id": 999}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["username"], "tester")
        self.assertNotEqual(res.data["id"], 999)

    def test_deactivate_profile(self):
        res = self.client.patch(ME_URL, {"is_active": False}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(res.data["is_active"])
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())


class ProfileDetailTests(ProfileTestCase):
    def setUp(self):
        super().setUp()
        self.other = User.objects.create_user("other", "other@example.com", "otherpass123")
        self.other_profile = Profile.objects.create(
            user=self.other, display_name="Sam", city="Orlando"
        )

    def test_view_another_users_profile(self):
        res = self.client.get(detail_url(self.other.id))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["display_name"], "Sam")

    def test_profile_does_not_expose_email(self):
        res = self.client.get(detail_url(self.other.id))
        self.assertNotIn("email", res.data)

    def test_unknown_user_returns_404(self):
        res = self.client.get(detail_url(99999))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_without_profile_returns_404(self):
        nobody = User.objects.create_user("noprofile", "np@example.com", "password123")
        res = self.client.get(detail_url(nobody.id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_deactivated_profile_is_hidden(self):
        self.other_profile.is_active = False
        self.other_profile.save()
        res = self.client.get(detail_url(self.other.id))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_requires_login(self):
        self.client.credentials()
        res = self.client.get(detail_url(self.other.id))
        self.assertIn(res.status_code, UNAUTHENTICATED)


class OptionsTests(ProfileTestCase):
    def test_lists_instruments_genres_and_levels(self):
        res = self.client.get(OPTIONS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("Guitar", res.data["instruments"])
        self.assertIn("Rock", res.data["genres"])
        self.assertEqual(
            res.data["experience_levels"],
            ["beginner", "intermediate", "advanced", "professional"],
        )

    def test_requires_login(self):
        self.client.credentials()
        res = self.client.get(OPTIONS_URL)
        self.assertIn(res.status_code, UNAUTHENTICATED)


class ProfileFlowTests(APITestCase):
    def test_register_build_profile_view_and_logout(self):
        Instrument.objects.create(name="Bass")
        Genre.objects.create(name="Funk")

        reg = self.client.post(
            "/api/auth/register/",
            {"username": "newmusician", "email": "nm@example.com", "password": "password123"},
            format="json",
        )
        self.assertEqual(reg.status_code, status.HTTP_201_CREATED)
        token = reg.data["token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        patch = self.client.patch(
            ME_URL, {"display_name": "New Musician", "instruments": ["Bass"], "genres": ["Funk"]},
            format="json",
        )
        self.assertEqual(patch.status_code, status.HTTP_200_OK)

        user = User.objects.get(username="newmusician")
        view = self.client.get(detail_url(user.id))
        self.assertEqual(view.status_code, status.HTTP_200_OK)
        self.assertEqual(view.data["instruments"], ["Bass"])

        self.client.post("/api/auth/logout/")
        after = self.client.get(ME_URL)
        self.assertIn(after.status_code, UNAUTHENTICATED)
