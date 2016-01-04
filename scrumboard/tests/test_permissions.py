from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django.test import TestCase
from django.test import Client


class AuthenticatedViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='developer1', email='developer1@bagile.org', password='top_secret')

    def test_should_redirect_unauthenticated_user(self):
        c = Client()
        response = c.get(reverse('scrumboard:item_create'))

        assert response.status_code == 302  # redirection

    def skip_test_should_service_authenticated_user(self):
        c = Client()
        c.login(username='developer1', password='top_secret')

        response = c.get(reverse('scrumboard:item_create'))

        assert response.status_code == 200
