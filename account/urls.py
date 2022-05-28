from django.urls import path
from account.views import UserResgister


urlpatterns = [
    path('register', UserResgister.as_view(), name='register')
]