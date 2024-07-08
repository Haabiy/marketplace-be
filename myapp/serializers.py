from django.contrib.auth.models import User
from rest_framework import serializers
from .models import SourceModel

from django import forms


class SourceSerializer(serializers.ModelSerializer):
    next_status = serializers.CharField(read_only=True)
    class Meta:
        model = SourceModel
        fields = '__all__' 

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user