from rest_framework import routers
from .viewsets import TaskListViewset, TaskViewset, AttachmentViewset

app_name = 'task'
router = routers.DefaultRouter()
router.register('tasklists', TaskListViewset, basename='tasklist')
router.register(r'tasks', TaskViewset, basename='task')
router.register('attachments', AttachmentViewset, basename='attachment')