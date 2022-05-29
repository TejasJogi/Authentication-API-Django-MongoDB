from rest_framework import serializers
from account.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'password2']
        extra_kwargs = {
            "password": {'write_only': True}
        }

    def passwordvalidat(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Pasword doesn't match")

        return super().validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)