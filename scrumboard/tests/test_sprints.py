import datetime
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from scrumboard.models import Sprint


class SprintTestCase(TestCase):
    def test_sprint_name(self):
        name = '249'
        start_date = datetime.date(2015, 4, 30)
        end_date = datetime.date(2015, 12, 28)

        sprint = Sprint.objects.create(
            name=name,
            start_date=start_date,
            end_date=end_date
        )

        self.assertEqual(str(sprint), '{0}'.format(name))


class IsActiveSprintTestCase(TestCase):
    def setUp(self):
        patcher = patch('django.utils.timezone.now')
        self.addCleanup(patcher.stop)

        self.mock_time = patcher.start()
        self.mock_time.return_value = datetime.date(2015, 4, 30)
        self.now = timezone.now()

        self.two_weeks_ago = self.now - datetime.timedelta(days=14)
        self.one_week_ago = self.now - datetime.timedelta(days=7)
        self.in_one_week = self.now + datetime.timedelta(days=7)
        self.in_two_weeks = self.now + datetime.timedelta(days=14)

    def test_ended_sprint_is_not_active(self):
        sprint = Sprint.objects.create(
            start_date=self.two_weeks_ago,
            end_date=self.one_week_ago)
        self.assertFalse(sprint.is_active())

    def test_yet_to_begin_sprint_is_not_active(self):
        sprint = Sprint.objects.create(
            start_date=self.in_one_week,
            end_date=self.in_two_weeks)
        self.assertFalse(sprint.is_active())

    def test_begins_today_ends_today_sprint_is_active(self):
        sprint = Sprint.objects.create(
            start_date=self.now,
            end_date=self.now)
        self.assertTrue(sprint.is_active())

    def test_begins_today_ends_next_week_sprint_is_active(self):
        sprint = Sprint.objects.create(
            start_date=self.now,
            end_date=self.in_one_week)
        self.assertTrue(sprint.is_active())


class GetActiveSprintsTestCase(TestCase):
    def setUp(self):
        patcher = patch('django.utils.timezone.now')
        self.addCleanup(patcher.stop)

        self.mock_time = patcher.start()
        self.mock_time.return_value = datetime.date(2015, 4, 30)
        self.now = timezone.now()

        self.two_weeks_ago = self.now - datetime.timedelta(days=14)
        self.one_week_ago = self.now - datetime.timedelta(days=7)
        self.three_days_ago = self.now - datetime.timedelta(days=3)
        self.in_four_days = self.now + datetime.timedelta(days=4)
        self.in_one_week = self.now + datetime.timedelta(days=7)

    def test_returns_empty_list_if_no_sprint_in_database(self):
        self.assertEqual([], Sprint.get_active_sprints())

    def test_returns_none_if_no_sprints_active(self):
        Sprint.objects.create(start_date=self.one_week_ago, end_date=self.three_days_ago)

        self.assertEqual([], Sprint.get_active_sprints())

    def test_returns_active_sprint_as_current_sprint(self):
        sprint = Sprint.objects.create(start_date=self.three_days_ago, end_date=self.in_four_days)

        active_sprints = Sprint.get_active_sprints()

        self.assertEqual(1, len(active_sprints))
        self.assertIn(sprint, active_sprints)


class GetCurrentSprintTestCase(TestCase):
    def setUp(self):
        self.date_past = datetime.date(2015, 4, 15)
        self.date_now = datetime.date(2015, 4, 30)
        self.date_future = datetime.date(2015, 5, 15)

    def test_returns_none_if_no_sprint_in_database(self):
        self.assertEqual(None, Sprint.get_current_sprint())

    @patch('scrumboard.models.Sprint.get_active_sprints')
    def test_returns_single_sprint_if_active_count_is_one(self, active_sprints):
        sprint = Sprint.objects.create(start_date=self.date_now, end_date=self.date_now)
        active_sprints.return_value = [sprint]

        self.assertEqual(sprint, Sprint.get_current_sprint())

    @patch('scrumboard.models.Sprint.get_active_sprints')
    def test_returns_single_objects_if_active_count_is_more_than_one(self, active_sprints):
        sprint1 = Sprint.objects.create(start_date=self.date_past, end_date=self.date_now)
        sprint2 = Sprint.objects.create(start_date=self.date_now, end_date=self.date_future)
        active_sprints.return_value = [sprint1, sprint2]

        self.assertEqual(sprint1, Sprint.get_current_sprint())

    @patch('scrumboard.models.Sprint.get_active_sprints')
    def test_returns_earlier_started_sprint_if_they_overlap(self, active_sprints):
        sprint1 = Sprint.objects.create(start_date=self.date_now, end_date=self.date_future)
        sprint2 = Sprint.objects.create(start_date=self.date_past, end_date=self.date_now)
        active_sprints.return_value = [sprint1, sprint2]

        self.assertEqual(sprint2, Sprint.get_current_sprint())
