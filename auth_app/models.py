# from django.db import models
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.models import (
#     AbstractBaseUser,
#     PermissionsMixin,
#     BaseUserManager,
# )

# class Player(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     user_name = models.CharField(max_length=150, unique=True)
#     first_name = models.CharField(max_length=150, blank=True)
#     last_name = models.CharField(max_length=150, blank=True)
#     start_date = models.DateTimeField(default=timezone.now)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)

#     objects = CustomAccountManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['user_name', 'first_name']

#     def __str__(self):
#         return self.user_name
