from dataclasses import fields
from rest_framework import serializers
from account.models import User
from rest_framework.response import Response
from rest_framework import status


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {
            "password": {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Pasword doesn't match")

        return super().validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)

    def update(self, instance, validated_data):
    
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)

    class Meta:
        model = User
        fields = ['email', 'password']

class UserDashSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    class Meta:
        model = User
        fields = ['email', 'username', 'phone']