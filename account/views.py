import email
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import UserDashSerializer, UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from account.renderers import Renderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User


# Generate token manually

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.


class UserResgister(APIView):
    renderer_classes = [Renderer]

    def post(self, request, format=None):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({
                "message": "You are successfully registered.",
                "status": status.HTTP_201_CREATED,
                "user": {
                    "username": request.data['username'],
                    "email": request.data['email'],
                    "phone": request.data['phone'],
                },
                "token": token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    renderer_classes = [Renderer]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({
                    "message": "Login Successfully.",
                    "token": token
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'non_field_errors': 'Email or Password is not Valid'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDash(APIView):
    renderer_classes = [Renderer]

    def get(self, request, format=None):
        serializer = UserDashSerializer(request.user) 
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserRegisterSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
