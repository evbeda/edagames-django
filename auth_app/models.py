from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from development.encode_jwt import encode_data


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    username = models.CharField(max_length=25, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return "@{}".format(self.username)


class BotManager(models.Manager):
    def create(self, *args, **kwargs):
        if 'name' in kwargs:
            kwargs['token'] = encode_data(
                key='user',
                value=kwargs['name'],
            )
        return super().create(*args, **kwargs)


class Bot(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=200, default='')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    objects = BotManager()
