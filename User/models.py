from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db.models import AutoField, CharField, BooleanField

from User.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = AutoField(primary_key=True)
    full_name = CharField(max_length=255)
    email = CharField(max_length=255, unique=True)
    email_verified = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']
