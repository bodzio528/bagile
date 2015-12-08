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

        self.assertEqual(str(sprint), '{0}: {1}/{2}'.format(name, start_date, end_date))


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
        self.assertEqual([], Sprint.fetch_active())

    def test_returns_none_if_no_sprints_active(self):
        Sprint.objects.create(start_date=self.one_week_ago, end_date=self.three_days_ago)

        self.assertEqual([], Sprint.fetch_active())

    def test_returns_active_sprint_as_current_sprint(self):
        sprint = Sprint.objects.create(start_date=self.three_days_ago, end_date=self.in_four_days)

        active_sprints = Sprint.fetch_active()

        self.assertEqual(1, len(active_sprints))
        self.assertIn(sprint, active_sprints)
