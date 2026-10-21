from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

User = get_user_model()

LOGIN_URL = "/api/auth/login/"
LOGOUT_URL = "/api/auth/logout/"
REGISTER_URL = "/api/auth/register/"


class LoginTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", email="test@example.com", password="testpass123"
        )

    def test_login_success_returns_token(self):
        res = self.client.post(LOGIN_URL, {"email": "test@example.com", "password": "testpass123"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data)

    def test_login_email_is_case_insensitive(self):
        res = self.client.post(LOGIN_URL, {"email": "TEST@Example.com", "password": "testpass123"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_trims_whitespace_around_email(self):
        res = self.client.post(LOGIN_URL, {"email": "  test@example.com  ", "password": "testpass123"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_login_wrong_password(self):
        res = self.client.post(LOGIN_URL, {"email": "test@example.com", "password": "wrong"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_login_unknown_email(self):
        res = self.client.post(LOGIN_URL, {"email": "nobody@example.com", "password": "testpass123"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_sql_injection_attempt_is_rejected(self):
        res = self.client.post(
            LOGIN_URL,
            {"email": "' OR '1'='1", "password": "' OR '1'='1"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Token.objects.exists())

    def test_login_empty_body(self):
        res = self.client.post(LOGIN_URL, {}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_password(self):
        res = self.client.post(LOGIN_URL, {"email": "test@example.com"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_whitespace_only_email(self):
        res = self.client.post(LOGIN_URL, {"email": "   ", "password": "testpass123"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_rejects_get_requests(self):
        res = self.client.get(LOGIN_URL)
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class LogoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester", email="test@example.com", password="testpass123"
        )
        self.token = Token.objects.create(user=self.user)

    def test_logout_deletes_token(self):
        res = self.client.post(LOGOUT_URL, HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_logout_without_token_is_rejected(self):
        res = self.client.post(LOGOUT_URL)
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_logout_with_invalid_token_is_rejected(self):
        res = self.client.post(LOGOUT_URL, HTTP_AUTHORIZATION="Token notarealtoken")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_token_cannot_be_reused_after_logout(self):
        self.client.post(LOGOUT_URL, HTTP_AUTHORIZATION=f"Token {self.token.key}")
        res = self.client.post(LOGOUT_URL, HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.assertIn(res.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))


class RegisterTests(APITestCase):
    def valid_data(self, **overrides):
        data = {"username": "newuser", "email": "new@example.com", "password": "password123"}
        data.update(overrides)
        return data

    def test_register_success_returns_token(self):
        res = self.client.post(REGISTER_URL, self.valid_data(), format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", res.data)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_password_of_exactly_8_characters_is_accepted(self):
        res = self.client.post(REGISTER_URL, self.valid_data(password="12345678"), format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_register_password_of_7_characters_is_rejected(self):
        res = self.client.post(REGISTER_URL, self.valid_data(password="1234567"), format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_register_missing_fields_is_rejected(self):
        for field in ("username", "email", "password"):
            data = self.valid_data()
            data.pop(field)
            res = self.client.post(REGISTER_URL, data, format="json")
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST, msg=field)

    def test_register_duplicate_username_is_rejected_case_insensitively(self):
        User.objects.create_user("newuser", "other@example.com", "password123")
        res = self.client.post(REGISTER_URL, self.valid_data(username="NEWUSER"), format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_email_is_rejected(self):
        User.objects.create_user("someoneelse", "new@example.com", "password123")
        res = self.client.post(REGISTER_URL, self.valid_data(), format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class AuthIntegrationTests(APITestCase):
    def test_login_then_logout_flow(self):
        User.objects.create_user(username="tester", email="test@example.com", password="testpass123")
        login = self.client.post(LOGIN_URL, {"email": "test@example.com", "password": "testpass123"}, format="json")
        token = login.data["token"]
        logout = self.client.post(LOGOUT_URL, HTTP_AUTHORIZATION=f"Token {token}")
        self.assertEqual(logout.status_code, status.HTTP_200_OK)
        again = self.client.post(LOGOUT_URL, HTTP_AUTHORIZATION=f"Token {token}")
        self.assertIn(again.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_register_then_login_flow(self):
        reg = self.client.post(
            REGISTER_URL,
            {"username": "newuser", "email": "new@example.com", "password": "password123"},
            format="json",
        )
        self.assertEqual(reg.status_code, status.HTTP_201_CREATED)
        login = self.client.post(LOGIN_URL, {"email": "new@example.com", "password": "password123"}, format="json")
        self.assertEqual(login.status_code, status.HTTP_200_OK)
