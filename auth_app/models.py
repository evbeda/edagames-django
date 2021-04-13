from django.db import models
from django.contrib.auth.models import User
import uuid


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=True, unique=True)

    def __str__(self):
        return f'{self.user.username} Profile'
