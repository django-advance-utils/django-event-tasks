from django.db import models
from time_stamped_model.models import TimeStampedModel
from django.conf import settings


class TaskType(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class ReminderType(TimeStampedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class TaskTypeReminder(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    reminder_type = models.ForeignKey(ReminderType, on_delete=models.PROTECT)
    minutes_before = models.IntegerField()


class TimeType(TimeStampedModel):
    TIME_TYPE_ALL_DAY = 0
    TIME_TYPE_CUSTOM = 1
    TIME_TYPE_SET_TIME = 2

    TIME_CHOICES = (
        (TIME_TYPE_ALL_DAY, 'All Day'),
        (TIME_TYPE_CUSTOM, 'Custom'),
        (TIME_TYPE_SET_TIME, 'Set Time'),
    )

    name = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(choices=TIME_CHOICES, default=TIME_TYPE_SET_TIME)
    time = models.TimeField(null=True, blank=True)
    default = models.BooleanField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class TaskStatus(TimeStampedModel):
    TASK_STATUS_ACTIVE = 1
    TASK_STATUS_PAUSED = 2
    TASK_STATUS_COMPLETED = 3

    name = models.CharField(max_length=100)
    TASK_STATUS_CHOICES = ((TASK_STATUS_ACTIVE, 'Active'),
                           (TASK_STATUS_PAUSED, 'Paused'),
                           (TASK_STATUS_COMPLETED, 'Completed'))
    type = models.PositiveSmallIntegerField(choices=TASK_STATUS_CHOICES, default=TASK_STATUS_ACTIVE)

    class Meta:
        ordering = ('name',)


class Task(TimeStampedModel):
    task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='task_created_by')
    assign_to = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='assign_to_by')
    time_type = models.ForeignKey(TimeType, on_delete=models.PROTECT)
    task_due_date = models.DateField()
    task_due_time = models.TimeField(blank=True, null=True)
    task_status = models.ForeignKey(TaskStatus, on_delete=models.PROTECT)

    def __str__(self):
        return self.task_type.name

    class Meta:
        ordering = ('task_due_date', 'task_due_time')


class TaskReminder(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    reminder_date_time = models.DateTimeField()
    reminder_type = models.ForeignKey(ReminderType, on_delete=models.PROTECT)

