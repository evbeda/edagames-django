from django.db.models.signals import post_save
from django.contrib.auth import get_user_model as User
from django.dispatch import receiver


@receiver(post_save, sender=User)
def generate_token(sender, instance, **kwargs):
    sender.generate_token()
