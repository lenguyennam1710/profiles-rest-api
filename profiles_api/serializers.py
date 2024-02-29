from rest_framework import serializers
from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """Serializers a name field for testing our APIView"""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializers a user profile object"""

    """The way we use a meta class is to configure the serializer to a
    specific model in our project"""
    class Meta:
        #set serializer up to point to user profile model
        model = models.UserProfile

        #lists of all the fields we want to manage through our serializer
        fields = ('id', 'email', 'name', 'password')

        extra_kwargs = {
            'password': {
                'write_only': True,
            'style': {'input_type': 'password'}
            }
        }
    def create(self, validated_data):
        """Create and return a new user"""
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user

    def update(self, instance, validated_data):
        """Handle updating user account"""
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance, validated_data)
