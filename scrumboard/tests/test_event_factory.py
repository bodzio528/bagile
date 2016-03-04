import datetime

from django.test import TestCase

from scrumboard.models import Event, Item, Sprint


def create_item_changed_events(instance):
    if instance.pk is not 0:
        old_instance = Item.objects.get(pk=instance.pk)
        return []


def create_item_deleted_event(instance):
    pass


def is_item_created(instance):
    return 0 == instance.pk


def is_status_changed(instance, old_instance):
    return instance.status != old_instance.status


class EventFactoryTestCase(TestCase):
    def setUp(self):
        self.sprint1 = Sprint.objects.create(
            name="256",
            start_date=datetime.date(2015, 3, 8),
            end_date=datetime.date(2015, 3, 18),
        )

        self.sprint2 = Sprint.objects.create(
            name="257",
            start_date=datetime.date(2015, 3, 18),
            end_date=datetime.date(2015, 3, 28),
        )

    def test_create_event_for_instance_created(self):
        item = Item(
            name="asdf",
            sprint=self.sprint1,
            estimate_work=5,
            estimate_review=2
        )

        event = Event.create_item_created_event(item)

        assert isinstance(event, Event)
        assert event.change is Event.INC
        assert event.value is 7
