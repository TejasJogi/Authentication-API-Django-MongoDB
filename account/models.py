from djongo import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, username, phone, password=None, password2=None):
        """
        Creates and saves a User with the given email, name, phone and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            username=username,
            phone=phone,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, phone, password=None):
        """
        Creates and saves a superuser with the given email, name, phone and password.
        """
        user = self.create_user(
            email,
            phone=phone,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

#  Custom User Model


class User(AbstractBaseUser):
    username = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin