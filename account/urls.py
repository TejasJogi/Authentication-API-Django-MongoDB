from django.urls import path
from account.views import UserResgister, UserLogin


urlpatterns = [
    path('register', UserResgister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
]