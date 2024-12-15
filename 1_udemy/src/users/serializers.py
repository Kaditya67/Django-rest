from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'image']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    old_password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True)
    profile = ProfileSerializer(read_only=True)

    def validate(self, data):
        request_method = self.context.get('request').method
        password = data.get('password', None)   
        if request_method == 'POST':
            if not password:
                raise serializers.ValidationError({'password': ['This field is required.']})
        elif request_method == 'PUT' or request_method == 'PATCH':
            old_password = data.get('old_password', None)
            if not password:
                raise serializers.ValidationError({'password': ['Password is required.']})
            elif not old_password:
                raise serializers.ValidationError({'old_password': ['old_password is required.']})
        return data
        

    def create(self, validated_data):
        # Remove `old_password` if it exists
        validated_data.pop('old_password', None)

        password = validated_data.pop('password', None)
        first_name = validated_data.get('first_name', 'user').lower()
        last_name = validated_data.get('last_name', 'unknown').lower()

        # Generate a unique username
        username = ''.join(filter(str.isalnum, f"{first_name}_{last_name}"))
        counter = 0
        unique_username = username
        while User.objects.filter(username=unique_username).exists():
            counter += 1
            unique_username = f"{username}_{counter}"
        validated_data['username'] = unique_username

        # Create user
        user = User.objects.create_user(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Remove `old_password` if it exists
        old_password = validated_data.pop('old_password', None)
        password = validated_data.pop('password', None)

        if old_password and password:
            if instance.check_password(old_password):
                instance.set_password(password)
            else:
                raise serializers.ValidationError("Old password is incorrect.")
        elif password or old_password:
            raise serializers.ValidationError("Both old and new passwords are required.")

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'old_password','profile']

