import datetime

from django.test import TestCase

from scrumboard.models import Item, Sprint, Event


class ItemChangeEventTestCase(TestCase):
    def setUp(self):
        self.today = datetime.date(2016, 3, 4)
        self.tomorrow = datetime.date(2016, 3, 5)

    def test_item_create_calls_create_event(self):
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

        item.save()

        events = Event.objects.filter(sprint=sprint)

        self.assertEqual(1, len(events))

        event = events[0]

        self.assertEqual(sprint, event.sprint)
        self.assertEqual(Event.INC, event.change)
        self.assertEqual(item.estimate_work + item.estimate_review, event.value)
