from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer
from .models import TaskList, Task, Attachment
from rest_framework import mixins, response, viewsets, status
from .permissions import IsAllowedToEditTaskListElseNone, IsAllowedToEditTaskOrNone, IsAllowedToEditAttachmentElseNone
from rest_framework.decorators import action
from django.utils import timezone
from .models import COMPLETE,NOT_COMPLETE

class TaskListViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                      viewsets.GenericViewSet, mixins.DestroyModelMixin):
    permission_classes = [IsAllowedToEditTaskListElseNone]
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer

class TaskViewset(viewsets.ModelViewSet):
    permission_classes = [IsAllowedToEditTaskOrNone]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super(TaskViewset, self).get_queryset()
        user_profile = self.request.user.profile
        updated_queryset = queryset.filter(created_by=user_profile)
        return updated_queryset

    @action(methods=['patch'], detail=True)
    def update_task_status(self, request, pk=None):
        try:
            task = self.get_object()  # DRF provides `get_object` for detail routes
            profile = request.user.profile
            task_status = request.data.get('status')  # Use `.get()` for safety

            if task_status == NOT_COMPLETE:
                if task.status == COMPLETE:
                    task.status = NOT_COMPLETE
                    task.completed_by = None
                    task.completed_at = None
                else:
                    raise Exception('Task is already not complete')
            elif task_status == COMPLETE:
                if task.status == NOT_COMPLETE:
                    task.status = COMPLETE
                    task.completed_by = profile
                    task.completed_at = timezone.now()
                else:
                    raise Exception('Task is already marked complete')
            else:
                raise Exception(f"Incorrect status provided! Received: {task_status}")

            task.save()
            serializer = TaskSerializer(instance=task, context={"request": request})
            return response.Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as error:
            return response.Response({'detail': str(error) + " This is final error"}, status=status.HTTP_400_BAD_REQUEST)

class AttachmentViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                        mixins.ListModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditAttachmentElseNone]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
