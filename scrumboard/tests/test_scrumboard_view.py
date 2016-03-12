from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.test import TestCase
from django.test import Client

from scrumboard.models import Sprint, Item


class ScrumboardViewTestCase(TestCase):
    def setUp(self):
        import datetime
        from unittest.mock import patch

        patcher = patch('scrumboard.models.Sprint.get_current_sprint')
        self.addCleanup(patcher.stop)

        self.current_sprint = Sprint.objects.create(
            name='251',
            start_date=datetime.date(2015, 4, 30),
            end_date=datetime.date(2015, 5, 15),
            capacity=100
        )

        self.mock_current_sprint = patcher.start()
        self.mock_current_sprint.return_value = self.current_sprint

    def test_should_use_current_sprint_by_default(self):
        c = Client()
        response = c.get(reverse('scrumboard:index'))

        assert response.context['sprint'] == self.current_sprint

    def test_committed_item_appears_in_unassigned_items(self):
        item = Item.objects.create(
            name='item item',
            status=Item.COMMITTED,
            sprint=self.current_sprint
        )

        c = Client()
        response = c.get(reverse('scrumboard:index'))

        assert item in response.context['unassigned_items']['COMMITTED']

    def test_user_appears_in_assigned_items(self):
        developers = Group.objects.create(name='developers')

        dev1 = User.objects.create_user(username='dev1', email='dev1@localhost', password='top_secret')
        dev1.groups.add(developers)

        c = Client()
        response = c.get(reverse('scrumboard:index'))

        assert response.context['assigned_items'][0]['user'] == dev1
