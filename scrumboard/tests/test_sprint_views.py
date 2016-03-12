import datetime

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from django.test import TestCase
from django.test import Client

from scrumboard.models import Sprint


class SprintViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        developers = Group.objects.create(name='developers')

        dev1 = User.objects.create_user(username='dev1', email='dev1@localhost', password='top_secret')
        dev1.groups.add(developers)

    def setup_current_sprint(self, current_sprint):
        from unittest.mock import patch
        patcher = patch('scrumboard.models.Sprint.get_current_sprint')
        self.addCleanup(patcher.stop)
        self.mock_current_sprint = patcher.start()
        self.mock_current_sprint.return_value = current_sprint

    def setup_active_sprints(self, active_sprints):
        from unittest.mock import patch
        patcher = patch('scrumboard.models.Sprint.get_active_sprints')
        self.addCleanup(patcher.stop)
        self.mock_current_sprint = patcher.start()
        self.mock_current_sprint.return_value = active_sprints


class InstanceSprintViewTestCase(SprintViewTestCase):
    def setUp(self):
        self.sprint = Sprint.objects.create(
            name='251',
            start_date=datetime.date(2015, 4, 30),
            end_date=datetime.date(2015, 5, 15),
            capacity=100
        )

        dummy_current_sprint = Sprint.objects.create(
            name='current',
            start_date=datetime.date(2015, 5, 15),
            end_date=datetime.date(2015, 5, 30),
            capacity=100
        )

        self.setup_current_sprint(dummy_current_sprint)

    def test_sprint_url_is_correct(self):
        assert self.sprint.get_absolute_url() == reverse('scrumboard:sprint_details', kwargs={'pk': self.sprint.pk})

    def test_if_update_sprint_context_has_correct_sprint_instance_based_on_url(self):
        c = Client()
        c.login(username='dev1', password='top_secret')

        response = c.get(reverse('scrumboard:sprint_update', kwargs={'pk': self.sprint.pk}))

        assert self.sprint == response.context['sprint']

    def test_if_sprint_detail_context_has_correct_sprint_instance_based_on_url(self):
        c = Client()
        c.login(username='dev1', password='top_secret')

        response = c.get(reverse('scrumboard:sprint_details', kwargs={'pk': self.sprint.pk}))

        assert self.sprint == response.context['sprint']


class NoInstanceSprintViewTestCase(SprintViewTestCase):
    def setUp(self):
        sprint_a1 = Sprint.objects.create(
            name='251.1',
            start_date=datetime.date(2015, 4, 30),
            end_date=datetime.date(2015, 5, 7),
            capacity=100
        )

        sprint_a2 = Sprint.objects.create(
            name='251.2',
            start_date=datetime.date(2015, 5, 7),
            end_date=datetime.date(2015, 5, 15),
            capacity=110
        )

        self.active_sprints = [sprint_a1, sprint_a2]
        self.setup_active_sprints(self.active_sprints)

        self.setup_current_sprint(self.active_sprints[0])

    def test_sprint_active_view_has_correct_content(self):
        c = Client()
        c.login(username='dev1', password='top_secret')

        response = c.get(reverse('scrumboard:sprint_active'))

        self.assertEqual(response.status_code, 200)

        from django.forms import model_to_dict
        self.assertJSONEqual(str(response.content, encoding='utf8'),
                             [model_to_dict(sprint, fields=['id', 'name']) for sprint in self.active_sprints])

    def test_sprint_current_view_has_correct_content(self):
        c = Client()
        c.login(username='dev1', password='top_secret')
        response = c.get(reverse('scrumboard:sprint_current'))

        self.assertEqual(response.status_code, 200)

        import json
        result = json.loads(str(response.content, encoding='utf8'))['current_sprint']

        assert result['id'] == self.active_sprints[0].id
        assert result['start_date'] == str(self.active_sprints[0].start_date)
        assert result['end_date'] == str(self.active_sprints[0].end_date)
        assert result['capacity'] == self.active_sprints[0].capacity
