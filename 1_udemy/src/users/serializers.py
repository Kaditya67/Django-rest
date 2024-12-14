from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=False)
    username = serializers.CharField(read_only=True)

    def create(self,validated_data):
        print(validated_data)
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        username = f"{first_name}_{last_name}".lower() 
        counter = 0
        
        unique_username = username
        while User.objects.filter(username=unique_username).exists():
            counter += 1
            unique_username = f"{username}_{counter}"
        validated_data['username'] = unique_username 

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
