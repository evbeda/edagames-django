from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin)
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from development.token import generate_token


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


@receiver(post_save, sender=User)
def after_user_signed_up(sender, instance, **kwargs):
    if Bot.objects.filter(user=instance,).count() == 0:
        Bot.objects.create(
            name=instance.username,
            token=generate_token(instance.username),
            user=instance,
        )


class Bot(models.Model):
    name = models.CharField(max_length=30)
    token = models.CharField(max_length=200, default='')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        null=True
    )
