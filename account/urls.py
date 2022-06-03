from django.urls import path
from account.views import UserResgister, UserLogin, UserDash, UserUpdate


urlpatterns = [
    path('register', UserResgister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('update', UserUpdate.as_view(), name='update'),
    path('dashboard', UserDash.as_view(), name='dashboard'),
]