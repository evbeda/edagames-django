from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone

from development.encode_jwt import encode_data
from . import REGIONS


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        user = self.model(
            email=self.normalize_email(email),
            username=username,)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, username, password=None):
        from tournaments.models import TournamentRegistration
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        TournamentRegistration.objects.create(user=user)
        Bot.objects.create(user=user, name=user.email)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', unique=True)
    username = models.CharField(max_length=50, unique=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    profile_image = models.URLField(blank=True, null=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return "@{} - {}".format(self.username, self.email)


class UserProfile(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    country = models.CharField(max_length=100)
    region = models.CharField(max_length=100, choices=REGIONS)
    city_zone = models.CharField(max_length=100)
    # birthday = models.DateTimeField(blank=True, null=True)
    linkedin_profile = models.CharField(max_length=100)
    github_username = models.CharField(max_length=100)
    education_background = models.CharField(max_length=100)
    english_level = models.CharField(max_length=50)
    intro = models.TextField(max_length=1000)


class BotManager(models.Manager):
    def create(self, *args, **kwargs):
        if 'name' in kwargs:
            kwargs['token'] = encode_data(
                key='user',
                value=kwargs['name'],
            )
        return super().create(*args, **kwargs)


class Bot(models.Model):
    name = models.CharField(max_length=50)
    token = models.CharField(max_length=200, default='')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    objects = BotManager()

    def __str__(self):
        return "[{}] - {} :: {}".format(str(self.user), self.name, self.token)
