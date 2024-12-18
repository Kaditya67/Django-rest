from django.contrib import admin
from .models import Task, TaskList, Attachment

class AttachmentAdmin(admin.ModelAdmin):
    readonly_fields = ('id','created_at')

class TaskListAdmin(admin.ModelAdmin):
    pass
admin.site.register(Task)
admin.site.register(TaskList)
admin.site.register(Attachment,AttachmentAdmin)