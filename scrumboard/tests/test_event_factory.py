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

    def test_do_not_create_event_for_item_update_when_item_is_not_updated(self):
        events = Event.create_item_changed_events(self.item)
        assert 0 == len(events)

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


class EstimateChangeEventFactoryTestCase(TestCase):
    def setUp(self):
        self.sprint = Sprint.objects.create(
            name="256",
            start_date=datetime.date(2015, 3, 8),
            end_date=datetime.date(2015, 3, 18),
        )
        self.item = Item.objects.create(
            name="Item",
            sprint=self.sprint,
            estimate_work=8,
            estimate_review=3
        )

    def test_no_event_when_no_estimate_changed(self):
        assert 0 == len(Event.create_item_changed_events(self.item))

    def test_create_event_work_estimate_increased(self):
        self.item.estimate_work += 5

        events = Event.create_item_changed_events(self.item)

        assert len(events) == 1

        assert events[0].change == Event.INC
        assert events[0].value == 5
        assert events[0].sprint == self.sprint

    def test_create_event_work_estimate_decreased(self):
        self.item.estimate_work -= 3

        events = Event.create_item_changed_events(self.item)

        assert len(events) == 1

        assert events[0].change == Event.DEC
        assert events[0].value == 3
        assert events[0].sprint == self.sprint

    def test_create_event_review_estimate_increased(self):
        self.item.estimate_work += 13

        events = Event.create_item_changed_events(self.item)

        assert len(events) == 1

        assert events[0].change == Event.INC
        assert events[0].value == 13
        assert events[0].sprint == self.sprint

    def test_create_event_review_estimate_decreased(self):
        self.item.estimate_work -= 5

        events = Event.create_item_changed_events(self.item)

        assert len(events) == 1

        assert events[0].change == Event.DEC
        assert events[0].value == 5
        assert events[0].sprint == self.sprint

    def test_create_event_review_estimate_increased_and_work_estimate_increased(self):
        self.item.estimate_work += 5
        self.item.estimate_review += 2

        events = Event.create_item_changed_events(self.item)

        assert len(events) == 1

        assert events[0].change == Event.INC
        assert events[0].value == 7
        assert events[0].sprint == self.sprint

    def test_create_event_review_estimate_decreased_and_work_estimate_increased(self):
        self.item.estimate_work += 5
        self.item.estimate_review -= 1

        events = Event.create_item_changed_events(self.item)

        assert len(events) == 1

        assert events[0].change == Event.INC
        assert events[0].value == 4
        assert events[0].sprint == self.sprint

    def test_create_event_review_estimate_increased_and_work_estimate_decreased(self):
        self.item.estimate_work -= 3
        self.item.estimate_review += 2

        events = Event.create_item_changed_events(self.item)

        assert len(events) == 1

        assert events[0].change == Event.DEC
        assert events[0].value == 1
        assert events[0].sprint == self.sprint

    def test_create_event_review_estimate_decreased_and_work_estimate_decreased(self):
        self.item.estimate_work -= 3
        self.item.estimate_review -= 1

        events = Event.create_item_changed_events(self.item)

        assert len(events) == 1

        assert events[0].change == Event.DEC
        assert events[0].value == 4
        assert events[0].sprint == self.sprint


class SprintChangeEventFactoryTestCase(TestCase):
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

    def test_move_item_takes_effort_and_review_when_status_committed_wip_or_blocked(self):
        def test_for_status(status):
            item = Item.objects.create(
                name="Item",
                sprint=self.sprint1,
                estimate_work=8,
                estimate_review=3,
                status=status
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

        test_for_status(Item.COMMITTED)
        test_for_status(Item.WIP)
        test_for_status(Item.BLOCKED)

    def test_move_item_takes_only_review_when_status_pending_review(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=13,
            estimate_review=5,
            status=Item.PENDING_REVIEW
        )

        item.sprint = self.sprint2
        events = Event.create_item_changed_events(item)

        assert len(events) == 2

        assert events[0].change == Event.INC
        assert events[0].value == 5
        assert events[0].sprint == self.sprint2

        assert events[1].change == Event.DEC
        assert events[1].value == 5
        assert events[1].sprint == self.sprint1

    def test_move_item_takes_only_review_when_status_review(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=8,
            estimate_review=2,
            status=Item.REVIEW
        )

        item.sprint = self.sprint2
        events = Event.create_item_changed_events(item)

        assert len(events) == 2

        assert events[0].change == Event.INC
        assert events[0].value == 2
        assert events[0].sprint == self.sprint2

        assert events[1].change == Event.DEC
        assert events[1].value == 2
        assert events[1].sprint == self.sprint1

    def test_move_item_takes_only_review_when_status_fix(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=5,
            estimate_review=3,
            status=Item.FIX
        )

        item.sprint = self.sprint2
        events = Event.create_item_changed_events(item)

        assert len(events) == 2

        assert events[0].change == Event.INC
        assert events[0].value == 3
        assert events[0].sprint == self.sprint2

        assert events[1].change == Event.DEC
        assert events[1].value == 3
        assert events[1].sprint == self.sprint1

    def test_move_item_takes_nothing_when_status_external_review(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=13,
            estimate_review=2,
            status=Item.EXTERNAL_REVIEW
        )

        item.sprint = self.sprint2
        events = Event.create_item_changed_events(item)

        assert len(events) == 0

    def test_move_item_takes_effort_and_review_when_status_blocked(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=13,
            estimate_review=3,
            status=Item.BLOCKED
        )

        item.sprint = self.sprint2
        events = Event.create_item_changed_events(item)

        assert len(events) == 2

        assert events[0].change == Event.INC
        assert events[0].value == 16
        assert events[0].sprint == self.sprint2

        assert events[1].change == Event.DEC
        assert events[1].value == 16
        assert events[1].sprint == self.sprint1


class StatusChangeEventFactoryTestCase(TestCase):
    def setUp(self):
        self.sprint1 = Sprint.objects.create(
            name="256",
            start_date=datetime.date(2015, 3, 8),
            end_date=datetime.date(2015, 3, 18),
        )

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

    def test_pending_review_to_review(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=8,
            estimate_review=3,
            status=Item.PENDING_REVIEW
        )

        item.status = Item.REVIEW

        events = Event.create_item_changed_events(item)
        assert len(events) == 0

    def test_review_to_fix(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=8,
            estimate_review=3,
            status=Item.REVIEW
        )

        item.status = Item.FIX

        events = Event.create_item_changed_events(item)
        assert len(events) == 0

    def test_fix_to_external_review(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=21,
            estimate_review=13,
            status=Item.FIX
        )

        item.status = Item.EXTERNAL_REVIEW

        events = Event.create_item_changed_events(item)
        assert len(events) == 1
        assert events[0].change == Event.DEC
        assert events[0].value == 13

    def test_external_review_to_done(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=21,
            estimate_review=13,
            status=Item.EXTERNAL_REVIEW
        )

        item.status = Item.DONE

        events = Event.create_item_changed_events(item)
        assert len(events) == 0

    def test_committed_to_blocked(self):
        item = Item.objects.create(
            name="Item",
            sprint=self.sprint1,
            estimate_work=21,
            estimate_review=13,
            status=Item.COMMITTED
        )

        item.status = Item.BLOCKED

        events = Event.create_item_changed_events(item)
        assert len(events) == 0
