import datetime
from unittest.mock import patch

from django.test import TestCase

from scrumboard.models import Item, Sprint, Event


class ItemChangeEventTestCase(TestCase):
    def setUp(self):
        self.today = datetime.date(2016, 3, 4)
        self.tomorrow = datetime.date(2016, 3, 5)

    @patch('scrumboard.models.Event.create_item_created_event')
    def test_item_create_calls_item_created_event(self, mock_create_event):
        sprint = Sprint.objects.create(
            name='256',
            start_date=self.today,
            end_date=self.tomorrow
        )

        item = Item(
            name='Int.32',
            description='test item',
            estimate_work=3,
            estimate_review=2,
            sprint=sprint
        )

        expected_event = Event(
            sprint=sprint,
            change=Event.INC,
            value=5
        )

        mock_create_event.return_value = expected_event

        item.save()

        events = Event.get_events(sprint)
        assert len(events) == 1

        event = events[0]
        assert event.sprint == expected_event.sprint
        assert event.change == expected_event.change
        assert event.value == expected_event.value
