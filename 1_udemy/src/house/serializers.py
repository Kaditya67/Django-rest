from rest_framework import serializers
from django.urls import reverse
from .models import House

class HouseSerializer(serializers.ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)
    members = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(many=False, read_only=True, view_name='profile-detail')
    url = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = [
            'url', 
            'id', 
            'image', 
            'name', 
            'manager',
            'members',
            'members_count', 
            'description', 
            'created_at', 
            'points', 
            'completed_tasks_count', 
            'notcompleted_tasks_count'
        ]
        read_only_fields = ['points', 'completed_tasks_count', 'notcompleted_tasks_count']

    def get_url(self, obj):
        """
        Dynamically generates the URL for a House object by appending its ID.
        """
        request = self.context.get('request')
        if request:
            # Include namespace 'house' in the view name
            return request.build_absolute_uri(reverse('house:house-detail', args=[obj.id]))
        return None
