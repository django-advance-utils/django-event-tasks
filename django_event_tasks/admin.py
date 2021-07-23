from django.contrib import admin

from django_event_tasks.models import TaskType, ReminderType, TimeType, TaskStatus, Task, TaskReminder


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )


class TaskTypeReminderInline(admin.TabularInline):
    model = TaskReminder


@admin.register(ReminderType)
class ReminderTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    inlines = [TaskTypeReminderInline]


@admin.register(TimeType)
class TimeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'time', 'default')


@admin.register(TaskStatus)
class TaskStatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')


class TaskReminderInline(admin.TabularInline):
    model = TaskReminder


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskReminderInline]
    list_display = ('task_type', 'created_by', 'time_type', 'task_due_date', 'task_status')
