from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


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
        return '{0}: {1}/{2}'.format(self.name, self.start_date, self.end_date)

    def is_active(self):
        from datetime import date

        now = timezone.now()
        today = date(now.year, now.month, now.day)

        return self.start_date <= today <= self.end_date

    @staticmethod
    def fetch_active():
        return [sprint for sprint in list(Sprint.objects.all()) if sprint.is_active()]


# ITEM
# +-------------------------------------+
# |      Name       | Estimate | Review |
# +-------------------------------------+
# |       ITEM                          |
# |            DESCRIPTION              |
# |                        HERE         |
# +-------------------------------------+
# |                     Assigned User   |
# +-------------------------------------+
class Item(models.Model):
    COMMITTED = 1
    WIP = 2
    REVIEW = 3
    FIX = 4
    EXTERNAL_REVIEW = 5
    BLOCKED = 6
    DONE = 7

    name = models.CharField(
        max_length=63,
        blank=True,
    )
    description = models.TextField(
        max_length=255,
        blank=True,
    )
    status = models.IntegerField(
        choices=(
            (COMMITTED, 'Committed'),
            (WIP, 'Work In Progress'),
            (REVIEW, 'Under Review'),
            (FIX, "Fix"),
            (EXTERNAL_REVIEW, 'External Review'),
            (BLOCKED, 'Blocked'),
            (DONE, 'Done'),
        ),
        default=COMMITTED,
        blank=False,
    )
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
        return '{0}: {1}'.format(self.name, self.description)


# That's now the name of the reverse filter
# Item.objects.filter(tag__name="LTE3033")
class Tag(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="tags",
        related_query_name="tag",
    )
    name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.name


# +--------+--------------------------------------------+--------------+
# | SPRINT | WIP | REV | FIX | EXT | BLK |  COMMITTED   |     DONE     |
# +--------+-----------------------------+--------------+--------------+
# |  IMG 1 |                             |              |              |
# +--------+-----------------------------+              |              |
# |  IMG 2 |                             |              |              |
# +--------+-----------------------------+              |              |
# |  IMG 3 |                             |              |              |
# +--------+-----------------------------+--------------+--------------+
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
        return 'UserProfile {0}'.format(self.user.name)
