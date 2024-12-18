from rest_framework import viewsets,status,filters
from .models import House

from .serializers import HouseSerializer
from .permissions import IsHouseManagerOrNone
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend

class HouseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsHouseManagerOrNone]
    queryset = House.objects.all()
    serializer_class = HouseSerializer
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    search_fields = ['=name','description']
    ordering_fields = ['points','completed_tasks_count','notcompleted_tasks_count']
    filterset_fields = ['members']

    @action(detail=True, methods=['post'],name='Join', permission_classes=[])
    def join(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if(user_profile.house == None):
                user_profile.house = house
                user_profile.save()
                return Response({'detail':'You are now a member of this house'},status=status.HTTP_200_OK)
            elif(user_profile.house == house):
                return Response({'detail':'You are already a member of this house'},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'detail':'You are already a member of another house'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'detail':str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'],name='Leave', permission_classes=[])
    def leave(self, request, pk=None):
        try:
            house = self.get_object()
            user_profile = request.user.profile
            if(user_profile.house == house):
                user_profile.house = None
                user_profile.save()
                return Response({'detail':'You have left the house'},status=status.HTTP_200_OK)
            else:
                return Response({'detail':'You are not a member of this house'},status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({'detail':str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=['post'],name='Remove Member')
    def remove_member(self, request, pk=None):
        try:
            house = self.get_object()
            user_id = request.data.get('user_id',None)
            if(user_id == None):
                return Response({'detail':'user_id is required'},status=status.HTTP_400_BAD_REQUEST)
            user_profile = User.objects.get(pk=user_id).profile
            house_members = house.members
            if(user_profile in house_members.all()):
                house_members.remove(user_profile)
                house.save()
                return Response({'detail':'Member removed successfully'},status=status.HTTP_200_OK)
            else:
                return Response({'detail':'You are not a member of this house'},status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist as error:
            return Response({'detail':str(error)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)