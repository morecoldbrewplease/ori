from django.test import TestCase
from django.urls import reverse

from .models import User


class SignUpTests(TestCase):
    url = reverse("accounts:signup")

    def post_signup(self, **overrides):
        data = {
            "username": "alice",
            "email": "alice@example.com",
            "password1": "correct-horse-42",
            "password2": "correct-horse-42",
        }
        data.update(overrides)
        return self.client.post(self.url, data)

    def test_page_renders(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create your account")

    def test_signup_creates_user_and_logs_in(self):
        response = self.post_signup()
        self.assertRedirects(response, reverse("dashboard:home"))
        user = User.objects.get(username="alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_email_is_stored_lowercase(self):
        self.post_signup(email="Alice@Example.COM")
        self.assertEqual(User.objects.get().email, "alice@example.com")

    def test_duplicate_email_rejected_case_insensitively(self):
        User.objects.create_user("bob", "alice@example.com", "pw")
        response = self.post_signup(email="ALICE@example.com")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A user with that email already exists.")
        self.assertFalse(User.objects.filter(username="alice").exists())

    def test_email_required(self):
        response = self.post_signup(email="")
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.exists())

    def test_logged_in_user_redirected_away(self):
        user = User.objects.create_user("bob", "bob@example.com", "pw")
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse("dashboard:home"))


class LoginLogoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            "alice", "alice@example.com", "correct-horse-42"
        )

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "alice", "password": "correct-horse-42"},
        )
        self.assertRedirects(response, reverse("dashboard:home"))

    def test_login_with_wrong_password(self):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "alice", "password": "wrong"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_requires_post_and_logs_out(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertNotIn("_auth_user_id", self.client.session)
