import datetime

from django.test import TestCase

from scrumboard.models import Event, Item, Sprint


class EventFactoryTestCase(TestCase):
    def setUp(self):
        self.sprint = Sprint.objects.create(
            name="256",
            start_date=datetime.date(2015, 3, 8),
            end_date=datetime.date(2015, 3, 18),
        )

        self.item = Item(
            name="An Item",
            sprint=self.sprint,
            estimate_work=5,
            estimate_review=2
        )

    def test_create_event_for_instance_created(self):
        event = Event.create_item_created_event(self.item)

        assert isinstance(event, Event)
        assert event.change == Event.INC
        assert event.value == 7

        assert event.sprint == self.sprint

    def test_create_event_for_instance_deleted(self):
        event = Event.create_item_deleted_event(self.item)

        assert isinstance(event, Event)
        assert event.change == Event.DEC
        assert event.value == 7

        assert event.sprint == self.sprint


class StatusChangeEventFactoryTestCase(TestCase):
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

    def test_create_events_for_sprint_change(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=8,
            estimate_review=3
        )

        item.sprint = self.sprint2

        events = Event.create_item_changed_events(item)

        assert len(events) == 2

        assert events[0].change == Event.INC
        assert events[0].value == 11
        assert events[0].sprint == self.sprint2

        assert events[1].change == Event.DEC
        assert events[1].value == 11
        assert events[1].sprint == self.sprint1

    def test_committed_to_wip(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=8,
            estimate_review=3,
            status=Item.COMMITTED
        )

        item.status = Item.WIP

        events = Event.create_item_changed_events(item)

        assert len(events) == 0

    def test_wip_to_pending_review(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=8,
            estimate_review=3,
            status=Item.WIP
        )

        item.status = Item.PENDING_REVIEW

        events = Event.create_item_changed_events(item)

        assert len(events) == 1
        assert events[0].change == Event.DEC
        assert events[0].value == 8
