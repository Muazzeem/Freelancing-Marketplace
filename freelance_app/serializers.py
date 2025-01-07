from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, Job


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "role", "email", "username", "password"]
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            role=validated_data['role']
        )

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','username', 'role']  # Include password if needed
        read_only_fields = ['username']  # Username is read-only (can't be updated)

    def update(self, instance, validated_data):
        # Update the instance with validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Save the updated instance to the database
        instance.save()
        return instance


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ["id", "title", "description", "created_at"]
        read_only_fields = ["id", "created_at"]