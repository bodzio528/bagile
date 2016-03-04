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

        mock_create_event.return_value = Event(
            sprint=sprint,
            change=Event.INC,
            value=5
        )

        item.save()

        events = Event.get_events(sprint)
        assert len(events) is 1

        event = events[0]
        self.assertEqual(event.sprint, sprint)
        self.assertEqual(event.change, Event.INC)
        self.assertEqual(event.value, 5)
    #
    # def test_create_event_for_instance_created_is_connected(self, mock_factory):
    #     item = Item.objects.create(
    #         name="asdf",
    #         sprint=self.sprint,
    #         estimate_work=5,
    #         estimate_review=3
    #     )

        # assert mock_call
        #
        # events = Event.get_events(self.sprint)
        #
        # assert len(events) is 1
        # assert events[0].change is Event.INC
        # assert events[0].value is 8
