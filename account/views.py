from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

# Create your views here.

class UserResgister(APIView):
    def post(self, request, format=None):
        return Response({
            "message": "You are successfully registered."
        })