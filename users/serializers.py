from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email','firstname', 'lastname','cv','signup_choices','jobType','jobContract')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'firstname','lastname','cv','signup_choices','jobType','jobContract')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['firstname'], validated_data['lastname'],validated_data['password'],signup_choices=validated_data['signup_choices'],cv=validated_data['cv'],jobType=validated_data['jobType'],jobContract=validated_data['jobContract'])

        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")