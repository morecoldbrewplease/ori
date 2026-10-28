from django.test import TestCase
from django.urls import reverse

from accounts.models import User


class HomeTests(TestCase):
    url = reverse("dashboard:home")

    def test_anonymous_user_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_logged_in_user_sees_dashboard(self):
        user = User.objects.create_user("alice", "alice@example.com", "pw")
        self.client.force_login(user)
        response = self.client.get(self.url)
        self.assertContains(response, "Hi, alice")
