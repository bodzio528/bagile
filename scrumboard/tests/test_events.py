import datetime

from django.test import TestCase

from scrumboard.models import Event, Sprint


class EstimateChangeEventTestCase(TestCase):
    def setUp(self):
        self.start_date = datetime.date(2015, 4, 30)
        self.end_date = datetime.date(2015, 5, 10)

        self.sprint = Sprint.objects.create(
            name='249',
            start_date=self.start_date,
            end_date=self.end_date
        )

    def test_if_event_can_be_created(self):
        event = Event.objects.create(
            sprint=self.sprint,
            date=self.start_date,
            change=Event.INC,
            value=3
        )

        self.assertIn(event, Event.get_events(self.sprint))

