from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from account.renderers import Renderer

# Create your views here.


class UserResgister(APIView):
    renderer_classes = [Renderer]
    def post(self, request, format='JSON'):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({
                "message": "You are successfully registered.",
                "status": status.HTTP_201_CREATED,
                "user": {
                    "username": request.data['username'],
                    "email": request.data['email'],
                    "phone": request.data['phone'],
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    renderer_classes = [Renderer]
    def post(self, request, format='JSON'):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                return Response({
                    "message": "Login Successfully."
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'non_field_errors': 'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
