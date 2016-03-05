import datetime

from django.test import TestCase

from scrumboard.models import Event, Sprint


class EventTestCase(TestCase):
    def setUp(self):
        self.sprint = Sprint.objects.create(
            name='256',
            start_date=datetime.date(2015, 4, 30),
            end_date=datetime.date(2015, 5, 10)
        )

    def test_if_event_can_be_created(self):
        event = Event.objects.create(
            sprint=self.sprint,
            change=Event.INC,
            value=3
        )

        assert event in Event.get_events(self.sprint)

    def test_if_events_can_be_casted_to_integer(self):
        event = Event.objects.create(
            sprint=self.sprint,
            change=Event.DEC,
            value=8
        )

        assert -8 == int(event)

    def test_if_events_can_be_added_to_zero(self):
        event = Event.objects.create(
            sprint=self.sprint,
            change=Event.DEC,
            value=5
        )

        assert -5 == event + 0
        assert -5 == 0 + event

    def test_if_events_can_be_added_to_int(self):
        event = Event.objects.create(
            sprint=self.sprint,
            change=Event.INC,
            value=13
        )

        assert 34 == event + 21
        assert 34 == 21 + event

    def test_if_events_can_be_added_to_themselves(self):
        ev1 = Event.objects.create(
            sprint=self.sprint,
            change=Event.DEC,
            value=3
        )
        ev2 = Event.objects.create(
            sprint=self.sprint,
            change=Event.INC,
            value=5
        )

        assert 2 == ev1 + ev2


def from_iso(iso_string):
    return datetime.datetime.strptime(iso_string, "%Y-%m-%d")


class EventInSprintTestCase(TestCase):
    def setUp(self):
        self.start_date = datetime.date(2015, 4, 30)
        self.end_date = datetime.date(2015, 5, 10)

        self.sprint = Sprint.objects.create(
            name='256',
            start_date=self.start_date,
            end_date=self.end_date
        )

        self.changes = [("2015-04-30", 54), ("2015-05-01", -5), ("2015-05-02", -4), ("2015-05-03", -8),
                        ("2015-05-04", -13),
                        ("2015-05-07", -8), ("2015-05-08",  5), ("2015-05-09", -3), ("2015-05-10", -5),
                        ("2015-05-11", -13)]

    @staticmethod
    def create_events(sprint, changes):
        events = []

        for change in changes:
            event = Event.objects.create(
                sprint=sprint,
                date=from_iso(change[0]),
                change=Event.INC if change[1] > 0 else Event.DEC,
                value=abs(change[1])
            )
            events.append(event)

        return events

    def test_events_can_be_fetched_by_sprint(self):
        events = self.create_events(self.sprint, self.changes)
        assert len(events) == len(Event.get_events(self.sprint))

    def test_events_can_be_fetched_ordered_by_date(self):
        more_changes = [("2015-05-01", 3), ("2015-05-02", 5), ("2015-05-09", -8)]

        events = self.create_events(self.sprint, self.changes + more_changes)

        assert len(events) == len(Event.get_events(self.sprint))

        timetable = Event.get_events_timetable(self.sprint)
        assert 2 == len(timetable["2015-05-01"])
        assert -2 == sum(timetable["2015-05-01"])
