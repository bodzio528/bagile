from colorfield.fields import ColorField
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone


# SPRINT
# +-------------------------------------+
# |     Start Date    |     End Date    |
# +-------------------------------------+
# |        NAME / NUMBER / ID           |
# +-------------------------------------+
class Sprint(models.Model):
    name = models.CharField(
        max_length=7,
        blank=True,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.PositiveIntegerField(
        default=0,
        blank=True,
    )

    def __str__(self):
        return '{0}'.format(self.name)

    def is_active(self):
        from datetime import date

        now = timezone.now()
        today = date(now.year, now.month, now.day)

        return self.start_date <= today <= self.end_date

    @staticmethod
    def get_active_sprints():
        return [sprint for sprint in list(Sprint.objects.all()) if sprint.is_active()]

    @staticmethod
    def get_current_sprint():
        sprints = Sprint.get_active_sprints()
        return sorted(sprints, key=lambda s: s.start_date)[0] if len(sprints) > 0 else None

    def get_absolute_url(self):
        return reverse('scrumboard:sprint_details', kwargs={'pk': self.pk})


# ITEM
# +-------------------------------------+
# |      Name       | Estimate | Review |
# +-------------------------------------+
# |       ITEM                          |
# |            DESCRIPTION              |
# |                        HERE         |
# +-------------------------------------+
# | Status | Sprint |   Assigned User   |
# +-------------------------------------+
class Item(models.Model):
    COMMITTED = 1
    WIP = 2
    PENDING_REVIEW = 3
    REVIEW = 4
    FIX = 5
    EXTERNAL_REVIEW = 6
    BLOCKED = 7
    DONE = 8

    name = models.CharField(
        max_length=63,
    )
    description = models.TextField(
        max_length=255,
    )
    estimate_work = models.PositiveIntegerField(
        default=0,
    )
    estimate_review = models.PositiveIntegerField(
        default=0,
    )
    status = models.IntegerField(
        choices=(
            (COMMITTED, 'Committed'),
            (WIP, 'Work In Progress'),
            (PENDING_REVIEW, 'Ready to Review'),
            (REVIEW, 'Under Review'),
            (FIX, 'Fix'),
            (EXTERNAL_REVIEW, 'External Review'),
            (BLOCKED, 'Blocked'),
            (DONE, 'Done'),
        ),
        default=COMMITTED,
    )
    color = ColorField(default='#96CFFF')
    assignee = models.ForeignKey(
        User,
        models.SET_NULL,
        blank=True,
        null=True,
    )
    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return '{0}: {1} [E{2} R{3}]'.format(
                self.name,
                self.description,
                self.estimate_work,
                self.estimate_review)

    def get_absolute_url(self):
        return reverse('scrumboard:item_details', kwargs={'pk': self.pk})

    def get_full_estimate(self):
        return self.estimate_work + self.estimate_review

# +--------+--------------------------------------------------+--------------+
# | SPRINT | WIP | RDY | REV | FIX | EXT | BLK |  COMMITTED   |     DONE     |
# +--------+-----------------------------------+--------------+--------------+
# |  IMG 1 |[it]              [it]             | [item]       | [item]       |
# +--------+-----------------------------------+    [item]    |       [item] |
# |  IMG 2 |      [it]        [it]             | [item]       |     [item]   |
# +--------+-----------------------------------+              |              |
# |  IMG 3 |            [it]                   |   [item]     | [item]       |
# +--------+-----------------------------------+--------------+--------------+
# +---------------+
# |Burndown Chart |
# |o              |
# |  o            |
# |      o o      |
# |          o    |
# |            o o|
# |M T W T F M T W|
# +---------------+


# SCRUMBOARD EVENT
# +--------+------------+--------+-------+
# | Sprint | Date       | Change | Value |
# +--------+------------+--------+-------+
# |  254.3 | 2016-03-20 |    INC |     3 |
# +--------+------------+--------+-------+
# |  254.3 | 2016-03-20 |    DEC |     5 |
# +--------+------------+--------+-------+
class Event(models.Model):
    INC = 1
    DEC = -1

    sprint = models.ForeignKey(
        Sprint,
        on_delete=models.CASCADE,
        blank=False,
        null=False)
    date = models.DateField(
        default=timezone.datetime.today
    )
    change = models.SmallIntegerField(
        choices=(
            (INC, 'Estimate Increased'),
            (DEC, 'Estimate Decreased'),
        ),
        default=INC
    )
    value = models.PositiveSmallIntegerField(
        blank=False,
        default=0
    )

    @staticmethod
    def get_events(sprint):
        return Event.objects.filter(sprint=sprint)

    @staticmethod
    def get_events_timetable(sprint):
        from collections import defaultdict

        timetable = defaultdict(set)
        for event in Event.get_events(sprint):
            timetable[str(event.date)].add(event)

        return timetable

    @staticmethod
    def create_item_created_event(instance):
        return Event(
            sprint=instance.sprint,
            change=Event.INC,
            value=instance.get_full_estimate()
        )

    @staticmethod
    def create_item_deleted_event(instance):
        return Event(
            sprint=instance.sprint,
            change=Event.DEC,
            value=instance.get_full_estimate()
        )

    @staticmethod
    def create_item_changed_events(instance):
        try:
            old_instance = Item.objects.get(pk=instance.pk)
            events = []

            def add_event_for_change(sprint, diff):
                if diff != 0:
                    events.append(Event(sprint=sprint,
                                        change=Event.INC if diff > 0 else Event.DEC,
                                        value=abs(diff)))

            group = ({Item.EXTERNAL_REVIEW, Item.DONE},
                     {Item.PENDING_REVIEW, Item.REVIEW, Item.FIX},
                     {Item.COMMITTED, Item.WIP, Item.BLOCKED})

            review = (instance.estimate_review - old_instance.estimate_review) if old_instance.status not in group[0] else 0
            effort = (instance.estimate_work - old_instance.estimate_work) if old_instance.status in group[2] else 0

            add_event_for_change(old_instance.sprint, effort + review)

            if instance.status != old_instance.status:
                tt = [(0, 1, 0, Event.INC),
                      (1, 0, 0, Event.DEC),
                      (1, 2, Event.INC, 0),
                      (2, 1, Event.DEC, 0),
                      (0, 2, Event.INC, Event.INC),
                      (2, 0, Event.DEC, Event.DEC)]

                change_expr = next((t for t in tt if old_instance.status in group[t[0]] and instance.status in group[t[1]]), None)

                if change_expr is not None:
                    add_event_for_change(old_instance.sprint,
                                         change_expr[2] * instance.estimate_work +
                                         change_expr[3] * instance.estimate_review)

            if instance.sprint.pk != old_instance.sprint.pk:
                review = instance.estimate_review if instance.status not in group[0] else 0
                effort = instance.estimate_work if instance.status in group[2] else 0

                add_event_for_change(instance.sprint, effort + review)
                add_event_for_change(old_instance.sprint, -(effort + review))

            return events
        except Item.DoesNotExist:
            return []

    def __str__(self):
        return '{2}{3} {1} ({0})'.format(
                self.sprint,
                self.date,
                '-' if self.change == Event.DEC else '',
                self.value)

    def __int__(self):
        return self.value * self.change

    def __add__(self, other):
        if isinstance(other, Event):
            assert other.sprint.pk == self.sprint.pk
        return int(self) + int(other)

    def __radd__(self, other):
        if isinstance(other, Event):
            assert other.sprint.pk == self.sprint.pk
        return other + self.value * self.change


@receiver(pre_save, sender=Item)
def create_event_for_item_update(sender, instance, **kwargs):
    events = Event.create_item_changed_events(instance)
    for event in events:
        event.save()


@receiver(post_save, sender=Item)
def create_event_for_item_create(sender, instance, created, **kwargs):
    if created:
        Event.create_item_created_event(instance).save()


@receiver(pre_delete, sender=Item)
def create_event_for_item_delete(sender, instance, **kwargs):
    Event.create_item_created_event(instance).save()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class UserProfile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
    )
    avatar = models.FileField(
        upload_to=user_directory_path,
    )

    def __str__(self):
        return 'User {0}'.format(self.user.name)

    def get_absolute_url(self):
        return reverse('scrumboard:user_details', kwargs={'pk': self.pk})
